#!/usr/bin/env python3
"""
MRS Parser with Knowledge Linking and LLM-based Pruning
Parses sentences to MRS, links to Wikidata and WordNet, prunes with ollama, saves as YAML
"""

import time
import argparse
import yaml
import psycopg2
import hashlib
import json
import requests
from pathlib import Path
from datetime import datetime
from delphin import ace
from delphin.mrs import MRS
import nltk
from nltk.corpus import wordnet as wn

# Ensure WordNet is downloaded
try:
    wn.ensure_loaded()
except:
    nltk.download('wordnet')
    nltk.download('omw-1.4')


class LLMPruner:
    """Prunes candidates using ollama LLM"""
    
    def __init__(self, model='gpt-oss:20b', ollama_url='http://localhost:11434', 
                 save_prompts=False, prompt_dir='sshg/prompt'):
        self.model = model
        self.ollama_url = ollama_url
        self.api_endpoint = f"{ollama_url}/api/generate"
        self.save_prompts = save_prompts
        self.prompt_dir = Path(prompt_dir)
        self.sentence_slug = None  # Will be set when first called
        
        # Load prompt template
        self.prompt_template = self._load_prompt_template()
        
        # Create prompt directory if needed
        if self.save_prompts:
            try:
                self.prompt_dir.mkdir(parents=True, exist_ok=True)
                print(f"✓ Prompt directory ready: {self.prompt_dir.absolute()}")
            except Exception as e:
                print(f"✗ Failed to create prompt directory: {e}")
                print(f"  Attempted path: {self.prompt_dir.absolute()}")
                raise
    
    def _sanitize_filename(self, text: str, max_length: int = 50) -> str:
        """Convert text to safe filename"""
        import re
        # Convert to lowercase and replace spaces/special chars with underscore
        text = text.lower()
        text = re.sub(r'[^\w\s-]', '', text)
        text = re.sub(r'[-\s]+', '_', text)
        # Trim to max length
        if len(text) > max_length:
            text = text[:max_length]
        return text.strip('_')
    
    def _save_prompt(self, prompt: str, sentence: str, word: str, batch_num: int):
        """Save prompt to file"""
        if not self.save_prompts:
            return
        
        # Generate sentence slug on first call
        if self.sentence_slug is None:
            self.sentence_slug = self._sanitize_filename(sentence)
        
        # Sanitize word for filename
        word_slug = self._sanitize_filename(word, max_length=20)
        
        # Generate filename with word included
        filename = f"{self.sentence_slug}_{word_slug}_{batch_num:02d}.txt"
        filepath = self.prompt_dir / filename
        
        # Save prompt
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(prompt)
        
        print(f"    Saved prompt to: {filepath}")
        
    def _load_prompt_template(self):
        """Load prompt template from file"""
        template_path = Path('sshg/prune_word_prompt.txt')
        if not template_path.exists():
            raise FileNotFoundError(f"Prompt template not found: {template_path}")
        
        with open(template_path, 'r', encoding='utf-8') as f:
            return f.read()
    
    def _call_ollama(self, prompt: str) -> str:
        """Call ollama API and return response"""
        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
            "temperature": 0.0  # Deterministic output
        }
        
        try:
            response = requests.post(self.api_endpoint, json=payload, timeout=120)
            response.raise_for_status()
            result = response.json()
            return result.get('response', '').strip()
        except Exception as e:
            print(f"Error calling ollama: {e}")
            return None
    
    def _parse_llm_response(self, response: str) -> list:
        """Parse LLM response to extract Q-IDs or synset IDs"""
        if not response:
            return []
        
        try:
            # Try to parse as JSON
            parsed = json.loads(response)
            if isinstance(parsed, list):
                return [str(item) for item in parsed]
            return []
        except json.JSONDecodeError:
            # Fallback: extract anything that looks like Q-IDs or synset IDs
            import re
            qids = re.findall(r'Q\d+', response)
            synsets = re.findall(r'\w+\.\w+\.\d+', response)
            return qids + synsets
    
    def prune_candidates_batch(self, sentence: str, word: str, word_index: int, 
                               candidates: list, batch_size: int = 20) -> list:
        """
        Prune candidates in batches using LLM
        Args:
            sentence: The full sentence
            word: The target word
            word_index: The Nth occurrence (0-indexed)
            candidates: List of candidate dicts with 'qid'/'synset' and 'label'/'definition'
            batch_size: Number of candidates per LLM call
        Returns:
            List of pruned candidates
        """
        if not candidates:
            return []
        
        print(f"  Pruning {len(candidates)} candidates in batches of {batch_size}...")
        
        all_pruned = []
        
        # Process in batches
        for i in range(0, len(candidates), batch_size):
            batch = candidates[i:i+batch_size]
            batch_num = (i // batch_size) + 1
            total_batches = (len(candidates) + batch_size - 1) // batch_size
            
            print(f"    Batch {batch_num}/{total_batches} ({len(batch)} candidates)...", end=' ')
            
            # Format candidates for prompt
            candidates_json = json.dumps(batch, ensure_ascii=False, indent=2)
            
            # Fill prompt template
            prompt = self.prompt_template.replace('{{sentence}}', sentence)
            prompt = prompt.replace('{{word}}', word)
            prompt = prompt.replace('{{word_index}}', str(word_index))
            prompt = prompt.replace('{{candidates}}', candidates_json)

            self._save_prompt(prompt, sentence, word, batch_num)
            
            # Call LLM
            response = self._call_ollama(prompt)
            
            if response is None:
                print("Failed (keeping all)")
                all_pruned.extend(batch)
                continue
            
            # Parse response
            kept_ids = self._parse_llm_response(response)
            
            # Filter batch based on LLM response
            for candidate in batch:
                candidate_id = candidate.get('qid') or candidate.get('synset')
                if candidate_id in kept_ids:
                    all_pruned.append(candidate)
            
            print(f"Kept {len([c for c in batch if (c.get('qid') or c.get('synset')) in kept_ids])}/{len(batch)}")
        
        print(f"  Total pruned: {len(all_pruned)}/{len(candidates)} candidates")
        return all_pruned


class KnowledgeLinker:
    """Links MRS predicates to Wikidata and WordNet"""
    
    def __init__(self, conn_str):
        self.conn = psycopg2.connect(conn_str)
        
    def search_wikidata(self, lemma, limit=100):
        """
        Search Wikidata for entities matching lemma
        Returns list of candidate Q-IDs with labels and descriptions
        """
        cursor = self.conn.cursor()
        candidates = []
        
        # Search in labels (case-insensitive)
        label_to_id_query = """
        SELECT entity_id FROM entity_labels
        WHERE LOWER(label) = LOWER(%s) AND language = 'en'
        LIMIT %s;
        """
        cursor.execute(label_to_id_query, (lemma, limit))
        entity_ids_from_label = [row[0] for row in cursor.fetchall()]

        if entity_ids_from_label:
            id_to_details_query = """
            SELECT DISTINCT e.id, el.label, ed.description
            FROM entities e
            JOIN entity_labels el ON e.id = el.entity_id AND el.language = 'en'
            LEFT JOIN entity_descriptions ed ON e.id = ed.entity_id AND ed.language = 'en'
            WHERE e.id = ANY(%s) AND e.type = 'item';
            """
            cursor.execute(id_to_details_query, (entity_ids_from_label,))
            results = cursor.fetchall()
            
            for qid, label, description in results:
                # Skip entries with empty descriptions
                if not description or description.strip() == '':
                    continue
                    
                candidates.append({
                    'qid': qid,
                    'label': label,
                    'description': description,
                    'source': 'label'
                })
        
        # Also search aliases if we have few results
        if len(candidates) < limit:
            alias_to_id_query = """
            SELECT entity_id FROM entity_aliases
            WHERE md5(alias) = %s AND language = 'en'
            LIMIT %s;
            """
            
            lemma_hash = hashlib.md5(lemma.encode('utf-8')).hexdigest()
            
            cursor.execute(alias_to_id_query, (lemma_hash, limit - len(candidates)))
            entity_ids = [row[0] for row in cursor.fetchall()]

            if entity_ids:
                id_to_details_query = """
                SELECT DISTINCT e.id, el.label, ed.description
                FROM entities e
                JOIN entity_labels el ON e.id = el.entity_id AND el.language = 'en'
                LEFT JOIN entity_descriptions ed ON e.id = ed.entity_id AND ed.language = 'en'
                WHERE e.id = ANY(%s)
                AND e.type = 'item';
                """
                
                cursor.execute(id_to_details_query, (entity_ids,))
                details_results = cursor.fetchall()

                for qid, label, description in details_results:
                    # Skip entries with empty descriptions
                    if not description or description.strip() == '':
                        continue
                        
                    if not any(c['qid'] == qid for c in candidates):
                        candidates.append({
                            'qid': qid,
                            'label': label,
                            'description': description,
                            'source': 'alias'
                        })
        
        cursor.close()
        return candidates
    
    def search_wordnet(self, lemma, pos=None):
        """
        Search WordNet for all synsets
        Returns all synsets where the lemma exactly matches
        """
        pos_map = {
            'n': wn.NOUN,
            'v': wn.VERB,
            'a': wn.ADJ,
            'r': wn.ADV
        }
        
        wn_pos = pos_map.get(pos) if pos else None
        
        try:
            synsets = wn.synsets(lemma, pos=wn_pos)
            
            candidates = []
            for synset in synsets:
                # Check if any lemma in this synset exactly matches our search term
                synset_lemma_names = [l.name() for l in synset.lemmas()]
                if lemma not in synset_lemma_names:
                    continue
                
                candidates.append({
                    'synset': synset.name(),
                    'definition': synset.definition()
                })
            
            return candidates
        except Exception as e:
            print(f"WordNet error for '{lemma}': {e}")
            return []
    
    def close(self):
        if self.conn:
            self.conn.close()


def is_top_unknown(mrs_obj: MRS) -> bool:
    top_handle = mrs_obj.top
    for hcon in mrs_obj.hcons:
        if hcon.hi == top_handle and hcon.relation == 'qeq':
            top_label = hcon.lo
            for ep in mrs_obj.rels:
                if ep.label == top_label and ep.predicate == 'unknown':
                    return True
    return False


def parse_sentence_to_mrs_all(sentence: str, grammar_path: str = None) -> list:
    """Parse sentence and return all MRS objects"""
    
    if grammar_path is None:
        possible_grammars = [
            'erg.dat',
            'erg-2025-x86-64-0.9.34.dat',
            '../erg.dat',
            '~/erg-2025-x86-64-0.9.34.dat'
        ]
        
        for gram in possible_grammars:
            gram_path = Path(gram).expanduser()
            if gram_path.exists():
                grammar_path = str(gram_path)
                print(f"Using grammar: {grammar_path}")
                break
        
        if grammar_path is None:
            print("Error: No ERG grammar file found.")
            return []
    else:
        grammar_path = str(Path(grammar_path).expanduser())
    
    try:
        with ace.ACEParser(grammar_path) as parser:
            response = parser.interact(sentence)
            
            results = response.results()
            if not results:
                print(f"Warning: No parse results for: '{sentence}'")
                return []
            
            mrs_list = []
            filtered_count = 0
            
            for result in results:
                mrs_obj = result.mrs()
                
                if is_top_unknown(mrs_obj):
                    filtered_count += 1
                    continue
                
                mrs_list.append(mrs_obj)
            
            print(f"Found {len(results)} parse(s), filtered {filtered_count} with 'unknown' predicates.")
            print(f"Valid parses: {len(mrs_list)}")
            return mrs_list
    
    except Exception as e:
        print(f"Error during parsing: {e}")
        return []


def extract_unique_nodes(mrs_list: list) -> tuple:
    """
    Extract unique lemma nodes (noun and verb only) from all MRS parses
    Returns: (nouns_dict, verbs_dict)
        Each dict has key=lemma, value={'lemma': str, 'sources': [{'parse_id': int, 'predicate': str}, ...]}
    """
    nouns = {}
    verbs = {}
    
    for parse_id, mrs_obj in enumerate(mrs_list):
        for ep in mrs_obj.rels:
            predicate = ep.predicate
            
            # Only process content predicates starting with '_'
            if not predicate.startswith('_'):
                continue
            
            parts = predicate[1:].split('_')
            if len(parts) < 2:
                continue
            
            lemma = parts[0]
            pos = parts[1]
            
            # Skip common/generic predicates
            skip_predicates = ['the', 'a', 'an', 'be', 'have', 'do']
            if lemma in skip_predicates:
                continue
            
            source_info = {
                'parse_id': parse_id,
                'predicate': predicate
            }
            
            # Categorize by POS
            if pos == 'n':
                if lemma not in nouns:
                    nouns[lemma] = {
                        'lemma': lemma,
                        'sources': []
                    }
                # Add source if not already present
                if source_info not in nouns[lemma]['sources']:
                    nouns[lemma]['sources'].append(source_info)
                    
            elif pos == 'v':
                if lemma not in verbs:
                    verbs[lemma] = {
                        'lemma': lemma,
                        'sources': []
                    }
                # Add source if not already present
                if source_info not in verbs[lemma]['sources']:
                    verbs[lemma]['sources'].append(source_info)
    
    return nouns, verbs


def find_word_index(sentence: str, word: str) -> int:
    """
    Find the index of word in sentence (0-based)
    Returns the first occurrence index
    """
    words = sentence.lower().split()
    word_lower = word.lower()
    
    try:
        return words.index(word_lower)
    except ValueError:
        return 0  # Default to 0 if not found


def link_nodes_to_knowledge(nodes: dict, pos: str, linker: KnowledgeLinker, 
                            pruner: LLMPruner, sentence: str, batch_size: int = 20) -> list:
    """
    Link all nodes to knowledge bases (Wikidata and WordNet) and prune with LLM
    Args:
        nodes: dict with key=lemma, value={'lemma': str, 'sources': [...]}
        pos: 'n' or 'v'
        linker: KnowledgeLinker instance
        pruner: LLMPruner instance
        sentence: The original sentence for context
        batch_size: Number of candidates per LLM call
    Returns: list of nodes with pruned knowledge links
    """
    print(f"\n=== Linking {len(nodes)} {pos} nodes to knowledge bases ===")
    
    linked_nodes = []
    
    for lemma, node_data in nodes.items():
        print(f"\nLinking: {lemma} ({pos})")
        
        # Find word index in sentence
        word_index = find_word_index(sentence, lemma)
        
        # Search WordNet (all synsets initially)
        wordnet_candidates = linker.search_wordnet(lemma, pos)
        print(f"  -> WordNet: {len(wordnet_candidates)} synsets (before pruning)")
        
        # Prune WordNet with LLM
        if wordnet_candidates and pruner:
            wordnet_candidates = pruner.prune_candidates_batch(
                sentence, lemma, word_index, wordnet_candidates, batch_size
            )
        
        # For nouns, also search Wikidata
        if pos == 'n':
            wikidata_candidates = linker.search_wikidata(lemma, limit=100)
            print(f"  -> Wikidata: {len(wikidata_candidates)} candidates (before pruning)")
            
            # Prune Wikidata with LLM
            if wikidata_candidates and pruner:
                wikidata_candidates = pruner.prune_candidates_batch(
                    sentence, lemma, word_index, wikidata_candidates, batch_size
                )
            
            node_entry = {
                'lemma': lemma,
                'sources': node_data['sources'],
                'wikidata': wikidata_candidates,
                'wordnet': wordnet_candidates
            }
        else:
            print(f"  -> Wikidata: skipped (verbs not in Wikidata)")
            node_entry = {
                'lemma': lemma,
                'sources': node_data['sources'],
                'wordnet': wordnet_candidates
            }
        
        linked_nodes.append(node_entry)
    
    return linked_nodes


def mrs_to_dict(mrs_obj: MRS) -> dict:
    """Convert MRS to dict without knowledge links"""
    
    mrs_dict = {
        'top': mrs_obj.top,
        'index': mrs_obj.index,
        'rels': [],
        'hcons': [],
        'icons': []
    }
    
    # Process predicates
    for ep in mrs_obj.rels:
        ep_dict = {
            'predicate': ep.predicate,
            'label': ep.label,
            'args': {}
        }
        
        # Arguments
        for role, value in ep.args.items():
            ep_dict['args'][role] = value
        
        mrs_dict['rels'].append(ep_dict)
    
    # Handle Constraints
    for hcon in mrs_obj.hcons:
        mrs_dict['hcons'].append({
            'relation': hcon.relation,
            'hi': hcon.hi,
            'lo': hcon.lo
        })
    
    # Individual Constraints
    for icon in mrs_obj.icons:
        mrs_dict['icons'].append({
            'relation': icon.relation,
            'left': icon.left,
            'right': icon.right
        })
    
    return mrs_dict


def save_all_mrs_to_yaml(mrs_list: list, noun_nodes: list, verb_nodes: list, 
                         output_path: str, sentence: str):
    """Save all MRS with pruned knowledge links to YAML"""
    
    output_dir = Path(output_path).parent
    if output_dir and str(output_dir) != '.':
        output_dir.mkdir(parents=True, exist_ok=True)
        print(f"Created directory: {output_dir}")
    
    parses = []
    for i, mrs_obj in enumerate(mrs_list):
        print(f"\nProcessing parse {i}...")
        mrs_dict = mrs_to_dict(mrs_obj)
        
        parse_entry = {
            'parse_id': i,
            'mrs': mrs_dict
        }
        parses.append(parse_entry)
    
    output_data = {
        'metadata': {
            'timestamp': datetime.now().isoformat(),
            'sentence': sentence,
            'parser': 'ACE + ERG',
            'knowledge_bases': ['Wikidata (nouns only)', 'WordNet'],
            'pruning': 'LLM-based (ollama gpt-oss:20b)',
            'num_parses': len(mrs_list),
            'num_noun_nodes': len(noun_nodes),
            'num_verb_nodes': len(verb_nodes),
            'note': 'Pruned: Wikidata for nouns, empty descriptions removed, LLM-based candidate pruning, examples/lemmas removed, simplemrs removed'
        },
        'parses': parses,
        'nodes': {
            'nouns': noun_nodes,
            'verbs': verb_nodes
        }
    }
    
    with open(output_path, 'w', encoding='utf-8') as f:
        yaml.dump(output_data, f, default_flow_style=False, allow_unicode=True, sort_keys=False)
    
    print(f"\nMRS saved to: {output_path}")
    print(f"Total parses saved: {len(mrs_list)}")
    print(f"Total noun nodes saved: {len(noun_nodes)}")
    print(f"Total verb nodes saved: {len(verb_nodes)}")


def main():
    main_start_time = time.perf_counter()

    parser = argparse.ArgumentParser(
        description='Parse sentence to MRS with knowledge linking and LLM pruning'
    )
    parser.add_argument('--sentence', type=str, required=True, help='Input sentence to parse')
    parser.add_argument('--output', type=str, default=None, help='Output YAML file path')
    parser.add_argument('--grammar', type=str, default=None, help='Path to ACE grammar file')
    parser.add_argument('--db', type=str, 
                       default="host=localhost user=postgres password=test1224! dbname=geuldev sslmode=disable",
                       help='PostgreSQL connection string')
    parser.add_argument('--batch-size', type=int, default=20,
                       help='Batch size for LLM pruning (default: 20)')
    parser.add_argument('--ollama-model', type=str, default='gpt-oss:20b',
                       help='Ollama model name (default: gpt-oss:20b)')
    parser.add_argument('--ollama-url', type=str, default='http://localhost:11434',
                       help='Ollama API URL (default: http://localhost:11434)')
    parser.add_argument('--no-prune', action='store_true',
                       help='Disable LLM pruning')
    
    parser.add_argument('--save-prompts', action='store_true',
                       help='Save prompts to files for debugging')
    parser.add_argument('--prompt-dir', type=str, default='sshg/prompt',
                       help='Directory to save prompts (default: sshg/prompt)')
    
    args = parser.parse_args()
    
    if args.output is None:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        args.output = f"mrs_{timestamp}.yaml"
    
    print(f"Parsing sentence: '{args.sentence}'")
    print(f"Batch size: {args.batch_size}")
    print(f"LLM pruning: {'disabled' if args.no_prune else f'enabled ({args.ollama_model})'}")
    
    # Initialize knowledge linker
    print("\nConnecting to knowledge bases...")
    try:
        linker = KnowledgeLinker(args.db)
        print("Successfully connected to database.")
    except Exception as e:
        print(f"Error connecting to database: {e}")
        print("Continuing without Wikidata linking (WordNet only)")
        linker = None
    
    # Initialize LLM pruner
    pruner = None
    if not args.no_prune:
        try:
            print(f"Initializing LLM pruner ({args.ollama_model})...")
            pruner = LLMPruner(
                model=args.ollama_model,
                ollama_url=args.ollama_url,
                save_prompts=args.save_prompts,
                prompt_dir=args.prompt_dir
            )
            print("LLM pruner initialized.")
        except Exception as e:
            print(f"Error initializing LLM pruner: {e}")
            print("Continuing without pruning.")
    
    try:
        parsing_start_time = time.perf_counter()
        # Parse to MRS
        mrs_list = parse_sentence_to_mrs_all(args.sentence, args.grammar)
        parsing_end_time = time.perf_counter()
        parsing_duration = parsing_end_time - parsing_start_time
        
        if not mrs_list:
            print("Failed to parse sentence.")
            return
        
        # Extract unique nodes (nouns and verbs separately)
        extraction_start_time = time.perf_counter()
        nouns_dict, verbs_dict = extract_unique_nodes(mrs_list)
        print(f"\nExtracted {len(nouns_dict)} unique noun nodes")
        print(f"Extracted {len(verbs_dict)} unique verb nodes")
        
        # Debug: print what was extracted
        if nouns_dict:
            print(f"Nouns: {list(nouns_dict.keys())}")
        if verbs_dict:
            print(f"Verbs: {list(verbs_dict.keys())}")
            
        extraction_end_time = time.perf_counter()
        extraction_duration = extraction_end_time - extraction_start_time
        
        # Link nodes to knowledge bases with pruning
        linking_start_time = time.perf_counter()
        if linker:
            noun_nodes = link_nodes_to_knowledge(
                nouns_dict, 'n', linker, pruner, args.sentence, args.batch_size
            )
            verb_nodes = link_nodes_to_knowledge(
                verbs_dict, 'v', linker, pruner, args.sentence, args.batch_size
            )
        else:
            print("Skipping knowledge linking due to database connection failure.")
            # Still create node entries without knowledge links
            noun_nodes = [{'lemma': data['lemma'], 'sources': data['sources'], 'wikidata': [], 'wordnet': []} 
                         for data in nouns_dict.values()]
            verb_nodes = [{'lemma': data['lemma'], 'sources': data['sources'], 'wordnet': []} 
                         for data in verbs_dict.values()]
        
        linking_end_time = time.perf_counter()
        linking_duration = linking_end_time - linking_start_time
        
        # Save to YAML
        save_start_time = time.perf_counter()
        save_all_mrs_to_yaml(mrs_list, noun_nodes, verb_nodes, args.output, args.sentence)
        save_end_time = time.perf_counter()
        save_duration = save_end_time - save_start_time
        
        # Summary
        print(f"\n=== MRS Summary ===")
        print(f"Number of interpretations: {len(mrs_list)}")
        for i, mrs_obj in enumerate(mrs_list):
            print(f"\nParse {i}:")
            print(f"  Top: {mrs_obj.top}")
            print(f"  Index: {mrs_obj.index}")
            print(f"  Relations: {len(mrs_obj.rels)}")
            
            # Count content predicates
            content_predicates = [ep for ep in mrs_obj.rels if ep.predicate.startswith('_')]
            print(f"  Content predicates: {len(content_predicates)}")
    
    finally:
        if linker:
            linker.close()

    main_end_time = time.perf_counter()
    main_duration = main_end_time - main_start_time

    print("\n=== Execution Time Summary ===")
    print(f"  1. MRS Parsing: {parsing_duration:.4f} seconds")
    print(f"  2. Node Extraction: {extraction_duration:.4f} seconds")
    print(f"  3. Knowledge Linking + Pruning: {linking_duration:.4f} seconds")
    print(f"  4. YAML Save: {save_duration:.4f} seconds")
    print(f"-----------------------------------")
    print(f"  Total Execution Time: {main_duration:.4f} seconds")


if __name__ == '__main__':
    main()