import pandas as pd
import spacy

nlp = spacy.load("en_core_web_sm")

sample = pd.read_csv("../../data/sampling/FAA_sample_100.csv")

out_dict = {'index':[], 'c5_unique_id':[], 'c119_text':[], 'entities':[], 'labels':[]}

for index in range(len(sample)):
    text = sample['c119'][index]
    ents = nlp(text).ents
    if len(ents) == 0:
        ents = ("")     # still want to create an entry in the final sheet, but leave entity column empty
    for ent in ents:
        out_dict['index'].append(sample['Unnamed: 0'][index])
        out_dict['c5_unique_id'].append(sample['c5'][index])
        out_dict['c119_text'].append(sample['c119'][index])
        out_dict['entities'].append(ent.text)
        out_dict['labels'].append(ent.label_)

print(pd.DataFrame(out_dict))

pd.DataFrame(out_dict).to_excel("spacy_ner.xlsx", index=False)