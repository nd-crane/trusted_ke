import torch
from model.model_transformers import  UniRelModel
from predict import UniRel
import pandas as pd
from pathlib import Path
from datetime import datetime


def unirel_setup():
    local = False
    if local:
        model_path = "./output/nyt/checkpoint-final"
        unirel = UniRel(model_path=model_path)
    else:
        # Load model directly
        #Changed predict.py to accept the UniRel pretrained model
        #Hugging Face Link: https://huggingface.co/vramesh/UniRel-nyt-checkpoint
        model = UniRelModel.from_pretrained("vramesh/UniRel-nyt-checkpoint")
        unirel = UniRel(model_path=None, model=model)

        '''# Sample Data to verify that it works, will replace with FAA Data
        print(unirel.predict("In perhaps the most ambitious Mekong cruise attempt, Impulse Tourism, an operator based in Chiang Mai, Thailand, is organizing an expedition starting in November in Jinghong, a small city in the Yunnan province in China."))
        print(unirel.predict("Adisham Hall in Sri Lanka was constructed between 1927 and 1931 at St Benedicts Monastery , Adisham , Haputhale , Sri Lanka in the Tudor and Jacobean style of architecture"))
        print(unirel.predict(["Anson was born in 1979 in Hong Kong.",
            "In perhaps the most ambitious Mekong cruise attempt, Impulse Tourism, an operator based in Chiang Mai, Thailand, is organizing an expedition starting in November in Jinghong, a small city in the Yunnan province in China.",
            "Adisham Hall in Sri Lanka was constructed between 1927 and 1931 at St Benedicts Monastery , Adisham , Haputhale , Sri Lanka in the Tudor and Jacobean style of architecture"
        ]))'''
    return unirel




def output_results(row_limit=None):
    df = pd.read_csv('data/FAA_data/Maintenance_Text_data_nona.csv')

    # Apply row limit if specified
    if row_limit is not None:
        df = df.head(row_limit)

    new_df = pd.DataFrame(df['c5'], columns=['c5'])
    textcols = ['c119']

    # Set up Unirel Setup
    unirel = unirel_setup()

    # Add original columns
    new_df['c119'] = df['c119']

    # Add columns with unirel output information
    new_df['c119_output'] = df['c119'].apply(lambda x: unirel.predict(x) if pd.notnull(x) else x)
    # Add timestamp to the output file path
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    filepath = Path(f'FAA_DataModel_{timestamp}.csv')
    filepath.parent.mkdir(parents=True, exist_ok=True)
    
    new_df.to_csv(filepath, index=False)  # Specify index=False to avoid saving row indices
    return

if __name__ == '__main__':
    # Run with a row limit of 400 for example
    output_results(row_limit=None)
