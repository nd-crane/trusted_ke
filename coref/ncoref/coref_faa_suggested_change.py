#!/usr/bin/env python3
import spacy
import pandas as pd
from pathlib import Path
import neuralcoref
from datetime import datetime
from textblob import TextBlob
from tqdm import tqdm
import argparse
import os

def coref_setup(model_name):
    nlp = spacy.load(model_name)
    neuralcoref.add_to_pipe(nlp)
    return nlp

def coref(nlp, text):
    return nlp(text)._.coref_clusters

def ner(nlp, text):
    doc = nlp(text)
    return [(ent.text, ent.label_) for ent in doc.ents]

def pos_tagging(nlp, text):
    doc = nlp(text)
    return [(token.text, token.pos_) for token in doc]

def lemmatize(nlp, text):
    doc = nlp(text)
    return [token.lemma_ for token in doc]

def dependency_parsing(nlp, text):
    doc = nlp(text)
    return [(token.text, token.dep_, token.head.text) for token in doc]

def sentiment_analysis(text):
    blob = TextBlob(text)
    return blob.sentiment.polarity

def resolve(dataset_path, model_name, id_col, text_col, row_limit=None):
    df = pd.read_csv(dataset_path)

    # Apply row limit if specified
    if row_limit is not None:
        df = df.head(row_limit)

    new_df = pd.DataFrame(df[id_col], columns=[id_col])
    textcols = [text_col]

    # Set up coref once
    nlp = coref_setup()

    # Add original 'PROBLEM' and 'ACTION' columns
    new_df[text_col] = df[text_col]

    # Add columns with coreference clusters for 'PROBLEM' and 'ACTION'
    new_df['c119_coref'] = df[text_col].apply(lambda x: coref(nlp, x) if pd.notnull(x) else x)

    # Add columns for Named Entity Recognition (NER) and Part-of-Speech (POS) Tagging
    new_df['c119_ner'] = df[text_col].apply(lambda x: ner(nlp, x) if pd.notnull(x) else x)
    new_df['c119_pos'] = df[text_col].apply(lambda x: pos_tagging(nlp, x) if pd.notnull(x) else x)

    # Add columns for Lemmatization, Dependency Parsing, and Sentiment Analysis
    new_df['c119_lemmatized'] = df[text_col].apply(lambda x: lemmatize(nlp, x) if pd.notnull(x) else x)
    new_df['c119_dependency'] = df[text_col].apply(lambda x: dependency_parsing(nlp, x) if pd.notnull(x) else x)
    new_df['c119_sentiment'] = df[text_col].apply(lambda x: sentiment_analysis(x) if pd.notnull(x) else x)

    return new_df

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-d', '--dataset_path',
        type=str,
        required=False,
        default="../../data/FAA_data/Maintenance_Text_data_nona.csv",
        help='path/to/input/dataset.csv'
    )
    parser.add_argument(
        '-m', '--model_name',
        type=str,
        required=False,
        default="en_core_web_lg",
        help='spacy model to load'
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

        # Run with a row limit of 400 for example
        results_df = resolve(args.dataset_path, args.model_name, args.text_col, args.id_col, row_limit=None)

        results_df.to_csv(args.output_path, index=False)  # Specify index=False to avoid saving row indices