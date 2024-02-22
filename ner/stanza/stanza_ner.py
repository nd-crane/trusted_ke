import stanza
import pandas as pd

sample = pd.read_csv("../../data/sampling/FAA_sample_100.csv")

nlp = stanza.Pipeline(lang='en', processors='tokenize,ner')

out_dict = {'index':[], 'c5_unique_id':[], 'c119_text':[], 'stanza_ner_recd_ents':[]}

for index in range(len(sample)):
    text = sample['c119'][index]
    ents = nlp(text).ents
    if len(ents) == 0:
        ents = ("")     # still want to create an entry in the final sheet, but leave entity column empty
    for ent in ents:
        out_dict['index'].append(sample['Unnamed: 0'][index])
        out_dict['c5_unique_id'].append(sample['c5'][index])
        out_dict['c119_text'].append(sample['c119'][index])
        out_dict['stanza_ner_recd_ents'].append(ent.text)

pd.DataFrame(out_dict).to_excel("stanza_ner.xlsx", index=False)