#!/usr/bin/env python3
import spacy
import pandas as pd
from pathlib import Path
from datetime import datetime
from tqdm import tqdm
import argparse
import os

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
            entity_info = {"identifier":linked_entity.identifier, "label":linked_entity.label, "description":linked_entity.description}
            entities_list.append(entity_info)
    return entities_list

# ... (other functions remain the same)

def resolve_entity_linker(dataset_path, id_col, text_col, row_limit=None):
    
    df = pd.read_csv(dataset_path)

    # Apply row limit if specified
    if row_limit is not None:
        df = df.head(row_limit)

    results_dict = {'c5_id':[], 'c119_input':[], 'raw_results':[], 'entities':[], 'qids':[], 'descriptions':[]}

    # Set up spaCy Entity Linker once
    nlp = entity_linker_setup()

    for i in tqdm(range(len(df))):
        id = df['c5'].iat[i]
        text = df['c119'].iat[i]
        results = entity_linking(nlp, text)
        for result in results:
            results_dict['c5_id'].append(id)
            results_dict['c119_input'].append(text)
            results_dict['raw_results'].append(results)
            results_dict['entities'].append(result['label'])
            results_dict['qids'].append(result['identifier'])
            results_dict['descriptions'].append(result['description'])
    
    return results_dict

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-d', '--dataset_path',
        type=str,
        required=False,
        default="../../data/FAA_data/Maintenance_Text_data_nona.csv",
        help='path/to/input/dataset.csv'
    )
    parser.add_argument(
        '-t', '--text_col',
        type=str,
        required=False,
        default='c119',
        help='Name of column in input dataset which contains text'
    )
    parser.add_argument(
        '-i', '--id_col',
        type=str,
        required=False,
        default='c5',
        help='Name of column in input dataset which contains unique identifier'
    )
    parser.add_argument(
        '-o', '--output_path',
        type=str,
        required=True,
        help='path/to/output/dataset.csv'
    )

    args = parser.parse_args()

    output_path = args.output_path
    file_name = output_path.split('/')[-1]
    output_dir = '/'.join(output_path.split('/')[:-1])
    if output_dir == '':
        output_dir = './'
    if file_name[-4:] != '.csv' or not os.path.isdir(output_dir):
        print("Error: output_path must be a .csv file in a valid location.")

    else:

        # Run with a row limit of 400 for example
        results_dict = resolve_entity_linker(args.dataset_path, args.text_col, args.id_col, row_limit=None)

        pd.DataFrame(results_dict).to_csv(args.output_path, index=False)  # Specify index=False to avoid saving row indices