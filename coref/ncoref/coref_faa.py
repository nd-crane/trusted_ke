#!/usr/bin/env python3
import spacy
import pandas as pd
from pathlib import Path
import neuralcoref
from datetime import datetime
from textblob import TextBlob

def coref_setup():
    nlp = spacy.load('en_core_web_lg')
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

def resolve(row_limit=None):
    df = pd.read_csv('data/FAA_data/Maintenance_Text_data_nona.csv')

    # Apply row limit if specified
    if row_limit is not None:
        df = df.head(row_limit)

    new_df = pd.DataFrame(df['c5'], columns=['c5'])
    textcols = ['c119']

    # Set up coref once
    nlp = coref_setup()

    # Add original column
    new_df['c119'] = df['c119']

    # Add columns with coreference clusters
    new_df['c119_coref'] = df['c119'].apply(lambda x: coref(nlp, x) if pd.notnull(x) else x)

    # Add columns for Named Entity Recognition (NER) and Part-of-Speech (POS) Tagging
    new_df['c119_ner'] = df['c119'].apply(lambda x: ner(nlp, x) if pd.notnull(x) else x)
    new_df['c119_pos'] = df['c119'].apply(lambda x: pos_tagging(nlp, x) if pd.notnull(x) else x)

    # Add columns for Lemmatization, Dependency Parsing, and Sentiment Analysis
    new_df['c119_lemmatized'] = df['c119'].apply(lambda x: lemmatize(nlp, x) if pd.notnull(x) else x)
    new_df['c119_dependency'] = df['c119'].apply(lambda x: dependency_parsing(nlp, x) if pd.notnull(x) else x)
    new_df['c119_sentiment'] = df['c119'].apply(lambda x: sentiment_analysis(x) if pd.notnull(x) else x)

    # Add timestamp to the output file path
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    filepath = Path(f'tool_results/neuralcoref/FAA_DataModel_large_{timestamp}.csv')
    filepath.parent.mkdir(parents=True, exist_ok=True)
    
    new_df.to_csv(filepath, index=False)  # Specify index=False to avoid saving row indices
    return

if __name__ == '__main__':
    #Run with a row limit of 400 for example
    resolve(row_limit=None)
