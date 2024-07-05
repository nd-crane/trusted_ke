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

def eval(dataset_path, gs_path, id_col, cr_col):

    pred_df = pd.read_csv(dataset_path)
    gold_df = pd.read_csv(gs_path)

    tool_name = dataset_path.split('/')[-2]

    scorer = Scorer()

    for i in range(len(gold_df)):
        gold = ast.literal_eval(gold_df['coreferences'].iat[i])
        pred = ast.literal_eval(pred_df[pred_df[id_col]==gold_df['c5'].iat[i]][cr_col].iat[0])
        doc = Document(predicted=pred, truth=gold)
        scorer.update(doc)

    conll_f1, metrics = scorer.detailed_score(modelname=tool_name, dataset="FAA", verbose=True)
    print("The CoNLL-2012 F1 score is the average of F1 scores from MUC, B-CUBED, and CEAF")

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
        default="../../gold_standard/gold/coref_gold.csv",
        help='Path to NER gold standard'
    )

    args = parser.parse_args()

    # call eval
    eval(args.dataset_path, args.gs_path, args.id_col, args.cr_col)