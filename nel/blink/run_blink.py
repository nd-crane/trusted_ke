import pandas as pd
import argparse
import json
import re
import requests
import sys
sys.path.append("./BLINK")
import blink.candidate_ranking.utils as utils
from main_dense import load_models, run

def lookup(url, qiddict):
    
    qidp = re.compile(r'.*id="t-wikibase" class="mw-list-item"><a href="https://www.wikidata.org/wiki/Special:EntityPage/(Q\d*)".*')

    content = str(requests.get(url).content)
    mo = re.match(qidp, content)

    if mo:
        QID = mo.groups()[0]
    else:
        QID = url
        
    qiddict.update({url:QID})
            
    return QID, qiddict

models_path = "BLINK/models/" # the path where you stored the BLINK models
annotated_samples_path = "./faa_samples.jsonl"

config = {
    "test_entities": None,
    "test_mentions": annotated_samples_path,
    "interactive": False,
    "top_k": 10,
    "biencoder_model": models_path+"biencoder_wiki_large.bin",
    "biencoder_config": models_path+"biencoder_wiki_large.json",
    "entity_catalogue": models_path+"entity.jsonl",
    "entity_encoding": models_path+"all_entities_large.t7",
    "crossencoder_model": models_path+"crossencoder_wiki_large.bin",
    "crossencoder_config": models_path+"crossencoder_wiki_large.json",
    "fast": False,
    "output_path": "./BLINK/logs/" # logging directory
}

args = argparse.Namespace(**config)

logger = utils.get_logger(args.output_path)

models = load_models(args, logger)

title2id = models[5]
id2title = models[6]
id2text = models[7]
wikipedia_id2local_id = models[8]

id2url = {
        v: "https://en.wikipedia.org/wiki?curid=%s" % k
        for k, v in wikipedia_id2local_id.items()
    }

# Get test data
with open("./faa_samples.jsonl") as f:
    jsonl_data = f.read()

samples = []
for json_str in jsonl_data.split('\n'):
    samples.append(json.loads(json_str))

## Crossencoder predictions
result = run(args, logger, *models, test_data=samples)
crossencoder_predictions = result[5]


## Biencoder predictions -- change fast to True
args.fast = True
result = run(args, logger, *models, test_data=samples)
biencoder_predictions = result[5]

## Store results
og_data = pd.read_csv("../../OMIn_dataset/data/FAA_data/Maintenance_Text_data_nona.csv")

results_dict = {"doc_idx":[], "c5_id":[], "sent_idx":[], "original_sentence":[], "input":[], "mentions":[], "bi_pred_entity":[], "bi_qid":[], "bi_desc":[], "cross_pred_entity":[], "cross_qid":[],"cross_desc":[]}

url2qid = {} # stores each looked-up qid for faster referencing later

for isample, sample in enumerate(samples):
    
    results_dict["doc_idx"].append(sample["doc_idx"])
    results_dict["c5_id"].append(sample["c5_id"])
    results_dict["sent_idx"].append(sample["sent_idx"])
    results_dict["original_sentence"].append(og_data["c119"].iat[sample["doc_idx"]])
    results_dict["input"].append(''.join([sample["context_left"], sample["mention"], sample["context_right"]]))
    results_dict["mentions"].append(sample["mention"])
    
    # Biencoder
    entity = biencoder_predictions[isample][0] # just taking top one
    entity_id = title2id[entity]
    url = id2url[entity_id]
    desc = id2text[entity_id]

    if url in url2qid:
        qid = url2qid[url]
    else:
        qid, url2qid = lookup(url, url2qid)

    results_dict["bi_pred_entity"].append(entity)
    results_dict["bi_qid"].append(qid)
    results_dict["bi_desc"].append(desc)

    # Crossencoder:
    entity = crossencoder_predictions[isample][0]
    entity_id = title2id[entity]
    url = id2url[entity_id]
    desc = id2text[entity_id]

    if url in url2qid:
        qid = url2qid[url]
    else:
        qid, url2qid = lookup(url, url2qid)

    results_dict["cross_pred_entity"].append(entity)
    results_dict["cross_qid"].append(qid)
    results_dict["cross_desc"].append(desc)
    
pd.DataFrame(results_dict).to_csv("../../tool_results/blink/blink_results.csv", index=False)