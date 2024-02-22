from flair.data import Sentence
from flair.nn import Classifier
import pandas as pd

sample = pd.read_csv("../../data/sampling/FAA_sample_100.csv")

out_dict = {'index':[], 'c5_unique_id':[], 'c119_text':[], 'entities':[], 'labels':[]}

tagger = Classifier.load('ner')

for index in range(len(sample)):
    text = sample['c119'][index]
    sentence = Sentence(text)
    tagger.predict(sentence)
    sent_dict = sentence.to_dict()
    if 'entities' not in sent_dict:
        print("err on ", sent_dict)
        continue
    ents = sent_dict['entities']
    
    if len(ents) == 0:
        ents = [{"text":"", "labels":""}]     # still want to create an entry in the final sheet, but leave entity column empty
    for ent in ents:
        out_dict['index'].append(sample['Unnamed: 0'][index])
        out_dict['c5_unique_id'].append(sample['c5'][index])
        out_dict['c119_text'].append(sample['c119'][index])
        out_dict['entities'].append(ent['text'])
        out_dict['labels'].append(ent['labels'])

print(pd.DataFrame(out_dict))

pd.DataFrame(out_dict).to_excel("flair_ner.xlsx", index=False)