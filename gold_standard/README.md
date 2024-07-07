# Gold Standard data
The [gold standard data](processed/samples.csv) is a subset of the [Complete Set of FAA data](../data/FAA_data/Maintenance_Text_data_nona.csv) created to evaluate the correctness of the tools regarding Named Entity Recognition (NER), Coreference Resolution (CR), Named Entity Linking (NEL) and Relation Extraction (RE) tasks.


## Gold Standard Preparation

The Gold Standard dataset is derived from a [selected random subset of 100 records](../data/sampling/FAA_sample_100.csv) from the [Complete Set of Processed FAA data](../data/FAA_data/Maintenance_Text_data_nona.csv).

The gold standard datasets were hand crafted by our team, following guidelines described in the [gold folder](gold/README.md). For those interested in the gold standard creation process, the raw result from our team, including notes, is available in the [raw folder](raw/), and the processed files are available in the [processed folder](processed/). The data preparation process, including the steps taken to create the Gold Standard dataset, is registered in the [gold_standard_preparation.ipynb](../notebooks/gold_standar_preparation.ipynb) notebook.


We have a gold standard for the each of following tasks:

- [Named Entity Recognition (NER)](processed/nel.csv)
- [Coreference Resolution (CR)]()
- [Named Entity Linking (NEL)]()
- [Relation Extraction (RE)](processed/re.csv)
  
