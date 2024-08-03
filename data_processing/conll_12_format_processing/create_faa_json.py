#Putting the FAA data into json format since we write format_conll.py to accept json data
#Each entry is a seperate document with one part only, and the documents are labeled with ids constructed as: "faa/{index in csv data}_{c5 unique ID}"

import json
import pandas as pd
import re

faa_data = pd.read_csv("../../data/FAA_data/Maintenance_Text_data_nona.csv")

docs = [[entry] for entry in faa_data["c119"]]

# (FAA data often omits whitespace between sentences)
for idoc, doc in enumerate(docs):
    for ipart, part in enumerate(doc):
        part = part.lower()
        part = re.sub(r'([^0-9])\.([^0-9])', r'\1. \2', part) # often no space between sentences, add space after period
        part = re.sub(r'\.([^0-9])', r'. \1', part) # often no space between sentences, add space after period
        
        docs[idoc][ipart] = part

doc_ids = [f"faa/{no}_{id}" for no, id in enumerate(list(faa_data["c5"]))]

json_data = {doc_ids[idoc]:docs[idoc] for idoc in range(len(docs))}

with open("./faa.json", 'w') as json_file:
    json.dump(json_data, json_file, indent=4)