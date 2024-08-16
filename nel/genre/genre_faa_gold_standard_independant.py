import pandas as pd
from pathlib import Path
from datetime import datetime
from tqdm import tqdm
import torch
from torch.multiprocessing import Pool, set_start_method
import gc
from genre.fairseq_model import GENRE
from genre.entity_linking import get_end_to_end_prefix_allowed_tokens_fn_fairseq as get_prefix_allowed_tokens_fn

# Set the start method to 'spawn'
set_start_method('spawn', force=True)

def load_model(model_path):
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = GENRE.from_pretrained(model_path).to(device).eval()
    return model, device

def process_row(sentence_model_tuple):
    sentence, model_path = sentence_model_tuple
    model, device = load_model(model_path)
    
    with torch.no_grad():
        prefix_allowed_tokens_fn = get_prefix_allowed_tokens_fn(model, [sentence])
        predictions = model.sample([sentence], prefix_allowed_tokens_fn=prefix_allowed_tokens_fn)
        
        if predictions and predictions[0]:  # Check if predictions and predictions[0] are not empty
            best_prediction = max(predictions[0], key=lambda x: x['score'])
            result = (best_prediction['text'], best_prediction['score'].item())
        else:
            result = ("", "")
    
    # Clear model and CUDA memory
    del model
    torch.cuda.empty_cache()
    gc.collect()
    
    return result

def output_results(row_limit=None, batch_size=100):  # Run all in one batch
    df = pd.read_csv('../../OMIn_dataset/data/FAA_data/FAA_sample_100.csv')

    # Apply row limit if specified
    if row_limit is not None:
        df = df.head(row_limit)

    new_df = pd.DataFrame(df['c5'], columns=['c5_unique_id'])
    textcols = ['c119_text']

    # Load the model path
    model_path = "model/fairseq_e2e_entity_linking_aidayago"

    # Add original columns
    new_df['c119_text'] = df['c119']

    # Add columns with GENRE output information
    results = []
    pbar = tqdm(total=len(df))
    with Pool() as pool:
        for i in range(0, len(df), batch_size):
            batch = [(row, model_path) for row in df['c119'][i:i+batch_size]]
            batch_results = pool.map(process_row, batch)
            results.extend(batch_results)
            
            # Manually delete the model and clear GPU cache
            del batch_results
            torch.cuda.empty_cache()
            gc.collect()
            
            pbar.update(len(batch))
    pbar.close()

    output_data = list(zip(*results))
    new_df['c119_output'] = output_data[0]
    new_df['c119_score'] = output_data[1]

    # Add timestamp to the output file path
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    filepath = Path(f'FAA_model_gold_standards_independant_{timestamp}.csv')
    filepath.parent.mkdir(parents=True, exist_ok=True)
    
    new_df.to_csv(filepath, index=False)  # Specify index=False to avoid saving row indices
    return

if __name__ == '__main__':
    output_results(row_limit=None)
