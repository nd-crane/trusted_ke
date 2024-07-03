from flair.data import Sentence
from flair.nn import Classifier
import pandas as pd
from tqdm import tqdm
import argparse
import os

def main(dataset_path, id_col, text_col):
    dataset = pd.read_csv(dataset_path)
    
    out_dict = {f'{id_col}_id':[], f'{text_col}_input':[], 'entities':[], 'labels_raw':[], 'labels':[],'confidence':[]}
    
    tagger = Classifier.load('ner')
    
    for index in tqdm(range(len(dataset))):
        text = dataset['c119'][index]
        sentence = Sentence(text)
        tagger.predict(sentence)
        sent_dict = sentence.to_dict()
        if 'entities' not in sent_dict:
            print("err on ", sent_dict)
            continue
        ents = sent_dict['entities']
    
        for ent in ents:
            out_dict[f'{id_col}_id'].append(dataset['c5'][index])
            out_dict[f'{text_col}_input'].append(dataset['c119'][index])
            out_dict['entities'].append(ent['text'])
            out_dict['labels_raw'].append(ent['labels'])
            out_dict['labels'].append(ent['labels'][0]['value'])
            out_dict['confidence'].append(ent['labels'][0]['confidence'])
    
    return out_dict


if __name__=='__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-d', '--dataset_path',
        type=str,
        required=False,
        default="../../data/FAA_data/Maintenance_Text_data_nona.csv",
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