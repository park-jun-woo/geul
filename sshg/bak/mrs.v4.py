#!/usr/bin/env python3
"""
MRS Parser with Knowledge Linking
Parses sentences to MRS, links to Wikidata and WordNet, saves as YAML
"""

import time
import argparse
import yaml
import psycopg2
import hashlib
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


class KnowledgeLinker:
    """Links MRS predicates to Wikidata and WordNet"""
    
    def __init__(self, conn_str):
        self.conn = psycopg2.connect(conn_str)
        
    def search_wikidata(self, lemma, limit=10):
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
                # Skip entries with empty descriptions (no information for GPT)
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

            if not entity_ids:
                cursor.close()
                return candidates

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
    
    def search_wordnet(self, lemma, pos=None, max_synsets=None):
        """
        Search WordNet for synsets
        Only returns synsets where the lemma exactly matches
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
                    continue  # Skip synsets where the lemma doesn't match
                
                candidates.append({
                    'synset': synset.name(),
                    'definition': synset.definition()
                })
                
                # Apply limit if specified
                if max_synsets is not None and len(candidates) >= max_synsets:
                    break
            
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


def extract_verb_arg_structures(mrs_list: list, lemma: str) -> list:
    """
    Extract ARG structures for a specific verb lemma from all parses
    Returns list of arg structures: [{'has_arg2': bool, 'arg2_type': 'entity'/'handle'/None, 'has_arg3': bool}, ...]
    """
    arg_structures = []
    
    for mrs_obj in mrs_list:
        for ep in mrs_obj.rels:
            # Match predicates for this lemma
            if not ep.predicate.startswith('_'):
                continue
            
            parts = ep.predicate[1:].split('_')
            if len(parts) < 2:
                continue
            
            pred_lemma = parts[0]
            pred_pos = parts[1]
            
            if pred_lemma == lemma and pred_pos == 'v':
                # Extract ARG structure
                args = ep.args
                
                structure = {
                    'has_arg2': 'ARG2' in args,
                    'arg2_type': None,
                    'has_arg3': 'ARG3' in args
                }
                
                if structure['has_arg2']:
                    arg2_value = str(args['ARG2'])
                    # Determine type: handle (h) or entity (x/e)
                    if arg2_value.startswith('h'):
                        structure['arg2_type'] = 'handle'
                    elif arg2_value.startswith('x') or arg2_value.startswith('e'):
                        structure['arg2_type'] = 'entity'
                
                arg_structures.append(structure)
    
    return arg_structures


def frame_matches_structure(frame_id: int, structure: dict) -> bool:
    """
    Check if a WordNet frame ID matches an MRS ARG structure
    """
    # Frame 1: Intransitive (no ARG2)
    if frame_id == 1:
        return not structure['has_arg2']
    
    # Frames 2, 8: Transitive with entity object (ARG2 = entity)
    elif frame_id in [2, 8]:
        return structure['has_arg2'] and structure['arg2_type'] == 'entity'
    
    # Frame 9, 13: Ditransitive (ARG2 + ARG3)
    elif frame_id in [9, 13]:
        return structure['has_arg2'] and structure['has_arg3']
    
    # Frame 11: Gerund (ARG2 = handle for V-ing)
    elif frame_id == 11:
        return structure['has_arg2'] and structure['arg2_type'] == 'handle'
    
    # Frames 15, 22, 23, 25: Various prepositional patterns (need ARG2)
    elif frame_id in [15, 22, 23, 25]:
        return structure['has_arg2'] and structure['arg2_type'] == 'entity'
    
    # Frame 26: That-clause (ARG2 = handle)
    elif frame_id == 26:
        return structure['has_arg2'] and structure['arg2_type'] == 'handle'
    
    # Frame 29, 30: Control structures (ARG2 + handle)
    elif frame_id in [29, 30]:
        return structure['has_arg2'] and structure['arg2_type'] in ['entity', 'handle']
    
    # Default: allow if conservative (assume compatible)
    else:
        return True


def is_synset_compatible(synset_name: str, arg_structures: list) -> bool:
    """
    Check if synset is compatible with at least one parse structure
    """
    try:
        synset = wn.synset(synset_name)
        frame_ids = synset.frame_ids()
        
        # If no frame info, keep it (conservative)
        if not frame_ids:
            return True
        
        # Check if any frame matches any structure
        for frame_id in frame_ids:
            for structure in arg_structures:
                if frame_matches_structure(frame_id, structure):
                    return True
        
        return False
    
    except Exception as e:
        print(f"Warning: Error checking synset compatibility for '{synset_name}': {e}")
        return True  # Conservative: keep on error


def filter_verb_synsets(synsets: list, lemma: str, mrs_list: list) -> tuple:
    """
    Filter verb synsets based on frame compatibility with parse structures
    Returns: (filtered_synsets, stats)
    """
    # Extract all ARG structures for this verb from all parses
    arg_structures = extract_verb_arg_structures(mrs_list, lemma)
    
    if not arg_structures:
        return synsets, {'original': len(synsets), 'filtered': len(synsets), 'removed': 0}
    
    # Filter synsets
    filtered = []
    for synset_data in synsets:
        synset_name = synset_data['synset']
        if is_synset_compatible(synset_name, arg_structures):
            filtered.append(synset_data)
    
    stats = {
        'original': len(synsets),
        'filtered': len(filtered),
        'removed': len(synsets) - len(filtered)
    }
    
    return filtered, stats


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


def link_nodes_to_knowledge(nodes: dict, pos: str, linker: KnowledgeLinker, 
                            mrs_list: list = None, max_synsets: int = None, max_qids: int = 10) -> list:
    """
    Link all nodes to knowledge bases (Wikidata and WordNet)
    Args:
        nodes: dict with key=lemma, value={'lemma': str, 'sources': [...]}
        pos: 'n' or 'v'
        mrs_list: list of MRS objects (for verb frame filtering)
        max_synsets: maximum WordNet synsets per lemma (None for unlimited)
        max_qids: maximum Wikidata QIDs per lemma
    Returns: list of nodes with knowledge links
    """
    print(f"\n=== Linking {len(nodes)} {pos} nodes to knowledge bases ===")
    
    linked_nodes = []
    
    for lemma, node_data in nodes.items():
        print(f"Linking: {lemma} ({pos})")
        
        # Search WordNet for both nouns and verbs
        wordnet_candidates = linker.search_wordnet(lemma, pos, max_synsets)
        original_count = len(wordnet_candidates)
        print(f"  -> WordNet: {original_count} synsets (before filtering)")
        
        # For verbs, filter by frame compatibility
        if pos == 'v' and mrs_list:
            wordnet_candidates, filter_stats = filter_verb_synsets(
                wordnet_candidates, lemma, mrs_list
            )
            print(f"  -> Frame filtering: kept {filter_stats['filtered']}/{filter_stats['original']}, removed {filter_stats['removed']}")
        
        # Only search Wikidata for nouns (entities)
        if pos == 'n':
            wikidata_candidates = linker.search_wikidata(lemma, max_qids)
            print(f"  -> Wikidata: {len(wikidata_candidates)} candidates")
            # Create node entry
            node_entry = {
                'lemma': lemma,
                'sources': node_data['sources'],
                'wikidata': wikidata_candidates,
                'wordnet': wordnet_candidates
            }
        else:
            print(f"  -> Wikidata: skipped (verbs not in Wikidata)")
            # Create node entry
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
    """Save all MRS with knowledge links to YAML (simplemrs removed)"""
    
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
            'num_parses': len(mrs_list),
            'num_noun_nodes': len(noun_nodes),
            'num_verb_nodes': len(verb_nodes),
            'note': 'Pruned: Wikidata for nouns, empty descriptions removed, verb synsets filtered by frame compatibility, examples/lemmas removed, simplemrs removed'
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
        description='Parse sentence to MRS with knowledge linking (Wikidata + WordNet)'
    )
    parser.add_argument('--sentence', type=str, required=True, help='Input sentence to parse')
    parser.add_argument('--output', type=str, default=None, help='Output YAML file path')
    parser.add_argument('--grammar', type=str, default=None, help='Path to ACE grammar file')
    parser.add_argument('--db', type=str, 
                       default="host=localhost user=postgres password=test1224! dbname=geuldev sslmode=disable",
                       help='PostgreSQL connection string')
    parser.add_argument('--max-synsets', type=int, default=None,
                       help='Maximum WordNet synsets per lemma (default: unlimited)')
    parser.add_argument('--max-qids', type=int, default=10,
                       help='Maximum Wikidata QIDs per lemma (default: 10)')
    
    args = parser.parse_args()
    
    if args.output is None:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        args.output = f"mrs_{timestamp}.yaml"
    
    print(f"Parsing sentence: '{args.sentence}'")
    print(f"Max synsets: {'unlimited' if args.max_synsets is None else args.max_synsets}")
    print(f"Max QIDs: {args.max_qids}")
    
    # Initialize knowledge linker
    print("Connecting to knowledge bases...")
    try:
        linker = KnowledgeLinker(args.db)
        print("Successfully connected to database.")
    except Exception as e:
        print(f"Error connecting to database: {e}")
        print("Continuing without Wikidata linking (WordNet only)")
        linker = None
    
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
        
        # Link nodes to knowledge bases
        linking_start_time = time.perf_counter()
        if linker:
            noun_nodes = link_nodes_to_knowledge(nouns_dict, 'n', linker, 
                                                 max_synsets=args.max_synsets, max_qids=args.max_qids)
            verb_nodes = link_nodes_to_knowledge(verbs_dict, 'v', linker, mrs_list,
                                                 max_synsets=args.max_synsets, max_qids=args.max_qids)
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
    print(f"  3. Knowledge Linking: {linking_duration:.4f} seconds")
    print(f"  4. YAML Save: {save_duration:.4f} seconds")
    print(f"-----------------------------------")
    print(f"  Total Execution Time: {main_duration:.4f} seconds")


if __name__ == '__main__':
    main()