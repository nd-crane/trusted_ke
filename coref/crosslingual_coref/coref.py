#!/usr/bin/env python3
import spacy
import pandas as pd
from pathlib import Path
import neuralcoref
from datetime import datetime

def coref_setup():
    nlp = spacy.load('en_core_web_sm')
    neuralcoref.add_to_pipe(nlp)
    return nlp

def coref(nlp, text):
    return nlp(text)._.coref_clusters

def resolve():
    df = pd.read_csv('data/MaintNet_data/Aircraft_Annotation_DataFile.csv')

    # Limit to 400 rows temporarily so it doesn't run long
    num_rows = 400
    new_df = pd.DataFrame(df['IDENT'][:num_rows], columns=['IDENT'])
    textcols = ['PROBLEM', 'ACTION']

    # Set up coref once
    nlp = coref_setup()

    # Add original 'PROBLEM' and 'ACTION' columns
    new_df['PROBLEM'] = df['PROBLEM'][:num_rows]
    new_df['ACTION'] = df['ACTION'][:num_rows]

    # Add columns with coreference clusters for 'PROBLEM' and 'ACTION'
    new_df['PROBLEM_COREF'] = df['PROBLEM'][:num_rows].apply(lambda x: coref(nlp, x) if pd.notnull(x) else x)
    new_df['ACTION_COREF'] = df['ACTION'][:num_rows].apply(lambda x: coref(nlp, x) if pd.notnull(x) else x)

    # Add timestamp to the output file path
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    filepath = Path(f'models/Aircraft_Annotation_DataModel_{timestamp}.csv')
    filepath.parent.mkdir(parents=True, exist_ok=True)
    
    new_df.to_csv(filepath, index=False)  # Specify index=False to avoid saving row indices
    return

if __name__ == '__main__':
    resolve()
