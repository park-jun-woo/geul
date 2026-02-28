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
from delphin.codecs import simplemrs
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
        
    def search_wikidata(self, lemma, limit=5):
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
                candidates.append({
                    'qid': qid,
                    'label': label,
                    'description': description or '',
                    'source': 'label'
                })
        
        # Also search aliases if we have few results
        # Use hash index since alias field is too large for B-Tree
        if len(candidates) < limit:

            # 1단계: alias 테이블에서 entity_id 목록만 빠르게 조회
            alias_to_id_query = """
            SELECT entity_id FROM entity_aliases
            WHERE md5(alias) = %s AND language = 'en'
            LIMIT %s;
            """
            
            lemma_hash = hashlib.md5(lemma.encode('utf-8')).hexdigest()
            
            cursor.execute(alias_to_id_query, (lemma_hash, limit - len(candidates)))
            
            # 조회된 entity_id들을 리스트로 만듭니다.
            entity_ids = [row[0] for row in cursor.fetchall()]

            # 만약 찾은 id가 없다면, 여기서 종료
            if not entity_ids:
                cursor.close()
                return candidates

            # 2단계: 찾아낸 entity_id 목록을 이용해 나머지 정보 조회
            # WHERE e.id = ANY(%s)는 WHERE e.id IN (...) 와 유사하며, psycopg2에서 리스트를 넘기기 좋은 방식입니다.
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
                # Avoid duplicates
                if not any(c['qid'] == qid for c in candidates):
                    candidates.append({
                        'qid': qid,
                        'label': label, # 여기서는 alias가 아닌 대표 라벨(label)을 사용
                        'description': description or '',
                        'source': 'alias' # 출처는 alias가 맞음
                    })
        
        cursor.close()
        return candidates
    
    def search_wordnet(self, lemma, pos=None):
        """
        Search WordNet for synsets
        pos: 'n', 'v', 'a', 'r' or None for all
        """
        # Convert MRS POS to WordNet POS
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
                candidates.append({
                    'synset': synset.name(),
                    'definition': synset.definition(),
                    'examples': synset.examples()[:2],  # First 2 examples
                    'lemmas': [l.name() for l in synset.lemmas()[:5]]
                })
            
            return candidates
        except Exception as e:
            print(f"WordNet error for '{lemma}': {e}")
            return []
    
    def link_predicate(self, predicate_str):
        """
        Link a single MRS predicate to knowledge bases
        
        predicate_str: e.g., "_seoul_n_1", "_bark_v_1"
        Returns: dict with wikidata and wordnet candidates
        """
        # Parse predicate
        if not predicate_str.startswith('_'):
            return {'wikidata': [], 'wordnet': []}
        
        parts = predicate_str[1:].split('_')
        if len(parts) < 2:
            return {'wikidata': [], 'wordnet': []}
        
        lemma = parts[0]
        pos = parts[1] if len(parts) > 1 else None
        
        # Skip very common/generic predicates to reduce noise
        skip_predicates = ['the', 'a', 'an', 'be', 'have', 'do']
        if lemma in skip_predicates:
            return {'wikidata': [], 'wordnet': []}
        
        # Search both knowledge bases
        wikidata_candidates = self.search_wikidata(lemma)
        wordnet_candidates = self.search_wordnet(lemma, pos)
        
        return {
            'lemma': lemma,
            'pos': pos,
            'wikidata': wikidata_candidates,
            'wordnet': wordnet_candidates
        }
    
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
            
            # Filter out parses with 'unknown' predicates
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


def mrs_to_dict_with_links(mrs_obj: MRS, linker: KnowledgeLinker) -> dict:
    """Convert MRS to dict and add knowledge links"""
    
    mrs_dict = {
        'top': mrs_obj.top,
        'index': mrs_obj.index,
        'rels': [],
        'hcons': [],
        'icons': []
    }
    
    # Process predicates and add knowledge links
    for ep in mrs_obj.rels:
        ep_dict = {
            'predicate': ep.predicate,
            'label': ep.label,
            'args': {}
        }
        
        # Arguments
        for role, value in ep.args.items():
            ep_dict['args'][role] = value
        
        # Knowledge linking for content predicates
        if ep.predicate.startswith('_'):
            print(f"  Linking: {ep.predicate}")
            knowledge_links = linker.link_predicate(ep.predicate)
            if knowledge_links['wikidata'] or knowledge_links['wordnet']:
                ep_dict['knowledge_links'] = knowledge_links
                print(f"    -> Wikidata: {len(knowledge_links['wikidata'])} candidates")
                print(f"    -> WordNet: {len(knowledge_links['wordnet'])} synsets")
        
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


def save_all_mrs_to_yaml(mrs_list: list, output_path: str, sentence: str, linker: KnowledgeLinker):
    """Save all MRS with knowledge links to YAML"""
    
    output_dir = Path(output_path).parent
    if output_dir and str(output_dir) != '.':
        output_dir.mkdir(parents=True, exist_ok=True)
        print(f"Created directory: {output_dir}")
    
    parses = []
    for i, mrs_obj in enumerate(mrs_list):
        print(f"\nProcessing parse {i}...")
        mrs_dict = mrs_to_dict_with_links(mrs_obj, linker)
        simplemrs_str = simplemrs.encode(mrs_obj)
        
        parse_entry = {
            'parse_id': i,
            'mrs': mrs_dict,
            'simplemrs': simplemrs_str
        }
        parses.append(parse_entry)
    
    output_data = {
        'metadata': {
            'timestamp': datetime.now().isoformat(),
            'sentence': sentence,
            'parser': 'ACE + ERG',
            'knowledge_bases': ['Wikidata', 'WordNet'],
            'num_parses': len(mrs_list),
            'note': 'Multiple interpretations with knowledge links'
        },
        'parses': parses
    }
    
    with open(output_path, 'w', encoding='utf-8') as f:
        yaml.dump(output_data, f, default_flow_style=False, allow_unicode=True, sort_keys=False)
    
    print(f"\nMRS saved to: {output_path}")
    print(f"Total parses saved: {len(mrs_list)}")


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
    
    args = parser.parse_args()
    
    if args.output is None:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        args.output = f"mrs_{timestamp}.yaml"
    
    print(f"Parsing sentence: '{args.sentence}'")
    
    # Initialize knowledge linker
    print("Connecting to knowledge bases...")
    try:
        linker = KnowledgeLinker(args.db)
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
        
        linking_start_time = time.perf_counter()
        # Save with knowledge links
        if linker:
            save_all_mrs_to_yaml(mrs_list, args.output, args.sentence, linker)
        else:
            print("Skipping knowledge linking due to database connection failure.")
        
        linking_end_time = time.perf_counter()
        linking_duration = linking_end_time - linking_start_time
        
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
    print(f"  2. Knowledge Linking & Save: {linking_duration:.4f} seconds")
    print(f"-----------------------------------")
    print(f"  Total Execution Time: {main_duration:.4f} seconds")

if __name__ == '__main__':
    main()