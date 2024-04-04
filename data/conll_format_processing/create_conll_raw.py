### Recreating the original MSNBC file which is stored in conll format in conll_data, so that we can run format_conll.py on it, and check whether it puts it into conll format accurately

import re
import json

with open("conll_data/dev.english.v4_gold_conll") as f:
    conll_data = f.readlines()

docs = []
doc_ids = []
words = []
for line in conll_data:
    if "#begin document" in line:
        words = []
        # Find out whether same doc new part or new doc:
        mo = re.match(r"#begin document \((.*)\); part (\d+)", line)
        doc_id, part_no = mo.groups()
        if doc_id not in doc_ids:
            docs.append([])
            doc_ids.append(doc_id)
            
        
    elif "#end document" in line:
        docs[-1].append(' '.join(words))
    elif not line.isspace():
        columns = line.split()
        word = columns[3]
        word = re.sub("/","", word)
        words.append(word)


json_data = {doc_ids[idoc]:docs[idoc] for idoc in range(len(docs))}

with open("./conll_raw.json", 'w') as json_file:
    json.dump(json_data, json_file, indent=4)