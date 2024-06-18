import stanza
import pandas as pd

sample = pd.read_csv("../../data/sampling/FAA_sample_100.csv")

nlp = stanza.Pipeline(lang='en', processors='tokenize,ner')

out_dict = {'index':[], 'c5_unique_id':[], 'c119_text':[], 'entities':[], 'labels':[]}

for index in range(len(sample)):
    text = sample['c119'][index]
    ents = nlp(text).ents
    for ent in ents:
        out_dict['index'].append(sample['Unnamed: 0'][index])
        out_dict['c5_unique_id'].append(sample['c5'][index])
        out_dict['c119_text'].append(sample['c119'][index])
        out_dict['entities'].append(ent.text)
        out_dict['labels'].append(ent.type)

print(pd.DataFrame(out_dict))

pd.DataFrame(out_dict).to_csv("../../data/results/stanza/stanza_ner.csv", index=False)