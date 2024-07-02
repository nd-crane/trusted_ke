# This script checks whether the results generated from the noisy data have differences

import pandas as pd
import os
import argparse
import os

ORIGINAL = 'c119'
VARIANTS = ['c119_strip', 'c119_spaceafter',
       'c119_leadapost', 'c119_leadtrailapost', 'c119_lowerletter',
       'c119_lowerword', 'c119_lower']

# Many of the results dfs have several output columns and several rows of output for each unique input. This function condenses the df to
# simply have one result cell per input, in the form "[{col1:datpoint, col2:datapoint} , {col1:datpoint, col2:datapoint}, {col1:datpoint, col2:datapoint}]"
# where each dict represents a row and each key,value pair in the dict represents a column
def condense_df(df, id_col, cols_to_condense, condensed_name):
    cols_to_keep = list(df.columns)
    for col in cols_to_condense:
        cols_to_keep.remove(col)
    condensed_dict = {col:[] for col in cols_to_keep+[condensed_name]}
    ids = list(df[id_col].unique())
    for id in ids:
        # Get section of dataframe with same id (in case of FAA data, all the entries which may have the same c5 id, and different (head,relation,tail) etc)
        id_entries = df[df[id_col] == id]
        # Copy over data that will remain the same
        for col in cols_to_keep:
            condensed_dict[col].append(id_entries[col].iat[0])
        # Condense cols to condense
        condensed_str = "["
        for i in range(len(id_entries)):
            condensed_str = condensed_str + "{"
            for col in cols_to_condense:
                condensed_str = condensed_str + f"{col}:{id_entries[col].iat[i]}, "
            condensed_str = condensed_str + "}"
        condensed_str = condensed_str + "]"
        condensed_dict[condensed_name].append(condensed_str)

    return pd.DataFrame(condensed_dict)        

def main(directory, id_col, output_cols):

    original_df = condense_df(pd.read_csv(f"{directory}/{ORIGINAL}.csv"), id_col, output_cols, 'c119_output')
    
    # initialize out_dict
    out_dict = {col:list(original_df.to_dict()[col].values()) for col in original_df.columns}
    for variant in VARIANTS:
        out_dict[f'{variant}_output'] = [' ']*len(out_dict[id_col])

    # Check each variant for differences
    for variant in VARIANTS:
        variant_df = condense_df(pd.read_csv(f"{directory}/{variant}.csv"), id_col, output_cols, 'output')

        # check length mismatch
        if len(variant_df) != len(original_df):
            print(f"Error: {variant}.csv a different length than {ORIGINAL}.csv")
            return None

        # check for differences, if found, populate out_dict
        for i in range(len(variant_df)):
            if variant_df['output'].iat[i] != original_df['c119_output'].iat[i]:
                out_dict[f'{variant}_output'][i] = variant_df['output'].iat[i]            
    
    return out_dict

if __name__=='__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-d', '--directory',
        type=str,
        required=True,
        help='Name of directory which has csvs of which to check diff'
    )
    parser.add_argument(
        '-i', '--id_col',
        type=str,
        required=False,
        default='c5_id',
        help='Column with unique identifier'
    )
    parser.add_argument(
        '-c', '--output_cols',
        type=str,
        required=True,
        help='Columns with output from tool. Listed as col1/col2/col3'
    )

    args = parser.parse_args()

    err = False

    if not os.path.isdir(args.directory):
        print("Error: Invalid directory")
        err = True

    elif not os.path.isfile(f"{args.directory}/{ORIGINAL}.csv"):
        print(f"Error: No {ORIGINAL}.csv in directory {args.directory}")
        err = True

    for variant in VARIANTS:
        if not os.path.isfile(f"{args.directory}/{variant}.csv"):
            print(f"Error: No {variant}.csv in directory {args.directory}")
            err = True

    if not err:
        output_cols = args.output_cols.split('/')
        out_dict = main(args.directory, args.id_col, output_cols)

        pd.DataFrame(out_dict).to_csv(f"{args.directory}/diff.csv",index=False)

    