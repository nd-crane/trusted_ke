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
  
## Tools by Task
| Coreference Resolution         | Named Entity Linking (NEL)       | Relation Extraction (RE)   |
|-------------------------------|---------------------------------|---------------------------|
| [ ] ASP                       | [x] BLINK                       | [x] REBEL                 |
| [ ] coref_mt5                 | [x] spaCy EntityLinker          | [ ] UniRel                |
| [ ] s2e-coref                 | [ ] GENRE                       | [ ] DeepStruct            |
| [x] neuralcoref               | [ ] ReFinED                     | [x] PL-Marker             |


 x Tested with results

Results for each tool are saved in the [results folder](../data/results/).

## Methodology for Comparing Tool Outputs with the Gold Standard

### Correctness evaluation for NEL
For each named entity in the NEL gold standard, compare the tool's linking decision against it.\
This comparison will allow us to calculate the metrics such as precision, recall, and F1 score.

### Correctness evaluation for RE
We need to define a process to make that comparison. We can use the following steps:
1. Extract the relations from the gold standard data.
2. Extract the relations from the tool's output.
3. Compare the relations from the tool's output against the gold standard relations.
   1. That comparisson can't be done directly because the tool's output and the gold standard data are in different formats. We need to find a way to make that comparisson.
4. Calculate the metrics such as precision, recall, and F1 score.

### Correctness evaluation for CR
[TODO]

### Correctness evaluation for NER
[TODO]