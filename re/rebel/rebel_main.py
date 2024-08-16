from transformers import AutoConfig, AutoModelForSeq2SeqLM, AutoTokenizer
from time import time
import torch
import pandas as pd
import sys
from tqdm import tqdm
import argparse
import os

def load_models(dataset_path):
    tokenizer = AutoTokenizer.from_pretrained("Babelscape/rebel-large")
    model = AutoModelForSeq2SeqLM.from_pretrained("Babelscape/rebel-large")
    if torch.cuda.is_available():
        _ = model.to("cuda:0") # comment if no GPU available
    _ = model.eval()
    dataset = pd.read_csv(dataset_path)
    return (tokenizer, model, dataset)

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

def main(dataset_path, id_col, text_col, gen_kwargs):

    # load models
    tokenizer, model, dataset = load_models(dataset_path)
    
    id_col_name = f"{id_col}_id"
    text_col_name = f"{text_col}_input"
    results_dict = {id_col_name:[], text_col_name:[], "head":[], "relation":[], "tail":[]}
    
    for i in tqdm(range(len(dataset))):

        text = dataset[text_col].iat[i].lower()
        id = dataset[id_col].iat[i]
        
        model_inputs = tokenizer(text, max_length=256, padding=True, truncation=True, return_tensors = 'pt')
        
        generated_tokens = model.generate(
            model_inputs["input_ids"].to(model.device),
            attention_mask=model_inputs["attention_mask"].to(model.device),
            **gen_kwargs,
        )
    
        decoded_preds = tokenizer.batch_decode(generated_tokens, skip_special_tokens=False)
        decoded_preds = [text.replace('<s>', '').replace('</s>', '').replace('<pad>', '') for text in decoded_preds]
    
        for idx, sentence in enumerate(decoded_preds):
            
            extracted_triplets = extract_triplets(sentence)
            
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
        default = "../../OMIn_dataset/data/FAA_data/Maintenance_Text_Data_nona.csv",
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
    parser.add_argument(
        '-m', '--max_length',
        type=int,
        required=False,
        default=256,
        help='Max length of text input passed to model. Default is 256 characters'
    )
    parser.add_argument(
        '-p', '--length_penalty',
        type=float,
        required=False,
        default=0,
        help='Length penalty. If greater than 0, rewards longer sequences, if less than 0, rewards shorter sequences. Default is 0'
    )
    parser.add_argument(
        '-b', '--num_beams',
        type=int,
        required=False,
        default=1,
        help='Number of beams for beam search. If greater than 1, increases probability of finding best output, but increases computational load. Default is 1'
    )
    parser.add_argument(
        '-r', '--num_return_sequences',
        type=int,
        required=False,
        default=1,
        help='Number of sequences to return. Default is 1'
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
        
        gen_kwargs = {
            "max_length": args.max_length,
            "length_penalty": args.length_penalty,
            "num_beams": args.num_beams,
            "num_return_sequences": args.num_return_sequences,
        }

        # call main
        results_dict = main(args.dataset_path, args.id_col, args.text_col, gen_kwargs)
    
        # save to output_path
        pd.DataFrame(results_dict).to_csv(args.output_path, index=False)