# This script selects the 100 records used for eval from a result in data/results/tool_name, so that it can be downloaded and evaluated manually.

import pandas as pd
import argparse

def select_samples(result_df, samples, id_col):

    sampled_result_df = pd.DataFrame(columns=result_df.columns)
    for sample_no in samples:
        rows = result_df[result_df[id_col]==sample_no]
        sampled_result_df = pd.concat([sampled_result_df, rows], ignore_index=True)
    
    return sampled_result_df

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
        '-n', '--index_col',
        type=str,
        required=False,
        default="index",
        help='Name of column in input dataset which contains the index from Maintenance_Text_data_nona.csv'
    )
    parser.add_argument(
        '--use_indices',
        action='store_true',
        help='If true, it uses indices instead of the c5_id to select the samples'
    )
    parser.add_argument(
        '-s', '--sample_path',
        type=str,
        required=False,
        default="../../OMIn_dataset/data/FAA_data/FAA_sample_100.csv",
        help='Path to sample data'
    )
    parser.add_argument(
        '-o', '--output_folder',
        type=str,
        required=False,
        default="./",
        help='Folder in which to save output'
    )

    args = parser.parse_args()

    result_df = pd.read_csv(args.dataset_path)
    sample_df = pd.read_csv(args.sample_path)

    if args.use_indices:
        samples = list(sample_df['Unnamed: 0'])
        id_col = args.index_col
    else:
        samples = list(sample_df['c5'])
        id_col = args.id_col

    sampled_result_df = select_samples(result_df, samples, id_col)

    file_name = args.output_folder + args.dataset_path.split('/')[-1].split('.csv')[0]+'_eval.xlsx'
    with pd.ExcelWriter(file_name) as writer:
        sampled_result_df.to_excel(writer, sheet_name='sampled', index=False)
        result_df.to_excel(writer, sheet_name='raw_output', index=False)