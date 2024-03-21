# Gold Standard data
The [gold standard data](processed/samples.csv) is a subset of the [Complete Set of FAA data](../data/FAA_data/Maintenance_Text_data_nona.csv) created to evaluate the correctness of the tools regarding Named Entity Recognition (NER), Named Entity Linking (NEL) and Relation Extraction (RE) tasks.


## Gold Standard Preparation

The Gold Standard dataset is derived from a selected random subset of 100 records from the [Complete Set of FAA data](../data/FAA_data/Maintenance_Text_data_nona.csv). The subset selection is registered in the `FAA_sampling.ipynb` notebook.

In our preprocessing steps, we addressed the dataset's completeness by removing any records with empty entries in the c119 column, ensuring data integrity. Additionally, we undertook a thorough standardization process, aligning column names and structuring the data uniformly across tasks, to facilitate seamless analysis.

For those interested in the underlying data, both the initial raw files and the subsequently processed files, you can find them respectively at [raw folder](raw/) and [processed folder](processed/).\
The data preparation process, including the steps taken to create the Gold Standard dataset, is registered in the [gold_standard_preparation.ipynb](../notebooks/gold_standar_preparation.ipynb) notebook.


We have a gold standard for the each of following tasks:

- [Named Entity Recognition (NER)](processed/nel.csv)
- [Relation Extraction (RE)](processed/re.csv)
- [Coreference Resolution (CR)]()
- [Named Entity Linking (NEL)]()
  