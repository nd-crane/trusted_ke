from transformers import pipeline
import pandas as pd
import sys

# Function to parse the generated text and extract the triplets
def extract_triplets(text):
    triplets = []
    relation, subject, relation, object_ = '', '', '', ''
    text = text.strip()
    current = 'x'
    for token in text.replace("<s>", "").replace("<pad>", "").replace("</s>", "").split():
        if token == "<triplet>":
            current = 't'
            if relation != '':
                triplets.append({'head': subject.strip(), 'type': relation.strip(),'tail': object_.strip()})
                relation = ''
            subject = ''
        elif token == "<subj>":
            current = 's'
            if relation != '':
                triplets.append({'head': subject.strip(), 'type': relation.strip(),'tail': object_.strip()})
            object_ = ''
        elif token == "<obj>":
            current = 'o'
            relation = ''
        else:
            if current == 't':
                subject += ' ' + token
            elif current == 's':
                object_ += ' ' + token
            elif current == 'o':
                relation += ' ' + token
    if subject != '' and relation != '' and object_ != '':
        triplets.append({'head': subject.strip(), 'type': relation.strip(),'tail': object_.strip()})
    return triplets


triplet_extractor = pipeline('text2text-generation', model='Babelscape/rebel-large', tokenizer='Babelscape/rebel-large')

dataset = pd.read_csv('../../data/FAA_data/Maintenance_Text_data_nona.csv')

results_dict = {"index":[],"input":[], "head":[], "relation":[], "tail":[]}
for i in range(len(dataset)):
    text = dataset["c119"].iat[i]
    # We need to use the tokenizer manually since we need special tokens.
    extracted_text = triplet_extractor.tokenizer.batch_decode([triplet_extractor(text, return_tensors=True, return_text=False)[0]["generated_token_ids"]])

    extracted_triplets = extract_triplets(extracted_text[0])
    
    for triplet in extracted_triplets:
        results_dict["index"].append(i)
        results_dict["input"].append(text)
        results_dict["head"].append(triplet["head"])
        results_dict["relation"].append(triplet["type"])
        results_dict["tail"].append(triplet["tail"])
        #print(triplet)
        
    length = 50
    fill = "#"
    prefix = "Entries Processed:"
    suffix = ""
    percent = ("{0:.1f}").format(100 * (i / float(len(dataset))))
    filled_length = int(length * i // len(dataset))
    bar = fill * filled_length + '-' * (length - filled_length)
    sys.stdout.write(f'\r{prefix} |{bar}| {percent}% {suffix}', )
    sys.stdout.flush()
            
pd.DataFrame(results_dict).to_csv("../../data/FAA_data/rebel_results.csv")