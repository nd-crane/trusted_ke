#!/usr/bin/env python3
import pandas as pd
from pathlib import Path
from datetime import datetime
import sys
sys.path.append('./ReFinED/src')
from refined.inference.processor import Refined
from tqdm import tqdm
import argparse

def refined_results(dataset_path, model_name, entity_set, row_limit=None):
    df = pd.read_csv(dataset_path)

    # Apply row limit if specified
    if row_limit is not None:
        df = df.head(row_limit)

    new_df = pd.DataFrame(df['c5'], columns=['c5'])
    textcols = ['c119']

    # Set up Refined model once
    refined = Refined.from_pretrained(model_name=model_name,
                                      entity_set=entity_set)

    # Add original columns
    new_df['c119'] = df['c119']

    # Initialize tqdm progress bar
    tqdm.pandas(desc="Processing rows")

    # Add columns with entity linking information
    new_df['c119_entity_linking'] = df['c119'].progress_apply(lambda x: refined.process_text(x) if pd.notnull(x) else x)
    
    # Add timestamp to the output file path
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    filepath = Path(f'FAA_DataModel_{timestamp}.csv')
    filepath.parent.mkdir(parents=True, exist_ok=True)
    
    new_df.to_csv(filepath, index=False)  # Specify index=False to avoid saving row indices
    return

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-d', '--dataset_path',
        type=str,
        required=False,
        default="../../OMIn_dataset/data/FAA_data/Maintenance_Text_data_nona.csv",
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

    args = parser.parse_args()

    # Run with a row limit of 400 for example
    refined_results(args.dataset_path, args.model_name, args.entity_set, row_limit=None)