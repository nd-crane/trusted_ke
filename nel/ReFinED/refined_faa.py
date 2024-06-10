#!/usr/bin/env python3
import pandas as pd
from pathlib import Path
from datetime import datetime
from refined.inference.processor import Refined
from tqdm import tqdm

def refined_setup():
    refined = Refined.from_pretrained(model_name='wikipedia_model_with_numbers',
                                      entity_set="wikipedia")
    return refined

def refined_results(row_limit=None):
    df = pd.read_csv('../../data/FAA_data/Maintenance_Text_data_nona.csv')

    # Apply row limit if specified
    if row_limit is not None:
        df = df.head(row_limit)

    new_df = pd.DataFrame(df['c5'], columns=['c5'])
    textcols = ['c119']

    # Set up Refined model once
    refined = refined_setup()

    # Add original columns
    new_df['c119'] = df['c119']

    # Initialize tqdm progress bar
    tqdm.pandas(desc="Processing rows")

    # Add columns with entity linking information
    new_df['c119_entity_linking'] = df['c119'].progress_apply(lambda x: refined.process_text(x) if pd.notnull(x) else x)
    
    # Add timestamp to the output file path
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    filepath = Path(f'../../data/results/refined/FAA_DataModel_{timestamp}.csv')
    filepath.parent.mkdir(parents=True, exist_ok=True)
    
    new_df.to_csv(filepath, index=False)  # Specify index=False to avoid saving row indices
    return

if __name__ == '__main__':
    # Run with a row limit of 400 for example
    refined_results(row_limit=None)
