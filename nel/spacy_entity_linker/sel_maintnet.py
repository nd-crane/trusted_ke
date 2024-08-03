#!/usr/bin/env python3
import spacy
import pandas as pd
from pathlib import Path
from datetime import datetime

def entity_linker_setup():
    nlp = spacy.load("en_core_web_lg")
    # Add spaCy Entity Linker pipeline
    nlp.add_pipe("entityLinker", last=True)
    return nlp

def entity_linking(nlp, text):
    doc = nlp(text)
    entities_list = []
    for sent in doc.sents:
        for linked_entity in sent._.linkedEntities:
            # Concatenate the entity information in one line
            entity_info = {"indentifier":linked_entity.identifier, "label":linked_entity.label, "description":linked_entity.description}
            entities_list.append(entity_info)
    return entities_list

# ... (other functions remain the same)

def resolve_entity_linker(row_limit=None):
    df = pd.read_csv('data/MaintNet_data/Aircraft_Annotation_DataFile.csv')

    # Apply row limit if specified
    if row_limit is not None:
        df = df.head(row_limit)

    new_df = pd.DataFrame(df['IDENT'], columns=['IDENT'])
    textcols = ['PROBLEM', 'ACTION']

    # Set up spaCy Entity Linker once
    nlp = entity_linker_setup()

    # Add original 'PROBLEM' and 'ACTION' columns
    new_df['PROBLEM'] = df['PROBLEM']
    new_df['ACTION'] = df['ACTION']

    # Add columns with entity linking information for 'PROBLEM' and 'ACTION'
    new_df['PROBLEM_entity_linking'] = df['PROBLEM'].apply(lambda x: entity_linking(nlp, x) if pd.notnull(x) else x)
    new_df['ACTION_entity_linking'] = df['ACTION'].apply(lambda x: entity_linking(nlp, x) if pd.notnull(x) else x)

    # Add timestamp to the output file path
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    filepath = Path(f'tool_results/spacy_entity_linker/MaintNet_Aircraft_DataModel_{timestamp}.csv')
    filepath.parent.mkdir(parents=True, exist_ok=True)
    
    new_df.to_csv(filepath, index=False)  # Specify index=False to avoid saving row indices
    return

if __name__ == '__main__':
    # Run with a row limit of 400 for example
    resolve_entity_linker(row_limit=None)
