# This script selects 1000 random records to do a supplementary evaluation on pl-marker (bert), and adds them to a new sheet in pl-marker_ace05_bert_RE_jun17_eval.xlsx, so that it can be downloaded and evaluated qualitatively.

import pandas as pd
import numpy as np

data_df = pd.read_csv("../../OMIn_dataset/data/FAA_data/Maintenance_Text_data_nona.csv")
result_df = pd.read_csv("../../tool_results/pl-marker/pl-marker_ace05_bert_RE_jun17.csv")

sample_c5s = np.random.choice(data_df["c5"], size=1000, replace=False)

sample_df = result_df[result_df['c5_id'].isin(sample_c5s)]
    
with pd.ExcelWriter("pl-marker_ace05_bert_RE_jun17_eval.xlsx", "a") as writer:
    sample_df.to_excel(writer, sheet_name='1000_docs_eval', index=False)