import gzip
import pickle

in_file = "freebase-filtered.gz"

# We need entity-id, label, descr, num outgoing rels, tag, wiki_page

ENTITY_GET_LABEL = [
    b'<http://rdf.freebase.com/ns/type.object.name>', 
    b'<http://rdf.freebase.com/ns/common.topic.alias>',
    b'<http://rdf.freebase.com/key/en>',
    b'<http://rdf.freebase.com/key/wikipedia.en>',
    b'<http://rdf.freebase.com/key/wikipedia.en_title>',
    b'<http://www.w3.org/2000/01/rdf-schema#label>'
    ]

WIKI_PAGE_TITLE = [
    b'<http://rdf.freebase.com/key/wikipedia.en>',
    b'<http://rdf.freebase.com/key/wikipedia.en_title>', 
]

TYPE_PRED = b"http://rdf.freebase.com/ns/type.object.type"
ENTITY_GET_DESCRIPTION = [b'<http://rdf.freebase.com/ns/common.topic.description>']


f_in = gzip.open(in_file, "r")

line_num = 0
curr_ent = ''
curr_ent_triplets = 0
curr_element = {"subj_mid": "", "label": "", "descr": "", "num_rels": 0, "tag": "", "page": ""}

entities_info = []

for line in f_in:
    line_num += 1
    if line_num % 1000000 == 0:
        print(line_num)
    
    subj, pred, obj, rest = line.split(b"\t")
    if not subj.startswith(b"<http://rdf.freebase.com/ns/m."):
        continue

    if curr_ent == subj:
        curr_ent_triplets += 1
        if pred in ENTITY_GET_LABEL:
            curr_element['label'] = str(obj).strip("<>")
        if pred in WIKI_PAGE_TITLE:
            curr_element['page'] = str(obj).strip("<>")
        if pred in ENTITY_GET_DESCRIPTION:
            curr_element['descr'] = str(obj).strip("<>")
        if pred == TYPE_PRED and obj != b"<http://rdf.freebase.com/ns/common.topic>":
            curr_element['tag'] = str(obj[subj.rfind(b"/"): ].strip(b"<>"))
    else:
        if curr_ent_triplets > 10:
            curr_element['num_rels'] = curr_ent_triplets
            entities_info.append({curr_element['subj_mid']: curr_element})
        curr_ent = subj
        curr_ent_triplets = 1
        subj_mid = str(subj[subj.rfind(b"/"): ].strip(b"<>"))
        curr_element = {"subj_mid": subj_mid, "label": "", "descr": "", "num_rels": 0, "tag": "", "page": ""}
    
print(f"Added: {len(entities_info)} entities")
f_in.close()


entities_file = "ent2info.pickle"
with open(entities_file, "wb") as f:
    pickle.dump(entities_info, f)