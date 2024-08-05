#!/usr/bin/env python3
import pandas as pd
from pathlib import Path
from datetime import datetime
from refined.inference.processor import Refined
from tqdm import tqdm
import argparse
import os
import sys
sys.path.append('./ReFinED')

values_p = re.compile("\[?\['([^']+)', (Entity not linked to a knowledge base|Entity\([^\)]+\)), (None|[A-Z]+)\],? ?(.*)") # returns groups ent, linked_ent, label, rest
id_title_p = re.compile('Entity\(wikidata_entity_id=(Q[0-9]+)(, wikipedia_entity_title=)?([^\)]+)?\)') # returns Qid, Wikipedia title

def reformat_output(result_df):

    out_dict = {'c5_id':[],'c119_input':[],'c119_entity_linking':[], 'mentions':[],'labels':[],'entities':[],'qids':[]}
    
    for i in range(len(result_df)):
    
        text = result_df['c119_entity_linking'].iat[i]
        while text:
            
            mo = re.match(values_p, text)
        
            if mo:
                ent, linked_ent, label, text = mo.groups()
        
                # Put empty values where there is no data
                # Extract QID and title from linked_ent
                if linked_ent == "Entity not linked to a knowledge base":
                    id = ""
                    title = ""
                else:
                    id_title = re.match(id_title_p, linked_ent).groups()
                    if len(id_title) == 1:
                        id_title = [id_title[0], "", ""]
                    id = id_title[0]
                    title = id_title[2]
                if label == "None":
                    label = ""
        
                out_dict['c5_id'].append(result_df['c5'].iat[i])
                out_dict['c119_input'].append(result_df['c119'].iat[i])
                out_dict['c119_entity_linking'].append(result_df['c119_entity_linking'].iat[i])
                out_dict['mentions'].append(ent)
                out_dict['labels'].append(label)
                out_dict['entities'].append(title)
                out_dict['qids'].append(id)
        
            else:
                text = None

    return out_dict

def refined_results(dataset_path, model_name, entity_set, row_limit=None):
    df = pd.read_csv(dataset_path)

    # Apply row limit if specified
    if row_limit is not None:
        df = df.head(row_limit)

    new_df = pd.DataFrame(df['c5'], columns=['c5'])
    textcols = ['c119']

    # Set up Refined model once
    refined = Refined.from_pretrained(model_name=model_name, entity_set=entity_set)

    # Add original columns
    new_df['c119'] = df['c119']

    # Initialize tqdm progress bar
    tqdm.pandas(desc="Processing rows")

    # Add columns with entity linking information
    new_df['c119_entity_linking'] = df['c119'].progress_apply(lambda x: refined.process_text(x) if pd.notnull(x) else x)

    out_dict = reformat_output(new_df)

    return out_dict    

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
        '-m', '--model_name',
        type=str,
        required=False,
        default="wikipedia_model",
        help='model to load: wikipedia_model or wikipedia_model_with_numbers'
    )
    parser.add_argument(
        '-e', '--entity_set',
        type=str,
        required=False,
        default="wikipedia",
        help='entity_set to use: wikipedia or wikidata'
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
        results_dict = refined_results(args.dataset_path, args.model_name, args.entity_set, row_limit=None)

        pd.DataFrame(results_dict).to_csv(args.output_path, index=False)  # Specify index=False to avoid saving row indices