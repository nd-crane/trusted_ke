import sys
sys.path.append('./BLINK')
from blink import ner as NER
import json
import pandas as pd
import nltk

## Copied from main_dense.py, added idoc to arguments and line 26
def _annotate(ner_model, input_sentences, idoc, c5):
    ner_output_data = ner_model.predict(input_sentences)
    sentences = ner_output_data["sentences"]
    mentions = ner_output_data["mentions"]
    samples = []
    for mention in mentions:
        record = {}
        record["label"] = "unknown"
        record["label_id"] = -1
        # LOWERCASE EVERYTHING !
        record["context_left"] = sentences[mention["sent_idx"]][
            : mention["start_pos"]
        ].lower()
        record["context_right"] = sentences[mention["sent_idx"]][
            mention["end_pos"] :
        ].lower()
        record["mention"] = mention["text"].lower()
        record["start_pos"] = int(mention["start_pos"])
        record["end_pos"] = int(mention["end_pos"])
        record["sent_idx"] = mention["sent_idx"]
        record["doc_idx"] = idoc
        record["c5_id"] = c5
        samples.append(record)
    return samples

if __name__=="__main__":
    
    data = pd.read_csv("../../OMIn_dataset/data/FAA_data/Maintenance_Text_data_nona.csv")
    text = list(data["c119"])
    
    # initialize jsonl_output
    jsonl_output = []
            
    # Load NER model
    ner_model = NER.get_model()
    
    for idoc, doc in enumerate(text):
        
        # Split into seperate sentences if necessary
        sentences = nltk.sent_tokenize(doc)
            
        # annotate
        samples = _annotate(ner_model, sentences, idoc, data['c5'].iat[idoc])
        
        jsonl_output.extend(samples)
    
    with open("./faa_samples.jsonl", "w") as json_file:
        json_file.write(json.dumps(jsonl_output[0]))
        for line in jsonl_output[1:]:
            json_file.write('\n'+json.dumps(line))