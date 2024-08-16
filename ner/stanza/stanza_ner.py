import stanza
import pandas as pd
from tqdm import tqdm
import argparse
import os

def main(dataset_path, model_name, id_col, text_col):
    
    sample = pd.read_csv(dataset_path)

    nlp = stanza.Pipeline(lang='en', processors='tokenize,mwt,ner',package={"ner": [model_name]})
    
    out_dict = {'index':[], 'c5_id':[], 'c119_text':[], 'entities':[], 'labels':[]}
    
    for index in range(len(sample)):
        text = sample['c119'][index]
        ents = nlp(text).ents
        for ent in ents:
            out_dict['index'].append(sample['Unnamed: 0'][index])
            out_dict['c5_id'].append(sample['c5'][index])
            out_dict['c119_text'].append(sample['c119'][index])
            out_dict['entities'].append(ent.text)
            out_dict['labels'].append(ent.type)
    return out_dict

if __name__=='__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-d', '--dataset_path',
        type=str,
        required=False,
        default="../../OMIn_dataset/data/FAA_data/Maintenance_Text_data_nona.csv",
        help='path/to/input/dataset.csv'
    )
    parser.add_argument(
        '-m', '--model',
        type=str,
        required=False,
        default="ontonotes-ww-multi_charlm",
        help='Specify name of model (https://huggingface.co/stanfordnlp/stanza-en/tree/main/models/ner)'
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

    #elif args.model not in ["conll03","ontonotes"]:
    #    print("Error: argument --model must be either 'conll03' or 'ontonotes'")
    else:
    
        # call main
        results_dict = main(args.dataset_path, args.model, args.id_col, args.text_col)
    
        # save to output_path
        pd.DataFrame(results_dict).to_csv(args.output_path, index=False)