import pandas as pd
import os

# All original downloaded data resides here:
path_to_downloads = '../../data/FAA_data/downloads/'

# Get set of columns for each dataset so that we can find the common columns on which to concatenate data
columns = []
for file in os.listdir(path_to_downloads):
    if file[0] == 'a':
        columns.append(pd.read_csv(path_to_downloads+file, dtype='str').columns)
columns = [list(column_set) for column_set in columns]

column_dict = {}
for icolumn_set, column_set in enumerate(columns):
    for column in column_set:
        column_dict[column] = column_dict.get(column, []) + [icolumn_set]

common_cols = []
for col in column_dict:
    if len(column_dict[col]) == 10:
        common_cols.append(col)

# Concatenate data and save to concat_df
concat_df = pd.DataFrame()
columns = []
for file in os.listdir(path_to_downloads):
    if file[0] == 'a':
        new_df = pd.read_csv(path_to_downloads+file, dtype='str')[common_cols]
        concat_df = pd.concat([concat_df, new_df], axis=0)

# Select entries which have to do with maintenance incidents:s

# Codes signifying events which have to do with maintenance:
#AF: IMPROPER MAINTENANCE APT FAC
#DE: DEFIC, CO MAINTAIN EQUIP/SERV
#AI: INADEQUATELY MAINTAIN AWY FAC
#AP: INADEQUATELY MAINTAINA PCH FAC
#AU: ATTEMPT OPERATION WITH DEF EQP
#EQ: IMPROPER OPERATION EMEG/EQUIP
#II: INADEQUATE INSP OF AC PREFLT
#ME: FAIL/INCORRECT USE MISC EQUIP
# see ../FAA_data/downloads/AIDCODE.csv for all codes and descriptions
maintenance_codes = ['AF', 'DE', 'AI', 'AP', 'AU', 'EQ', 'II', 'ME']

concat_df = concat_df[concat_df['c78'].isin(maintenance_codes)]

concat_df.to_csv('../../data/FAA_data/Maintenance_Text_data.csv')