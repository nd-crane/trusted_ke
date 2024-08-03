# Gold Standard data
The gold standard data is a subset of the [Complete Set of FAA data](../data/FAA_data/Maintenance_Text_data_nona.csv) created to evaluate the correctness of the tools regarding Named Entity Recognition (NER), Coreference Resolution (CR), Named Entity Linking (NEL) and Relation Extraction (RE) tasks.


## Gold Standard Preparation

The Gold Standard dataset is derived from a [selected random subset of 100 records](../data/FAA_data/FAA_sample_100.csv) from the [Complete Set of Processed FAA data](../data/FAA_data/Maintenance_Text_data_nona.csv).

The gold standard datasets were hand crafted by our team, following guidelines described in the [raw folder](raw/README.md). For those interested in the gold standard creation process, the raw result from our team, including notes, is available in the [raw folder](raw/), and the processed files are available in the [processed folder](processed/). The data preparation process, including the steps taken to create the Gold Standard dataset, is registered in the [process_gs.ipynb](process_gs.ipynb) notebook.


We have a gold standard for the each of following tasks:

- [Named Entity Recognition (NER)](processed/ner.csv)
- [Coreference Resolution (CR)](processed/cr.csv)
- [Named Entity Linking (NEL)](processed/nel.csv)


## NER Gold Standards

1. processed/ner.csv - The unlabeled set of entities developed by our team, considering important information for maintenance
2. processed/ner_conll.csv - Set of entities with labels found following CoNLL-2003 annotation guidelines
3. processed/ner_ace.csv - Set of entities with labels found following ACE-2005 annotation guidelines
4. processed/ner_ace_nltk.csv - processed/ner_ace.csv without VEHICLE (or WEAPON) entities - based on the set of entity types used in ACE-Phase-1, which is what NLTK recognizes
5. processed/ner_on.csv - Set of entities with labels found following OntoNotes annotation guidelines

**Overlap between NER Gold Standards:**

Total refers to the total number of entities generated for the set of 100 sample records by each benchmark-annotated GS. Match and Partial refer to the number of entities in each benchmark-annotated GS that match or partially match an entity in our GS, regardless of label. Overlap is the sum of the matches and partial matches divided by the total number of entities in our GS, which is 510.

|               | Total | Match | Partial | Overlap |
|---------------|-------|-------|---------|---------|
| Conll-2003    | 44    | 36    | 8       | 0.086   |
| ACE-2005      | 195   | 133   | 54      | 0.35    |
| ACE Phase 1   | 122   | 89    | 26      | 0.22    |
| OntoNotes 5.0 | 61    | 52    | 9       | 0.12    |