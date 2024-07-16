import os
import requests
import json
import pandas as pd
import ast
import math
import argparse

def print_results(tool_name, scores_dict):

    print(f'\n### Automatic NEL Evaluation of {tool_name.title()} ###')
    for setup in scores_dict:
        print('------------------------------------------------------------')
        print(setup)
        for metric in scores_dict[setup]:
            print(f"{metric+':':20} {scores_dict[setup][metric]}")
    print('------------------------------------------------------------')

    return

## DATA PROCESSING FUNCS #############################################################################################

def is_match(ent1, ent2, matching):
    ''' Returns True if the entities match.
    matching may be "STRONG" or "WEAK".
    A strong match is an exact match.
    A weak match is where ent1 is found in ent2 or ent2 is found in ent1'''

    if type(ent1) != str or type(ent2) != str:
        return False
    
    if matching == "STRONG":
        return ent1 == ent2
    elif matching == "WEAK":
        return any([ent1 in ent2, ent2 in ent1])
    else:
        print("Error: matching must be 'STRONG' or 'WEAK'")
        return None

def find_match(gs_entities, tool_entities, matching, gold_set):
    ''' Returns (-1,-1) if no version of the gs_entity at hand is present in tool_entities.
    If a version of the gs_entity is present in tool entities, it returns the index of the
    gs_entity that matched it and the index in tool_entities of the matching entity in a tuple.
    Also uses weak matching if specified'''

    tool_entities = pd.Series(tool_entities)
    stop_idx = len(gs_entities) if gold_set == "EXTENDED" else 1

    for gold_idx in range(stop_idx):
        matches = tool_entities[tool_entities.apply(is_match, ent2 = gs_entities[gold_idx], matching=matching)]
        
        if len(matches) > 0:
            found_idx_ent = (gold_idx, gs_entities[gold_idx])
            return (gold_idx, matches.index.to_list()[0])
    
    return (-1,-1)

def prune_gold_set(gs_entities, gs_qids, gold_set, fill_in_qids):

    if fill_in_qids and None in gs_qids:
        none_idx = gs_qids.index(None)
        if none_idx == 0 and gs_qids[1] != None:
            gs_qids[0] = gs_qids[1]
        elif none_idx == 0 and gs_qids[2] != None:
            gs_qids[0] = gs_qids[2]
            gs_qids[1] = gs_qids[2]
        elif none_idx == 1 and gs_qids[2] != None:
            gs_qids[1] = gs_qids[2]
    
    stop_idx = 3 if gold_set == "EXTENDED" else 1
    valid_data = pd.DataFrame({'ents':gs_entities, 'qids':gs_qids}).iloc[:stop_idx].dropna()
    
    return (valid_data['ents'].to_list(), valid_data['qids'].to_list())

## F1 SCORE CALCULATION (Following GERBIL, with extra options) ############################################################

def calculate_precision_recall_f1(gs, df_tool, id_col, ent_col, qid_col, matching='WEAK', gold_set='PRIMARY', fill_in_qids=False):
    """
    Calculate precision and recall based on entities comparison between gs (ground truth) and df_tool (answers).
    
    Parameters:
    - gs: DataFrame with columns ['id', 'sample', 'entities','qids'] representing the ground truth.
    - df_tool: DataFrame with columns ['id', 'sample', 'entities', 'qids'] representing the tool's answers.
    - id_col, ent_col, and qid_col are the column names used in df_tool for the docid, entities (the mentions
    from the text, not Wikidata entity titles), and the QIDs, respectively.
    - matching may be "WEAK" or "STRONG". Strong matching counts an entity-link pair as correct if the entity
    exactly matches the entity in the gold standard, and the links are the same. Weak matching counts it as
    correct if the entity overlaps with the entity in the gold standard, and the links are the same.
    - gold_set may be "PRIMARY" or "EXTENDED". The primary set of gold standard entity-link pairs are those in
    the columns beginning with "primary" in the gold standard. The extended gold standard includes secondary
    and tertiary entity-link pairs, which attempt to account for variability in entity-tagging by providing correct
    links for other possible spans for each entity where applicable.
    
    Returns:
    - A tuple containing precision and recall.
    """
    TP = 0  # True Positives
    FP = 0  # False Positives
    FN = 0  # False Negatives

    for index, gs_row in gs.iterrows():
        gs_id, gs_entities, gs_qids = gs_row['id'], ast.literal_eval(gs_row['entity']), ast.literal_eval(gs_row['qid'])
        # Remove gs ent/qid pairs for which there is the ent or qid is None
        # fill_in_qids replaces qids of None to match the next qid in the extended set (always that of a more "general" entity), if there is one.
        gs_entities, gs_qids = prune_gold_set(gs_entities, gs_qids, gold_set, fill_in_qids)
        if len(gs_entities) == 0:
            continue

        selected_rows = df_tool[df_tool[id_col] == gs_id][qid_col].dropna().index # select rows in df_tool which have same docid as gsid, and there is a QID for the entity in the row
        tool_entities = [entity.upper() for entity in df_tool.loc[selected_rows][ent_col]] # get all the entities the tool generated for the gs_id entry
        tool_qids = [qid for qid in df_tool.loc[selected_rows][qid_col]] # get all the entities the tool generated for the gs_id entry

        # Check for False Negative (Gold Standard ent does not appear in tool output)
        gs_match_idx, tool_match_idx = find_match(gs_entities, tool_entities, matching, gold_set)
        if gs_match_idx == -1:
            FN += 1

        # Check for True and False Positives (based on link correctness)
        else:
            start_idx = 0 if gold_set == "EXTENDED" else gs_match_idx # with the extended gold set, if the matching entity is
                                                                        # a secondary or tertiary entity, the more primary QID's are still correct
                                                                        # since they are simply more specific and context-aware.
            if tool_qids[tool_match_idx] in gs_qids[start_idx:gs_match_idx+1]:
                TP += 1
            else:
                FP += 1        

        # Note: We only evaluate the set of entity-link pairs where the entity is present in the gold standard.
        # Note: An incorrect link is counted the same as a missing one if there is a correct link in the gold standard
            
    
    # Calculate precision and recall
    print(f"TP ={TP}, FP={FP}, FN={FN}")
    precision = TP / (TP + FP) if (TP + FP) > 0 else 0
    recall = TP / (TP + FN) if (TP + FN) > 0 else 0
    
    # Calculating the F1 score
    f1_score = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
    
    return precision, recall, f1_score

## SEMANTIC SIMILARITY SCORE UTILS #####################################################################

def match_gold_pred(gs, df_tool, id_col, ent_col, qid_col, matching, gold_set, fill_in_qids):
    
    id = []
    tool_ent = []
    gold_ent = []
    q1_gold = []
    q2_pred = []
    
    for index, gs_row in gs.iterrows():
        gs_id, gs_entities, gs_qids = gs_row['id'], ast.literal_eval(gs_row['entity']), ast.literal_eval(gs_row['qid'])
        # Remove gs ent/qid pairs for which there is the ent or qid is None
        # fill_in_qids replaces qids of None to match the next qid in the extended set (always that of a more "general" entity), if there is one.
        gs_entities, gs_qids = prune_gold_set(gs_entities, gs_qids, gold_set, fill_in_qids)
        if len(gs_entities) == 0:
            continue
        
        selected_rows = df_tool[df_tool[id_col] == gs_id][qid_col].dropna().index # select rows in df_tool which have same docid as gsid, and there is a QID for the entity in the row
        tool_entities = [entity.upper() for entity in df_tool.loc[selected_rows][ent_col]] # get all the entities the tool generated for the gs_id entry
        tool_qids = [qid for qid in df_tool.loc[selected_rows][qid_col]] # get all the entities the tool generated for the gs_id entry
    
        # Find matching gold standard and output entity-link pair if present
        gs_match_idx, tool_match_idx = find_match(gs_entities, tool_entities, matching, gold_set)
        if gs_match_idx == -1:
            continue
    
        # Append to arrays as appropriate
        id.append(gs_id)
        gold_ent.append(gs_entities[gs_match_idx])
        tool_ent.append(tool_entities[tool_match_idx])
        q1_gold.append(gs_qids[gs_match_idx])
        q2_pred.append(tool_qids[tool_match_idx])

    return id, tool_ent, gold_ent, q1_gold, q2_pred

def make_temp(q1_gold, q2_pred):
    temp = pd.DataFrame({'q1\tq2':[f"{q1_gold[i]}\t{q2_pred[i]}" for i in range(len(q1_gold))]})
    temp.to_csv('temp.csv',index=False) # create file to feed to call_semantic_similarity()

def call_semantic_similarity(input_file, url):
    file_name = os.path.basename(input_file)
    files = {
        'file': (file_name, open(input_file, mode='rb'), 'application/octet-stream')
    }
    resp = requests.post(url, files=files, params={'similarity_types': 'all'})
    s = json.loads(resp.json())
    return pd.DataFrame(s)

def retrieve_score_vals(i, col, score_df, eval_df):
    rows = score_df[(score_df['q1'] == eval_df['gold_qid'].iat[i]) & (score_df['q2'] == eval_df['pred_qid'].iat[i])]
    output = list(rows[col])
    if len(output) > 0:
        return output[0]
    else:
        return None

def get_class_score(score_df, id, tool_ent, gold_ent, q1_gold, q2_pred):

    # organize results
    eval_df = pd.DataFrame({'id':id, 'pred_ent':tool_ent, 'gold_ent':gold_ent,'gold_qid':q1_gold,'pred_qid':q2_pred, 'gold_label':range(len(id)), 'pred_label':range(len(id)),'class':range(len(id)), 'jc':range(len(id))})
    eval_df['gold_label'] = eval_df['gold_label'].apply(retrieve_score_vals, col='q1_label', score_df=score_df, eval_df=eval_df)
    eval_df['pred_label'] = eval_df['pred_label'].apply(retrieve_score_vals, col='q2_label', score_df=score_df, eval_df=eval_df)
    eval_df['class'] = eval_df['class'].apply(retrieve_score_vals, col='class', score_df=score_df, eval_df=eval_df)

    # Get highest scoring gold_qid-pred_qid for each pred_ent

    class_rows_to_keep = []
    
    for id in eval_df['id'].unique():
        for ent in eval_df[eval_df['id']==id]['pred_ent'].unique():
            rows = eval_df[(eval_df['id']==id) & (eval_df['pred_ent']==ent)]
            
            class_scores = [score for score in rows['class'] if score != None and score != "" and not(math.isnan(score))]
            if len(class_scores) > 0:
                idx = list(rows.index)[list(rows['class']).index(max(class_scores))]
                class_rows_to_keep.append(idx)

    class_score = eval_df.loc[class_rows_to_keep]['class'].dropna().mean()

    return class_score

def get_jc_score(score_df, id, tool_ent, gold_ent, q1_gold, q2_pred):

    # organize results
    eval_df = pd.DataFrame({'id':id, 'pred_ent':tool_ent, 'gold_ent':gold_ent,'gold_qid':q1_gold,'pred_qid':q2_pred, 'gold_label':range(len(id)), 'pred_label':range(len(id)),'class':range(len(id)), 'jc':range(len(id))})
    eval_df['gold_label'] = eval_df['gold_label'].apply(retrieve_score_vals, col='q1_label', score_df=score_df, eval_df=eval_df)
    eval_df['pred_label'] = eval_df['pred_label'].apply(retrieve_score_vals, col='q2_label', score_df=score_df, eval_df=eval_df)
    eval_df['jc'] = eval_df['jc'].apply(retrieve_score_vals, col='jc', score_df=score_df, eval_df=eval_df)

    # Get highest scoring gold_qid-pred_qid for each pred_ent

    jc_rows_to_keep = []

    for id in eval_df['id'].unique():
        for ent in eval_df[eval_df['id']==id]['pred_ent'].unique():
            rows = eval_df[(eval_df['id']==id) & (eval_df['pred_ent']==ent)]
            
            jc_scores = [score for score in rows['jc'] if score != None and score != "" and not(math.isnan(score))]
            if len(jc_scores) > 0:
                idx = list(rows.index)[list(rows['jc']).index(max(jc_scores))]
                jc_rows_to_keep.append(idx)

    jc_score = eval_df.loc[jc_rows_to_keep]['jc'].dropna().mean()

    return jc_score

def calculate_class_jc(gold_df, result_df, id_col, ent_col, qid_col, matching='STRONG', gold_set='PRIMARY', fill_in_qids=False, url='https://kgtk.isi.edu/similarity_api'):
    
    # Get all entity-link pair candidates for evaluation
    id, tool_ent, gold_ent, q1_gold, q2_pred = match_gold_pred(gold_df, result_df, id_col,ent_col,qid_col, matching, gold_set, fill_in_qids)
    
    # Call API
    make_temp(q1_gold, q2_pred)
    score_df = call_semantic_similarity('temp.csv', url)
    os.remove('temp.csv')
    
    # Get Scores
    class_score = get_class_score(score_df, id, tool_ent, gold_ent, q1_gold, q2_pred)
    jc_score = get_jc_score(score_df, id, tool_ent, gold_ent, q1_gold, q2_pred)

    return class_score, jc_score

def main(gs_path, result_path, id_col, ent_col, qid_col):

    gold_df = pd.read_csv(gs_path)
    print("Gold Standard")
    print(gold_df.head())
    result_df = pd.read_csv(result_path)
    print("Tool Output")
    print(result_df.head())
    tool_name = result_path.split('/')[-2]

    # Strong matching / primary GS setup
    print("Calculating scores for Strong Matching and Primary GS")
    print("F1...")
    strong_prec, strong_rec, strong_f1 = calculate_precision_recall_f1(gold_df, result_df, id_col, ent_col, qid_col, matching="STRONG", gold_set="PRIMARY", fill_in_qids=False)
    print("Semantic similarity...")
    strong_class, strong_jc = calculate_class_jc(gold_df, result_df, id_col, ent_col, qid_col, matching="STRONG", gold_set="PRIMARY", fill_in_qids=False)
    print("Done")

    # Weak matching / primary GS setup  
    print("Calculating scores for Weak Matching and Primary GS")
    print("F1...")
    weak_prec, weak_rec, weak_f1 = calculate_precision_recall_f1(gold_df, result_df, id_col, ent_col, qid_col, matching="WEAK", gold_set="PRIMARY", fill_in_qids=False)
    print("Semantic similarity...")
    weak_class, weak_jc = calculate_class_jc(gold_df, result_df, id_col, ent_col, qid_col, matching="WEAK", gold_set="PRIMARY", fill_in_qids=False)
    print("Done")

    # Strong matching / Extended GS setup
    print("Calculating scores for Strong Matching and Extended GS (Specific Entities w/o QIDs Given General QID)")
    print("F1...")
    ext_prec, ext_rec, ext_f1 = calculate_precision_recall_f1(gold_df, result_df, id_col, ent_col, qid_col, matching="STRONG", gold_set="EXTENDED", fill_in_qids=True)
    print("Semantic similarity...")
    ext_class, ext_jc = calculate_class_jc(gold_df, result_df, id_col, ent_col, qid_col, matching="STRONG", gold_set="EXTENDED", fill_in_qids=True)
    print("Done\n")

    scores_dict = {}
    scores_dict["Evaluation with Strong Matching and Primary GS"] = {"Precision":strong_prec, "Recall":strong_rec, "F1":strong_f1, "Class Sem. Sim.":strong_class, "JC Sem. Sim.":strong_jc}
    scores_dict["Evaluation with Weak Matching and Primary GS"] = {"Precision":weak_prec, "Recall":weak_rec, "F1":weak_f1, "Class Sem. Sim.":weak_class, "JC Sem. Sim.":weak_jc}
    scores_dict["Evaluation with Strong Matching and Extended GS\nSpecific Entities w/o QIDs Given General QID"] = {"Precision":ext_prec, "Recall":ext_rec, "F1":ext_f1, "Class Sem. Sim.":ext_class, "JC Sem. Sim.":ext_jc}
    print_results(tool_name, scores_dict)


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
        '-q', '--qid_col',
        type=str,
        required=False,
        default="qids",
        help='Name of column in results dataset which contains qids'
    )
    parser.add_argument(
        '-g', '--gs_path',
        type=str,
        required=False,
        default="../../gold_standard/processed/nel.csv",
        help='Path to NEL gold standard'
    )

    args = parser.parse_args()

    # call eval
    main(args.gs_path, args.dataset_path, args.id_col, args.ent_col, args.qid_col)