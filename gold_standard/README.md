### Gold Standard Preparation

We randomly selected 100 records from the FAA data to manually evaluate correctness. This sample of 100 comes from the ../data/FAA_data/Maintenance_Text_data_nona.csv, as shown in FAA_sampling.ipynb, since this dataset removes records that have empty entries in the c119 column.

In progress:
- see create_eval_sheets.ipynb - creates coref_gold.xlsx, nel_gold.xlsx, and re_gold.xlsx
- nel_gold.xlsx and re_gold.xlsx have spacy NER results included so that the person manually preparing gold standards can reference it. However, some of spacy's results for NER seem incorrect, so we need to manually review spacy's results first. => See spacy_ner_gold.ipynb which creates an excel sheet ready to be evaluated.