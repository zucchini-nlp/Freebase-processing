import time
import argparse
from rapidfuzz import fuzz
from typing import List
from lupyne import engine
import lucene

assert lucene.getVMEnv() or lucene.initVM()

indexer = engine.Indexer('freebase_entities_index')

start = time.time()

def search_by_label(entities_list: List[str]):
    res = [[] for _ in range(len(entities_list))]
    for idx, term in enumerate(entities_list):
        hits = indexer.search(term, field='label')
        for hit in hits:
            res[idx].append((hit['entity_id'], hit["label"], hit["num_rels"], fuzz.ratio(hit['label'] term)))
    
    # sort by num_rels, then by levenshtein distance
    sorted_res = []
    for elements in res:
        sorted_list = sorted(elements, key=lambda x: (-x[2], -x[3]))
        sorted_res.append(sorted_list)
    print(f"total processing time: {round(time.time()-start, 3)}")
    return sorted_res


def search_by_mid(mid_list: List[str]):
    res = [[] for _ in range(len(mid_list))]
    for idx, term in enumerate(mid_list):
        hits = indexer.search(term, field='entity_id')
        for hit in hits:
            res[idx].append(hit['label'])

    print(f"total processing time: {round(time.time()-start, 3)}")
    return res


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--entities", type=str, required=True, help="entities to search, separated by semicolon")
    args = parser.parse_args()
    entities = [ent.strip() for ent in args.entities.split(";")]
    res = search_by_label(entities)
    for cand_list, search_term in zip(res, entities):
        print(f"Seacrhing {search_term} yielded top-3 results {cand_list[:3]}")