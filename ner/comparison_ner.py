import pandas as pd

sample = pd.read_csv("../data/sampling/FAA_sample_100.csv")

flair = pd.read_excel("flair/flair_ner.xlsx")
nltk = pd.read_excel("nltk/nltk_ner_uppercased.xlsx")
spacy = pd.read_excel("spacy/spacy_ner.xlsx")
stanza = pd.read_excel("stanza/stanza_ner.xlsx")

dfs = {"flair":flair, "nltk":nltk, "spacy":spacy, "stanza":stanza}

out_dict = {'index':[], 'c5_unique_id':[], 'c119_text':[], 'flair_entities':[], 'flair_labels':[],\
            'nltk_entities':[], 'nltk_labels':[],\
            'spacy_entities':[], 'spacy_labels':[],\
            'stanza_entities':[], 'stanza_labels':[]}

for index in range(len(sample)):
    for tool, df in dfs.items():
        results = df[df["index"] == index]
        for iresult in range(len(results)):
            result = results.iloc[iresult]
            out_dict["index"].append(index)
            out_dict["c5_unique_id"].append(result["c5_unique_id"])
            out_dict["c119_text"].append(result["c119_text"])
            ent_results = {key : "" for key in dfs.keys()}
            label_results = {key : "" for key in dfs.keys()}
            ent_results[tool] = result["entities"]
            label_results[tool] = result["labels"]
            for key in dfs.keys():
                out_dict[f"{key}_entities"].append(ent_results[key])
                out_dict[f"{key}_labels"].append(label_results[key])

print(pd.DataFrame(out_dict))

pd.DataFrame(out_dict).to_excel("comparison_ner.xlsx", index=False)