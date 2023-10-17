from lupyne import engine
import time
import pickle
import lucene
assert lucene.getVMEnv() or lucene.initVM()

indexer = engine.Indexer('freebase_entities_index')

indexer.set('label', engine.Field.Text, stored=True)
indexer.set('entity_id', stored=True)
indexer.set('num_rels', stored=True)
indexer.set('tag', stored=True)
indexer.set('page', stored=True)
indexer.set('descr', stored=True)

with open("ent2info.pickle", "rb") as f:
    entities_info = pickle.load(f)

# I also got the wikidata to freebase mapping to have more entities with descriptions/labels
with open("ent2info_wdmap.pickle", "rb") as f:
    entities_info_wd = pickle.load(f)

entities_info_dict = {}
for el in (entities_info + entities_info_wd):
    entities_info_dict.update(el)

added, cnt = 0, 0
for mid in entities_info_dict:
    if mid and mid.startswith("m."):
        curr_element = entities_info_dict[mid]
        mid = mid[1:]
        label = curr_element["label"]
        label_clean = label.replace("'s", " ").replace("'", "").lower().replace("-", " ").replace("@en", "").replace("  ", " ").replace(".", "").replace("\"", "").lower()
        if len(label_clean) > 1:
            label_clean_split = label_clean.split()

            if curr_element["num_rels"] > 10:
                descr = curr_element['descr'].replace("'s", " ").replace("'", "").replace("-", " ").replace("@en", "").replace("\t", " ").replace("\n", " ").replace("  ", " ").replace("\"", "")
                page = curr_element["page"].replace("'s", " ").replace("'", "").replace("-", " ").replace("@en", "").replace("  ", " ").replace("\"", "")
                tag = curr_element["tag"].strip("/").split(".")[0] # get the first topic of the tag
                indexer.add(label=label_clean, entity_id=mid, num_rels=curr_element["num_rels"], tag=tag, page=page, descr=descr)
                added += 1        
    cnt += 1
    if cnt % 1000000 == 0:
        print(f"Processed elelments: {cnt}, added: {added}")


print('Started commiting, this may take a while...')
indexer.commit()
print("finished")
