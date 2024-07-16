import argparse
import os
import pandas as pd

def print_results(tool_name, precision, recall, f1_score):

    print(f'\n### Automatic NER Evaluation of {tool_name.capitalize()} ###')
    print('------------------------------------------------------------')
    print('*** F1
    print(f'{"Precision":15}{precision}')
    print(f'{"Recall":15}{recall}')
    print(f'{"F1":15}{f1_score}')
    print('------------------------------------------------------------')

    return

def calculate_precision_recall_f1(gs, df_tool, id_col, ent_col, strict):
    """
    Calculate precision and recall based on entities comparison between gs (ground truth) and df_tool (answers).
    
    Parameters:
    - gs: DataFrame with columns ['id', 'sample', 'entities'] representing the ground truth.
    - df_tool: DataFrame with columns ['id', 'sample', 'entities', 'POS tags', 'labels'] representing the tool's answers.
    
    Returns:
    - A tuple containing precision and recall.
    """
    TP = 0  # True Positives
    FP = 0  # False Positives
    FN = 0  # False Negatives
    
    # Check for True Positives and False Negatives by iterating over gs
    for index, gs_row in gs.iterrows():
        gs_id, gs_entity = gs_row['id'], gs_row['entities']
        tool_entities = [entity.upper() for entity in df_tool.loc[df_tool[id_col] == gs_id, ent_col].tolist()] # get all the entities the tool generated for the gs_id entry

        # In strict matching, we only count a tool-generated entity as correct if it exactly matches the gold standard entity
        if strict:
            if gs_entity in tool_entities:
                TP += 1
            else:
                FN += 1
        # In non-strict matching, we count a tool-generated entity as correct if it is a subspan of the gold standard entity, or if the gold standard entity is a subspan of it
        else:
            if any(gs_entity in tool_entity or tool_entity in gs_entity for tool_entity in tool_entities):
                TP += 1
            else:
                FN += 1
    
    # Check for False Positives by iterating over df_tool
    for index, tool_row in df_tool.iterrows():
        tool_id, tool_entity = tool_row[id_col], tool_row[ent_col]
        gs_entities = gs.loc[gs['id'] == tool_id, 'entities'].tolist()

        #  Strict matching
        if strict:
            if tool_entity not in gs_entities:
                FP += 1
        else:
            if not any(tool_entity in gs_entity or gs_entity in tool_entity for gs_entity in gs_entities):
                FP += 1
    
    # Calculate precision and recall
    precision = TP / (TP + FP) if (TP + FP) > 0 else 0
    recall = TP / (TP + FN) if (TP + FN) > 0 else 0
    
    # Calculating the F1 score
    f1_score = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
    
    return precision, recall, f1_score

def eval(dataset_path, gs_path, id_col, ent_col, strict):

    gs = pd.read_csv(gs_path)
    df_tool = pd.read_csv(dataset_path)

    tool_name = dataset_path.split('/')[-2]

    precision, recall, f1_score = calculate_precision_recall_f1(gs, df_tool, id_col, ent_col, strict)

    print_results(tool_name, precision, recall, f1_score)


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
        '-e', '--ent_col',
        type=str,
        required=False,
        default="entities",
        help='Name of column in results dataset which contains entities'
    )
    parser.add_argument(
        '-g', '--gs_path',
        type=str,
        required=False,
        default="../../gold_standard/processed/ner.csv",
        help='Path to NER gold standard'
    )
    parser.add_argument(
        '-s', '--strict',
        required=False,
        action='store_true',
        default=False,
        help='Whether or not to perform strict-match evaluation'
    )

    args = parser.parse_args()

    # call eval
    eval(args.dataset_path, args.gs_path, args.id_col, args.ent_col, args.strict)