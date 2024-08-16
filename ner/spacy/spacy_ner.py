import pandas as pd
import spacy
import argparse
import os
from tqdm import tqdm

def main(dataset_path, text_col, id_col, spacy_model_name):

    nlp = spacy.load(spacy_model_name)
    
    dataset = pd.read_csv(dataset_path)
    
    out_dict = {'c5_id':[], 'c119_input':[], 'entities':[], 'labels':[]}
    
    for index in tqdm(range(len(dataset))):
        text = dataset['c119'][index]
        ents = nlp(text).ents
        for ent in ents:
            out_dict['c5_id'].append(dataset[id_col][index])
            out_dict['c119_input'].append(dataset[text_col][index])
            out_dict['entities'].append(ent.text)
            out_dict['labels'].append(ent.label_)
    
    print(pd.DataFrame(out_dict))
    
    return out_dict

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
    parser.add_argument(
        '-m', '--spacy_model_name',
        type=str,
        required=True,
        help='May be "en_core_web_sm" or "en_core_web_lg"'
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

        out_dict = main(args.dataset_path, args.text_col, args.id_col, args.spacy_model_name)

        pd.DataFrame(out_dict).to_csv(args.output_path, index=False)
