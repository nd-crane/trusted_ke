# Credit to https://github.com/tollefj/coreference-eval
# To use, create virtual environment and run pip install coreference-eval numpy pandas

# Data in coreferences column should be in this format:
# [ coreference_chain, coreference_chain, ... ] where coreference_chain = [mention_span, mention_span, ...] and mention_span = [start_word_index, end_word_index]
# Such that the coreference chain for the sentence "PILOT LANDED ON WHAT HE THOUGHT TO BE ONE FOOT HIGH GRASS. IT TURNED OUT TO BE THREE FEET HIGH. ACFT NOSED OVER.":
# Which is: [["PILOT", "HE"], ["ONE FOOT HIGH GRASS", "IT"]]
# Appears as: [[0,0],[4,4],[[8,11],[13,13]]]
# The word indices are based on the word tokenization used in data/FAA_data/faa.conll, which is the input data for ASP and s2e-coref. The word indices continue to increase throughout the whole doc/entry and do not reset at sentence starts

import pandas as pd
import ast
import argparse
from corefeval import Document, Scorer

def print_results(tool_name, conll_f1, metrics):

    scores = {metric:{'prec':f"{float(metrics[metric]['precision']):.2}", 'rec':f"{float(metrics[metric]['recall']):.2}", 'f1':f"{float(metrics[metric]['f1']):.2}"} for metric in metrics}
    conll_f1 = f"{conll_f1:.2}"
    
    print("|                    | MUC Prec | MUC Rec | MUC F1 | B3 Prec | B3 Rec |  B3 F1 | CEAF Prec | CEAF Rec | CEAF F1 | Con12 F1 | LEA Prec | LEA Rec | LEA F1 |")
    print("|--------------------|----------|---------|--------|---------|--------|--------|-----------|----------|---------|----------|----------|---------|--------|")
    print(f"| {tool_name:19}| {scores['muc']['prec']:9}| {scores['muc']['rec']:8}| {scores['muc']['f1']:7}| {scores['b_cubed']['prec']:8}| {scores['b_cubed']['rec']:7}| {scores['b_cubed']['f1']:7}| {scores['ceafe']['prec']:10}| {scores['ceafe']['rec']:9}| {scores['ceafe']['f1']:8}| {conll_f1:9}| {scores['lea']['prec']:9}| {scores['lea']['rec']:8}| {scores['lea']['f1']:7}|")

def eval(dataset_path, gs_path, id_col, cr_col):

    pred_df = pd.read_csv(dataset_path)
    gold_df = pd.read_csv(gs_path)

    tool_name = dataset_path.split('/')[-2]

    scorer = Scorer()

    for i in range(len(gold_df)):
        gold = ast.literal_eval(gold_df['coreferences'].iat[i])
        pred = ast.literal_eval(pred_df[pred_df[id_col]==gold_df['id'].iat[i]][cr_col].iat[0])
        doc = Document(predicted=pred, truth=gold)
        scorer.update(doc)

    conll_f1, metrics = scorer.detailed_score(modelname=tool_name, dataset="FAA", verbose=False)

    return tool_name, conll_f1, metrics

if __name__=='__main__':

    parser = argparse.ArgumentParser()
    
    parser.add_argument(
        '-d', '--dataset_path',
        type=str,
        required=True,
        help='path/to/results/dataset.csv'
    )
    parser.add_argument(
        '-i', '--id_col',
        type=str,
        required=False,
        default="c5_id",
        help='Name of column in input dataset which contains unique identifier'
    )
    parser.add_argument(
        '-c', '--cr_col',
        type=str,
        required=False,
        default="corefs",
        help='Name of column in results dataset which contains lists of coreference chains.'
    )
    parser.add_argument(
        '-g', '--gs_path',
        type=str,
        required=False,
        default="../../OMIn_dataset/gold_standard/processed/cr.csv",
        help='Path to CR gold standard'
    )

    args = parser.parse_args()

    # call eval
    tool_name, conll_f1, metrics = eval(args.dataset_path, args.gs_path, args.id_col, args.cr_col)

    print_results(tool_name, conll_f1, metrics)