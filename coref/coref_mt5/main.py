"""
Adapted from the original code by @ianporada:
https://github.com/ianporada/mt5_coref_pytorch/blob/main/main.py
"""

import os
import time
import pandas as pd
import click
from transformers import MT5Tokenizer, T5ForConditionalGeneration
from tqdm import tqdm
import sys
sys.path.append('mt5_coref_pytorch')
from state import State
from util import create_document, create_next_batch, extract_result_string, predict_coreferences, read_jsonl


@click.command()
@click.option('--input_fname')
@click.option('--tokenizer_path', default='mt5-coref-pytorch/link-append-xxl')
@click.option('--model_path', default='mt5-coref-pytorch/link-append-xxl')
@click.option('--batch_size', default=1, type=int)
@click.option('--debug', is_flag=True, default=False, help="Enable debug mode")


def main(input_fname, tokenizer_path, model_path, batch_size, debug):

    # Setup model
    tokenizer = MT5Tokenizer.from_pretrained(tokenizer_path, device_map="auto")
    model = T5ForConditionalGeneration.from_pretrained(model_path, device_map="auto")

    # Load ontonotes
    inputs = read_jsonl(input_fname)
    sentence_count = 0
    states_dict = {}
    for doc in inputs:
        states_dict[doc['document_id']] = State(create_document(doc), tokenizer)
        sentence_count += len(doc["sentences"])

    print("----------------------------------")
    print(f'Loaded {len(inputs)} documents')
    print(f'Loaded {sentence_count} sentences')
    print("----------------------------------")
    
    total_time = time.time()
    total_results = 0
    docid_to_result = {}  # Keep results
    num_done = 0

    # Initialize CSV file with appropriate columns
    csv_filename = 'coref_mt5_intermediate.csv'
    columns = ['c5_id', 'input', 'prediction_strings', 'results']
    if not os.path.exists(csv_filename):
        pd.DataFrame(columns=columns).to_csv(csv_filename, index=False)

    # Initialize progress bar
    progress_bar = tqdm(total=sentence_count, desc='Processing', unit='sentences')

    while num_done < sentence_count:  # While states
        t = time.time()
        states, batches = create_next_batch(states_dict, batch_size=batch_size, num_batches=1)

        if not states:
            break

        documents_processing = set([x.input_document['doc_key'] for x in states])

        if debug:
            print(f'Processing documents: {documents_processing}')

        predictions = predict_coreferences(tokenizer, model, batches, len(batches))
        results = extract_result_string(predictions)

        if debug:
            print(predictions)
            print(results)

        for state, result, batch in zip(states, results, batches):
            state.extend(result)
            docid_to_result[state.input_document['doc_key']] = result  # Save result

            if debug:
                print('input batch[0]:                ', batch)
                print('mt5 output:                    ', results)

            # Save intermediate result to CSV
            row = {
                'c5_id': state.input_document['doc_key'].split('_')[1],
                'input': state.input_document,
                'prediction_strings': state.predictions_str,
                'results': docid_to_result[state.input_document['doc_key']]
            }
            pd.DataFrame([row]).to_csv(csv_filename, mode='a', header=False, index=False)

        total_results += len(results)
        num_done += len(results)
        progress_bar.update(len(results))

        if debug:
            print(
                f'time {time.time() - t}, round time/seq : {(time.time() - t) / len(results)}'
                f' total time/seq: {(time.time() - total_time) / total_results}'
            )

    progress_bar.close()


if __name__ == '__main__':
    results_dict = main()
    pd.DataFrame(results_dict).to_csv('coref_mt5_raw.csv', index=False)
