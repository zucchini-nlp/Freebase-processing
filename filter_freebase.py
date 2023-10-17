import gzip
import pickle


in_file = "freebase-latest.gz"
out_file = "freebase-filtered.gz"

datatype_string = {}
datatype_string["type.int"] = "<http://www.w3.org/2001/XMLSchema#integer>"
datatype_string["type.float"] = "<http://www.w3.org/2001/XMLSchema#float>"
datatype_string["type.boolean"] = "<http://www.w3.org/2001/XMLSchema#boolean>"


ENTITY_GET_LABEL = [
    b'<http://rdf.freebase.com/ns/type.object.name>', 
    b'<http://rdf.freebase.com/ns/common.topic.alias>',
    b'<http://rdf.freebase.com/key/en>',
    b'<http://rdf.freebase.com/key/wikipedia.en>',
    b'<http://rdf.freebase.com/key/wikipedia.en_title>',
    b'<http://www.w3.org/2000/01/rdf-schema#label>'
    ]

LBL_DESCR_LANG_ID = [b'<http://www.w3.org/2000/01/rdf-schema#label>',  b'<http://rdf.freebase.com/ns/type.object.name>', b'<http://rdf.freebase.com/ns/common.topic.description>']

PREDICATES_TYPEOBJECT = [
    b'<http://rdf.freebase.com/ns/type.object.key>',
    b'<http://rdf.freebase.com/ns/type.object.id>',
    b'<http://rdf.freebase.com/ns/type.object.permission>'
    ]

PREDICATE_START_UNNECESARRY = [
    b'<http://rdf.freebase.com/key',
    b'<http://rdf.freebase.com/dataworld',
    b'<http://rdf.freebase.com/freebase',
    b'<http://rdf.freebase.com/user',
    b'<http://rdf.freebase.com/base',
    b'<http://rdf.freebase.com/common',
    b'<http://www.w3.org/1999/02/22-rdf-syntax-ns'
    ]


type_map = {}
with open("numeric_properties.txt", "r") as f_in:
    for line in f_in:
        line = line.strip()
        pred, type = line.split("\t")
        type_map[pred] = datatype_string[type]


f_in = gzip.open(in_file, "r")
f_out = gzip.open(out_file, "w")

line_num = added = 0
for line in f_in:
    line_num += 1
    if line_num % 1000000 == 0:
        print(line_num)

    if not line:
        continue

    subj, pred, obj, rest = line.split(b"\t")

    if any([(pred.startswith(start) and pred not in ENTITY_GET_LABEL) for start in PREDICATE_START_UNNECESARRY]):
        continue
    if any([pred.startswith(typeobj) for typeobj in PREDICATES_TYPEOBJECT]):
        continue
    if pred in LBL_DESCR_LANG_ID and not obj.endswith(b'@en'):
        continue

    pred_t = pred[pred.rfind(b"/")+1:len(pred)-1]
    try:
        datatype_string = type_map[pred_t]
        if b"^^" in obj:
          pass
        else:
            if b"\"" in obj:
                obj = obj + b"^^" + datatype_string
            else:
                obj = b"\"" + obj + b"\"^^" + datatype_string
            line = b"\t".join([subj, pred, obj, rest])
    except:
        pass
    f_out.write(line)
    added += 1

print(f"Added: {added} triplets")
f_in.close()
f_out.close()
