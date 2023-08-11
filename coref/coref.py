#!/usr/bin/env python3
import spacy
import pandas as pd
from pathlib import Path


def resolve():
    coref = spacy.load('en_core_web_trf')
    df = pd.read_csv('MaintNet_data/Aircraft_Annotation_DataFile.csv')

    # Note using first 100 col temporary so it doesn't run long
    new_df = pd.DataFrame(df['IDENT'][:100], columns=['IDENT'])
    textcols = ['PROBLEM', 'ACTION']
    for textcol in textcols:
        new_df[textcol] = df[textcol][:100].apply(coref)
    filepath = Path('models/Aircraft_Annotation_DataModel.csv')
    filepath.parent.mkdir(parents=True, exist_ok=True)
    new_df.to_csv(filepath)
    # TODO: fix issue why it's outputting the df not new_df file
    return


if __name__ == '__main__':
    resolve()
