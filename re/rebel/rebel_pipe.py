from transformers import pipeline
import pandas as pd
import sys
from tqdm import tqdm
import argparse
import torch
import os

# Function to parse the generated text and extract the triplets
def extract_triplets(text):
    triplets = []
    relation, subject, relation, object_ = '', '', '', ''
    text = text.strip()
    current = 'x'
    for token in text.replace("<s>", "").replace("<pad>", "").replace("</s>", "").split():
        if token == "<triplet>":
            current = 't'
            if relation != '':
                triplets.append({'head': subject.strip(), 'type': relation.strip(),'tail': object_.strip()})
                relation = ''
            subject = ''
        elif token == "<subj>":
            current = 's'
            if relation != '':
                triplets.append({'head': subject.strip(), 'type': relation.strip(),'tail': object_.strip()})
            object_ = ''
        elif token == "<obj>":
            current = 'o'
            relation = ''
        else:
            if current == 't':
                subject += ' ' + token
            elif current == 's':
                object_ += ' ' + token
            elif current == 'o':
                relation += ' ' + token
    if subject != '' and relation != '' and object_ != '':
        triplets.append({'head': subject.strip(), 'type': relation.strip(),'tail': object_.strip()})
    return triplets

def main(dataset_path, id_col, text_col):

    # Load rebel-large model via Huggingface pipeline
    if torch.cuda.is_available():
        device = 0
    else:
        device = -1
    triplet_extractor = pipeline('text2text-generation', model='Babelscape/rebel-large', tokenizer='Babelscape/rebel-large', device=device)

    # Load dataset
    dataset = pd.read_csv(dataset_path)

    # Initialize results dict
    id_col_name = f"{id_col}_id"
    text_col_name = f"{text_col}_input"
    results_dict = {id_col_name:[], text_col_name:[], "head":[], "relation":[], "tail":[]}
    
    for i in tqdm(range(len(dataset))):
        
        text = dataset[text_col].iat[i]
        id = dataset[id_col].iat[i]
        
        # We need to use the tokenizer manually since we need special tokens.
        extracted_text = triplet_extractor.tokenizer.batch_decode([triplet_extractor(text, return_tensors=True, return_text=False)[0]["generated_token_ids"]])
    
        extracted_triplets = extract_triplets(extracted_text[0])
        
        for triplet in extracted_triplets:
            results_dict[id_col_name].append(id)
            results_dict[text_col_name].append(text)
            results_dict["head"].append(triplet["head"])
            results_dict["relation"].append(triplet["type"])
            results_dict["tail"].append(triplet["tail"])

    return results_dict

if __name__=='__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-d', '--dataset_path',
        type=str,
        required=False,
        default = "../../OMIn_dataset/data/FAA_data/Maintenance_Text_data_nona.csv",
        help='path/to/input/dataset.csv'
    )
    parser.add_argument(
        '-t', '--text_col',
        type=str,
        required=False,
        default="c119",
        help='Name of column in input dataset which contains text'
    )
    parser.add_argument(
        '-i', '--id_col',
        type=str,
        required=False,
        default="c5",
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

        # call main
        results_dict = main(args.dataset_path, args.id_col, args.text_col)
    
        # save to output_path
        pd.DataFrame(results_dict).to_csv(args.output_path, index=False)