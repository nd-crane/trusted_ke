# Code taken from https://fouadroumieh.medium.com/nlp-entity-extraction-ner-using-python-nltk-68649e65e54b

import nltk
import pandas as pd

# Download necessary NLTK data packages
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('maxent_ne_chunker')
nltk.download('words')

sample = pd.read_csv("../../data/sampling/FAA_sample_100.csv")

out_dict = {'index':[], 'c5_unique_id':[], 'c119_text':[], "entities":[], "POS tags":[], "labels":[]}

for index in range(len(sample)):
    
    text = sample["c119"][index]
    
    tokens = nltk.word_tokenize(text)
    tagged_tokens = nltk.pos_tag(tokens)
    chunked = nltk.ne_chunk(tagged_tokens)
    entities = []
    for tree in chunked.subtrees():
        if tree.label() == "S":
            continue
        out_dict["index"].append(sample['Unnamed: 0'][index])
        out_dict["c5_unique_id"].append(sample["c5"][index])
        out_dict["c119_text"].append(text)
        out_dict["entities"].append(' '.join([pair[0] for pair in tree.leaves()]))
        out_dict["POS tags"].append(', '.join([pair[1] for pair in tree.leaves()]))
        out_dict["labels"].append(tree.label())

print(pd.DataFrame(out_dict))

pd.DataFrame(out_dict).to_csv("../../data/results/nltk/nltk_ner_uppercased.csv", index=False)

###

out_dict = {'index':[], 'c5_unique_id':[], 'c119_text':[], "entities":[], "POS tags":[], "labels":[]}

for index in range(len(sample)):
    
    text = sample["c119"][index].lower()
    
    tokens = nltk.word_tokenize(text)
    tagged_tokens = nltk.pos_tag(tokens)
    chunked = nltk.ne_chunk(tagged_tokens)
    entities = []
    for tree in chunked.subtrees():
        if tree.label() == "S":
            continue
        out_dict["index"].append(sample['Unnamed: 0'][index])
        out_dict["c5_unique_id"].append(sample["c5"][index])
        out_dict["c119_text"].append(text)
        out_dict["entities"].append(' '.join([pair[0] for pair in tree.leaves()]))
        out_dict["POS tags"].append(', '.join([pair[1] for pair in tree.leaves()]))
        out_dict["labels"].append(tree.label())

print(pd.DataFrame(out_dict))

pd.DataFrame(out_dict).to_csv("../../data/results/nltk/nltk_ner_lowercased.csv", index=False)