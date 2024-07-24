# FOLLOWING SemEval 2013 STRATEGY:
# https://aclanthology.org/S13-2056.pdf

# Requirements: scikit-learn==1.5.0 nltk sklearn_crfsuite pandas
# Add NER-Evaluation as a submodule in this folder

import sys
sys.path.append("./NER-Evaluation")

import nltk
import sklearn_crfsuite

from copy import deepcopy
from collections import defaultdict

from sklearn_crfsuite.metrics import flat_classification_report

from ner_evaluation.ner_eval import compute_metrics
from ner_evaluation.ner_eval import compute_precision_recall_wrapper
from ner_evaluation.ner_eval import find_overlap

import pandas as pd
import json
import argparse

from collections import namedtuple
Entity = namedtuple("Entity", "e_type start_offset end_offset")

conll_tags = ['PER', 'ORG', 'MISC', 'LOC']
ace_nltk_tags = ['PER','ORG','LOC','FAC','GPE'] # RESTRICTED SET
ace_tags = ['PER','ORG','LOC','FAC','GPE','VEHICLE','WEAPON']
on_tags = ['PER','ORG','LOC','FAC','GPE','PRODUCT','NORP','QUANTITY','EVENT','WORK_OF_ART','CARDINAL','DATE','PERCENT','TIME','ORDINAL','MONEY','LAW','LANGUAGE']

def print_results_typed(tool_name, results):

    scores = {'exact':0.0,'strict':0.0,'partial':0.0,'ent_type':0.0}
    for score in scores:
        prec = results[score]['precision']
        rec = results[score]['recall']
        scores[score] = f"{2*prec*rec/(prec+rec):.4}" 

    print('|                                         | Strict  | Exact  | Partial  | Type    |')
    print('|-----------------------------------------|---------|--------|----------|---------|')
    print(f"| {tool_name:40}| {scores['strict']:8}| {scores['exact']:7}| {scores['partial']:9}| {scores['ent_type']:8}|")

def print_results_untyped(tool_name, results):
    scores = {'exact':0.0,'partial':0.0}
    for score in scores:
        prec = results[score]['precision']
        rec = results[score]['recall']
        scores[score] = {'prec':f"{prec:.4}", 'rec':f"{rec:.4}", 'f1':f"{(2*prec*rec/(prec+rec)):.4}"}

    print('|                                         | Precision (Weak) | Recall (Weak) | F1 (Weak)     | Precision (Strong) | Recall (Strong) | F1 (Strong) |')
    print('|-----------------------------------------|------------------|---------------|---------------|--------------------|-----------------|-------------|')
    print(f"| {tool_name:40}| {scores['partial']['prec']:17}| {scores['partial']['rec']:14}| {scores['partial']['f1']:14}| {scores['exact']['prec']:19}| {scores['exact']['rec']:16}| {scores['exact']['f1']:12}|")

def get_faa_tokenized():
    # Get FAA data in format {c5_id:{0: word0, 1: word1, ..., n: wordn}} using word tokenization from faa.conll    
    with open('../../data/FAA_data/faa.conll') as f:
        text = f.read()
    faa = {}
    docs = text.split('#begin document ')
    for doc in docs:
        if doc[:5] == '(faa/':
            word_count = 0
            c5_id = doc.split('_')[1][:15]
            faa[c5_id] = {}
            lines = doc.split('\n')
            for line in lines[1:]:
                if 'faa' in line:
                    faa[c5_id][word_count] = line.split()[3].upper()
                    word_count = word_count + 1
    # Fix known err
    faa['19980620030289I'] = {0: 'MR.', 1: 'KADERA', 2: 'THEN', 3: 'ATTEMPTED', 4: 'TO', 5: 'LAND', 6: 'IN', 7: 'A', 8: 'FIELD', 9: 'BUT', 10: 'WAS', 11: 'FORCED', 12: 'TO', 13: 'LAND', 14: 'ON', 15: 'HIGHWAY', 16: '93', 17: '.', 18: 'THREE', 19: 'MILES', 20: 'EAST', 21: 'OF', 22: 'SUNMER', 23: ',', 24: 'IOWA'}

    return faa

def get_spans(mentions, words):
    ''' Input:
    - mentions:['MENTION1','MENTION2',...]
    - words: ['This','is','a','sentence','.','This','is','another','sentence','.'] (dict values)
        Output: [[startidx_mention1, end_idxmention1], [startidx_mention2, end_idxmention2], ...]
    '''

    mention_spans = []

    if "'S" in words.values():
        idx = list(words.values()).index("'S")
        words[idx-1] = words[idx-1] + "'S"
        del words[idx]
    
    for mention in mentions:

        mention = mention.replace('(', ' ( ').replace(')',' ) ').replace('  ',' ')
        mention = mention.replace(',',' , ').replace('  ',' ')

        mention_span = [-1, -1]
        
        if mention in ' '.join(words.values()):
            try:
                start_idx = list(words.values()).index(mention.split()[0])
                end_idx = list(words.keys())[list(words.values())[start_idx:].index(mention.split()[-1]) + start_idx] + 1
                mention_span = [start_idx, end_idx]
            except:
                pass
        
        mention_spans.append(mention_span)

    return mention_spans

def collect_named_entities(entities, labels, tokens):
    """
    Our version of collect_named_entities() from https://github.com/davidsbatista/NER-Evaluation/blob/master/ner_evaluation/ner_eval.py#L155
    
    Creates a list of Entity named-tuples, storing the entity type and the start and end
    offsets of the entity.

    Parameters:
    - entities: ["ENT1","ENT2"...] All entities for a doc
    - labels: ["LABEL1","LABEL2"...] All corresponding labels for a doc
    - tokens: dict_values(['TOW', 'PLANE', 'BECAME', ...]) Tokenized doc. Result of faa[doc_id].values()

    Returns: a list of Entity named-tuples
    """

    ent_spans = get_spans(entities, tokens)

    named_entities = []
    for ient, ent_span in enumerate(ent_spans):
        named_entities.append(Entity(labels[ient], ent_span[0], ent_span[1]))

    return named_entities

def load_gold(gold_path):
    gold_df = pd.read_csv(gold_path)
    if 'labels' not in gold_df.columns:
        gold_df['labels'] = ['ORG']*len(gold_df) # Add dummy labels for aviation mentions-only gs
    return gold_df

def load_result(data_path):
    result_df = pd.read_csv(data_path)
    abbrevs = {'FACILITY':'FAC','ORGANIZATION':'ORG','PERSON':'PER','LOCATION':'LOC','VEH':'VEHICLE','WEA':'WEAPON'}
    result_df['labels'] = result_df['labels'].apply(lambda x: abbrevs[x] if x in abbrevs else x)
    result_df.rename(columns={'c5_unique_id':'id', 'c5_id':'id'},inplace=True)
    result_df['entities'] = result_df['entities'].apply(str.upper)
    return result_df

def sort_ents(true_ents):
    final_ents = {ent:0 for ent in true_ents}
    for ent_a in true_ents:
        rest = [ent for ent in true_ents if ent != ent_a]
        for ent_b in rest:
            overlap = find_overlap(range(ent_a[1],ent_a[2]),range(ent_b[1],ent_b[2]))
            #print(f"Comparing {ent_a} with {ent_b}, overlap = {overlap}")
            if len(overlap) > 0 and len(range(ent_a[1],ent_a[2])) > len(range(ent_b[1],ent_b[2])):
                final_ents[ent_a] += 1
    return [ent[0] for ent in sorted(final_ents.items(), key=lambda x: x[1])]

def get_true_pred_ents(gold_df, result_df, faa):
    all_true_ents = []
    all_pred_ents = []
    
    for doc_id in gold_df['id'].unique():
        true_rows = gold_df.dropna()[gold_df.dropna()['id']==doc_id]
        pred_rows = result_df.dropna()[result_df.dropna()['id']==doc_id]
    
        true_ents = collect_named_entities(true_rows['entities'].to_list(),true_rows['labels'].to_list(),faa[doc_id])
        pred_ents = collect_named_entities(pred_rows['entities'].to_list(),pred_rows['labels'].to_list(),faa[doc_id])
        
        all_true_ents.append(sort_ents(true_ents))
        all_pred_ents.append(pred_ents)
    return all_true_ents, all_pred_ents

def eval(all_true_ents, all_pred_ents, tags):
    metrics_results = {'correct': 0, 'incorrect': 0, 'partial': 0,
                   'missed': 0, 'spurious': 0, 'possible': 0, 'actual': 0, 'precision': 0, 'recall': 0}

    # overall results
    results = {'strict': deepcopy(metrics_results),
               'ent_type': deepcopy(metrics_results),
               'partial':deepcopy(metrics_results),
               'exact':deepcopy(metrics_results)
              }
    
    for true_ents, pred_ents in zip(all_true_ents, all_pred_ents):
        
        # compute results for one message
        tmp_results, tmp_agg_results = compute_metrics(
            true_ents, pred_ents,  tags
        )
        
        #print(tmp_results)
    
        # aggregate overall results
        for eval_schema in results.keys():
            for metric in metrics_results.keys():
                results[eval_schema][metric] += tmp_results[eval_schema][metric]
                
        # Calculate global precision and recall
            
        results = compute_precision_recall_wrapper(results)
    
    return results

def main(dataset_path, gs_path):

    faa = get_faa_tokenized()

    gold_df = load_gold(gs_path)
    result_df = load_result(dataset_path)

    tool_name = dataset_path.split('/')[-2]

    all_true_ents, all_pred_ents = get_true_pred_ents(gold_df, result_df, faa)

    if tool_name == "flair":
        tags = conll_tags
    elif tool_name in ["spacy_entityrecognizer","stanza"]:
        tags = on_tags
    elif tool_name == "nltk":
        tags = ace_nltk_tags
    elif tool_name == "pl-marker":
        tags = ace_tags

    results = eval(all_true_ents, all_pred_ents, tags)

    return tool_name, results

if __name__=='__main__':

    parser = argparse.ArgumentParser()
    
    parser.add_argument(
        '-d', '--dataset_path',
        type=str,
        required=True,
        help='path/to/results/dataset.csv'
    )
    parser.add_argument(
        '-g', '--gs_path',
        type=str,
        required=True,
        help='Path to NER gold standard'
    )
    parser.add_argument(
        '-u', '--untyped',
        action="store_true"
    )

    args = parser.parse_args()

    # call eval
    tool_name, results = main(args.dataset_path, args.gs_path)

    if args.untyped:
        print_results_untyped(tool_name, results)
    else:
        print_results_typed(tool_name, results)