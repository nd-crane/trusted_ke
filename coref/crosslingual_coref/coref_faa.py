#!/usr/bin/env python3
import spacy
import pandas as pd
from pathlib import Path
import neuralcoref


# TODO: This doesn't work
# Sources
# Found that spacy can handle panda data frames directly: https://stackoverflow.com/questions/43451906/load-column-in-csv-file-into-spacy
# Also found spacy coreference good for smaller datasets: https://spacy.io/universe/project/neuralcoref
# chatGPT

# Initialize neuralcoref
# neuralcoref.add_to_pipe(spacy.load('en_coref_trf'))


def resolve():
    coref = spacy.load('en_core_web_trf')
    df = pd.read_csv('data/FAA_data/Maintenance_Text_data.csv')

    # Note using first 100 col temporaraily so it doesn't run long
    new_df = pd.DataFrame(df['c5'][:100], columns=['c5'])
    textcols = ['c119']
    for textcol in textcols:
        new_df[textcol] = df[textcol][:100].apply(coref)

    filepath = Path('models/FAA_DataModel.csv')
    filepath.parent.mkdir(parents=True, exist_ok=True)
    new_df.to_csv(filepath, index=False)


if __name__ == '__main__':
    resolve()
