import os
import requests
import json
import pandas as pd
import ast
import math
import argparse

def print_results(tool_name, scores_dict):

    scores = {setup:{metric:f"{float(scores_dict[setup][metric]):.2}" for metric in scores_dict[setup]} for setup in scores_dict}
    
    print('|                                         |Prec (Strong)|Rec (Strong)|F1 (Strong)|JC (Strong)|Class (Strong)|Prec (Weak)|Rec (Weak)|F1 (Weak)|JC (Weak)|Class (Weak)|Prec (Flex)|Rec (Flex)|F1 (Flex)|JC (Flex)|Class (Flex)|')
    print('|-----------------------------------------|-------------|------------|-----------|-----------|--------------|-----------|----------|---------|---------|------------|-----------|----------|---------|---------|------------|')
    print(f"| {tool_name:40}| {scores['strong']['Precision']:12}| {scores['strong']['Recall']:11}| {scores['strong']['F1']:10}| {scores['strong']['JC Sem. Sim.']:10}| {scores['strong']['Class Sem. Sim.']:13}| {scores['weak']['Precision']:10}| {scores['weak']['Recall']:9}| {scores['weak']['F1']:8}| {scores['weak']['JC Sem. Sim.']:8}| {scores['weak']['Class Sem. Sim.']:11}| {scores['flexible']['Precision']:10}| {scores['flexible']['Recall']:9}| {scores['flexible']['F1']:8}| {scores['flexible']['JC Sem. Sim.']:8}| {scores['flexible']['Class Sem. Sim.']:11}|")

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
    ''' Finds the indices of a match between an entity in gs_entities and an entity in tool_entities.
    Parameters:
    - gs_entities: list of primary, secondary, and tertiary spans for an entity. This is taken from a single cell in the gold standard csv
    - tool_entities: list of all entities found by a tool for a certain document.
    - matching: either "STRONG" or "WEAK". Strong match: ent1 == ent2. Weak match: ent1 in ent2 or ent2 in ent1
    - gold_set: either "PRIMARY" or "EXTENDED". Primary gold set: gs_entities is restricted to gs_entities[0]. Extended gold set: use full gs_entities.

    Returns:
    If an entity in gs_entities matches an entity in tool_entities, returns the respective indices of the first match, else returns (-1, -1)'''

    tool_entities = pd.Series(tool_entities)
    stop_idx = len(gs_entities) if gold_set == "EXTENDED" else 1

    for gold_idx in range(stop_idx):
        matches = tool_entities[tool_entities.apply(is_match, ent2 = gs_entities[gold_idx], matching=matching)]
        
        if len(matches) > 0:
            found_idx_ent = (gold_idx, gs_entities[gold_idx])
            return (gold_idx, matches.index.to_list()[0])
    
    return (-1,-1)

def prune_gold_set(gs_entities, gs_qids, gold_set, fill_in_qids):
    ''' Removes gold entity-qid links with either a None entity or a None QID.

    Parameters:
    - gs_entities: list of primary, secondary, and tertiary spans for an entity. This is taken from a single cell in the gold standard csv
    - gs_qids: list of QIDs for the primary, secondary, and tertiary spans for an entity, respectively. This is taken from a single cell in the gold standard csv
    - gold_set: either "PRIMARY" or "EXTENDED". Primary gold set: gs_entities is restricted to gs_entities[0]. Extended gold set: use full gs_entities.
    - fill_in_qids determines whether specific entities with no valid QID (eg, "left wing") are assigned the
    QIDs for a subspan (eg, "Q161358" for "wing") and kept in the gold set, or whether they are removed.

    Returns: tuple containing the pruned lists of entities and qids.
    
    The gold standard includes entitiy-qid links with None's, so that the user of this function may specify how they are removed:
    1. fill_in_qids = False : All links with no QID are removed. For example, if gs_entities = ["left wing","wing",None] and gs_qids = [None, "Q161358", None],
    ["wing"], ["Q161358"] would be returned.
    2. fill_in_qids = True : If a primary or secondary link has no QID, but a later link does, that later QID is used to fill in
    the missing QID of the more primary link. For example, if gs_entities = ["left wing","wing",None] and gs_qids = [None, "Q161358", None],
    this function would edit gs_qids to ["Q161358","Q161358",None] so that "left wing" and the QID for wing is a valid gold standard link.
    ["left wing","wing"], ["Q161358","Q161358"] would be returned. Note that this almost always results in the same affect as setting matching="WEAK".
    '''

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

def calculate_precision_recall_f1(gs, df_tool, qid_col, matching='WEAK', gold_set='PRIMARY', fill_in_qids=False):
    """
    Calculate precision, recall, and F1 based on entity-qid links comparison between gs (ground truth) and df_tool (answers).
    
    Parameters:
    - gs: DataFrame with columns ['id', 'sample', 'entities','qids'] representing the ground truth.
    - df_tool: DataFrame with columns ['c5_id', 'mentions', qid_col] representing the tool's answers.
    - qid_col is the column names used in df_tool for the QIDs
    - matching may be "WEAK" or "STRONG". Strong matching counts an entity-link pair as correct if the entity
    exactly matches the entity in the gold standard, and the links are the same. Weak matching counts it as
    correct if the entity overlaps with the entity in the gold standard, and the links are the same.
    - gold_set may be "PRIMARY" or "EXTENDED". The primary set of gold standard entity-link pairs are those in
    the columns beginning with "primary" in the gold standard. The extended gold standard includes secondary
    and tertiary entity-link pairs, which attempt to account for variability in entity-tagging by providing correct
    links for other possible spans for each entity where applicable.
    - fill_in_qids determines whether specific entities with no valid QID (eg, "left wing") are assigned the
    QIDs for a subspan (eg, "Q161358" for "wing") and kept in the gold set, or whether they are removed.
    
    Returns:
    - A tuple containing precision, recall, and F1.
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

        selected_rows = df_tool[df_tool['c5_id'] == gs_id][qid_col].dropna().index # select rows in df_tool which have same docid as gsid, and there is a QID for the entity in the row
        tool_entities = [entity.upper() for entity in df_tool.loc[selected_rows]['mentions']] # get all the entities the tool generated for the gs_id entry
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

def match_gold_pred(gs, df_tool, qid_col, matching, gold_set, fill_in_qids):

    '''
    Returns 5 equal-length lists representing intersection between gold standard entity-qid links and tool-predicted entity-qid links where entities match and qids are present.

    Parameters:
    - gs: DataFrame with columns ['id', 'sample', 'entities','qids'] representing the ground truth.
    - df_tool: DataFrame with columns ['c5_id', 'mentions', qid_col] representing the tool's answers.
    - qid_col is the column names used in df_tool for the QIDs
    - matching may be "WEAK" or "STRONG". Strong matching counts an entity-link pair as correct if the entity
    exactly matches the entity in the gold standard, and the links are the same. Weak matching counts it as
    correct if the entity overlaps with the entity in the gold standard, and the links are the same.
    - gold_set may be "PRIMARY" or "EXTENDED". The primary set of gold standard entity-link pairs are those in
    the columns beginning with "primary" in the gold standard. The extended gold standard includes secondary
    and tertiary entity-link pairs, which attempt to account for variability in entity-tagging by providing correct
    links for other possible spans for each entity where applicable.
    - fill_in_qids determines whether specific entities with no valid QID (eg, "left wing") are assigned the
    QIDs for a subspan (eg, "Q161358" for "wing") and kept in the gold set, or whether they are removed.

    Returns: 5 equal-length lists (columns), where the entries across the same indices in each column make up a single match between
    a gold and a predicted entity-qid link.
    - id: doc ids (c5 ids)
    - gold_ent: gold entities
    - tool_ent: tool-predicted entities
    - q1_gold: gold QIDs
    - q2_pred: tool-predicted QIDs
    '''
    
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
        
        selected_rows = df_tool[df_tool['c5_id'] == gs_id][qid_col].dropna().index # select rows in df_tool which have same docid as gsid, and there is a QID for the entity in the row
        tool_entities = [entity.upper() for entity in df_tool.loc[selected_rows]['mentions']] # get all the entities the tool generated for the gs_id entry
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
    ''' 
    Creates temporary csv to send to https://kgtk.isi.edu/similarity_api similarity API
    '''
    temp = pd.DataFrame({'q1\tq2':[f"{q1_gold[i]}\t{q2_pred[i]}" for i in range(len(q1_gold))]})
    temp.to_csv('temp.csv',index=False) # create file to feed to call_semantic_similarity()

def call_semantic_similarity(input_file, url):
    '''
    Call to similarity API (if url is set to https://kgtk.isi.edu/similarity_api)
    input file should be path to temp.csv created in make_temp()
    Returns a dataframe of score information with columns ['q1', 'q2', 'q1_label', 'q2_label', 'class',  'jc']
    '''
    file_name = os.path.basename(input_file)
    files = {
        'file': (file_name, open(input_file, mode='rb'), 'application/octet-stream')
    }
    resp = requests.post(url, files=files, params={'similarity_types': 'all'})
    s = json.loads(resp.json())
    return pd.DataFrame(s)

def retrieve_score_vals(i, col, score_df, eval_df):
    '''
    Score_df contains information about a subset of entries in eval_df.
    This function returns the information in score_df for the column col for the pair of gold and pred qids found in row i in eval_df.
    It returns None if the pair of gold and pred qids is not present in score_df.
    '''
    rows = score_df[(score_df['q1'] == eval_df['gold_qid'].iat[i]) & (score_df['q2'] == eval_df['pred_qid'].iat[i])]
    output = list(rows[col])
    if len(output) > 0:
        return output[0]
    else:
        return None

def get_class_score(score_df, id, tool_ent, gold_ent, q1_gold, q2_pred):
    ''' This function gets the unweighted average (micro) Class similarity score for all evaluated entity-qid links in the predicted set.
    It ignores all links where a class score could not be calculated.

    Parameters:
    - score_df: dataframe outputted by call_semantic_similarity()
    - id, tool_ent, gold_ent, q1_gold, q2_pred: Equal length lists outputted by match_gold_pred() representing the intersection between gold
    standard entity-qid links and tool-predicted entity-qid links where entities match and qids are present.

    Returns: class similarity score
    '''

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
    ''' This function gets the unweighted average Jiang Conrath (JC) metric for all evaluated entity-qid links in the predicted set.
    It ignores all links where a class score could not be calculated.

    Parameters:
    - score_df: dataframe outputted by call_semantic_similarity()
    - id, tool_ent, gold_ent, q1_gold, q2_pred: Equal length lists outputted by match_gold_pred() representing the intersection between gold
    standard entity-qid links and tool-predicted entity-qid links where entities match and qids are present.

    Returns: JC score
    '''

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

def calculate_class_jc(gold_df, result_df, qid_col, matching='STRONG', gold_set='PRIMARY', fill_in_qids=False, url='https://kgtk.isi.edu/similarity_api'):
    '''
    Calculate class similarity score and JC metric based on entity-qid link comparison between gs (ground truth) and df_tool (answers).
    
    Parameters:
    - gs: DataFrame with columns ['id', 'sample', 'entities','qids'] representing the ground truth.
    - df_tool: DataFrame with columns ['c5_id', 'mentions', qid_col] representing the tool's answers.
    - qid_col is the column names used in df_tool for the QIDs
    - matching may be "WEAK" or "STRONG". Strong matching counts an entity-link pair as correct if the entity
    exactly matches the entity in the gold standard, and the links are the same. Weak matching counts it as
    correct if the entity overlaps with the entity in the gold standard, and the links are the same.
    - gold_set may be "PRIMARY" or "EXTENDED". The primary set of gold standard entity-link pairs are those in
    the columns beginning with "primary" in the gold standard. The extended gold standard includes secondary
    and tertiary entity-link pairs, which attempt to account for variability in entity-tagging by providing correct
    links for other possible spans for each entity where applicable.
    - fill_in_qids determines whether specific entities with no valid QID (eg, "left wing") are assigned the
    QIDs for a subspan (eg, "Q161358" for "wing") and kept in the gold set, or whether they are removed.
    - url: url to API to calculate semantic similarity metrics.
    
    Returns:
    - A tuple containing the class and jc scores.
    '''
    
    # Get all entity-link pair candidates for evaluation
    id, tool_ent, gold_ent, q1_gold, q2_pred = match_gold_pred(gold_df, result_df, qid_col, matching, gold_set, fill_in_qids)
    
    # Call API
    make_temp(q1_gold, q2_pred)
    score_df = call_semantic_similarity('temp.csv', url)
    os.remove('temp.csv')
    
    # Get Scores
    class_score = get_class_score(score_df, id, tool_ent, gold_ent, q1_gold, q2_pred)
    jc_score = get_jc_score(score_df, id, tool_ent, gold_ent, q1_gold, q2_pred)

    return class_score, jc_score

def main(gs_path, result_path, qid_col):

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
    strong_prec, strong_rec, strong_f1 = calculate_precision_recall_f1(gold_df, result_df, qid_col, matching="STRONG", gold_set="PRIMARY", fill_in_qids=False)
    print("Semantic similarity...")
    strong_class, strong_jc = calculate_class_jc(gold_df, result_df, qid_col, matching="STRONG", gold_set="PRIMARY", fill_in_qids=False)
    print("Done")

    # Weak matching / primary GS setup  
    print("Calculating scores for Weak Matching and Primary GS")
    print("F1...")
    weak_prec, weak_rec, weak_f1 = calculate_precision_recall_f1(gold_df, result_df, qid_col, matching="WEAK", gold_set="PRIMARY", fill_in_qids=False)
    print("Semantic similarity...")
    weak_class, weak_jc = calculate_class_jc(gold_df, result_df, qid_col, matching="WEAK", gold_set="PRIMARY", fill_in_qids=False)
    print("Done")

    # Strong matching / Extended GS setup
    print("Calculating scores for Flexible GS (strong matching)")
    print("F1...")
    ext_prec, ext_rec, ext_f1 = calculate_precision_recall_f1(gold_df, result_df, qid_col, matching="STRONG", gold_set="EXTENDED", fill_in_qids=False)
    print("Semantic similarity...")
    ext_class, ext_jc = calculate_class_jc(gold_df, result_df, qid_col, matching="STRONG", gold_set="EXTENDED", fill_in_qids=False)
    print("Done\n")

    scores_dict = {}
    scores_dict["strong"] = {"Precision":strong_prec, "Recall":strong_rec, "F1":strong_f1, "Class Sem. Sim.":strong_class, "JC Sem. Sim.":strong_jc}
    scores_dict["weak"] = {"Precision":weak_prec, "Recall":weak_rec, "F1":weak_f1, "Class Sem. Sim.":weak_class, "JC Sem. Sim.":weak_jc}
    scores_dict["flexible"] = {"Precision":ext_prec, "Recall":ext_rec, "F1":ext_f1, "Class Sem. Sim.":ext_class, "JC Sem. Sim.":ext_jc}
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
        default="../../OMIn_dataset/gold_standard/processed/nel.csv",
        help='Path to NEL gold standard'
    )

    args = parser.parse_args()

    # call eval
    main(args.gs_path, args.dataset_path, args.qid_col)