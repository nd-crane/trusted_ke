# Code adapted from https://fouadroumieh.medium.com/nlp-entity-extraction-ner-using-python-nltk-68649e65e54b

import nltk
import pandas as pd
from tqdm import tqdm
import argparse
import os

# Download necessary NLTK data packages
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('maxent_ne_chunker')
nltk.download('words')

def main(dataset_path, id_col, text_col, lower):

    sample = pd.read_csv(dataset_path)
    
    out_dict = {'index':[], f'{id_col}_id':[], f'{text_col}_input':[], "entities":[], "POS tags":[], "labels":[]}
    
    for index in tqdm(range(len(sample))):
        
        text = sample[text_col][index]

        if lower:
            text = text.lower()
        
        tokens = nltk.word_tokenize(text)
        tagged_tokens = nltk.pos_tag(tokens)
        chunked = nltk.ne_chunk(tagged_tokens)
        entities = []
        for tree in chunked.subtrees():
            if tree.label() == "S":
                continue
            out_dict["index"].append(sample['Unnamed: 0'][index])
            out_dict[f"{id_col}_id"].append(sample[id_col][index])
            out_dict[f"{text_col}_input"].append(text)
            out_dict["entities"].append(' '.join([pair[0] for pair in tree.leaves()]))
            out_dict["POS tags"].append(', '.join([pair[1] for pair in tree.leaves()]))
            out_dict["labels"].append(tree.label())

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
        '-l', '--lower',
        action='store_true',
        help='Whether or not to lowercase text in preprocessing.'
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
        results_dict = main(args.dataset_path, args.id_col, args.text_col, args.lower)
        print(pd.DataFrame(results_dict))
    
        # save to output_path
        pd.DataFrame(results_dict).to_csv(args.output_path, index=False)