import pandas as pd

FAA_data = pd.read_csv("../../data/FAA_data/Maintenance_Text_data.csv")

textcol = "c119"
text_data = FAA_data[textcol]

# Remove empty rows
drop_rows = []
for irow in range(len(text_data)):
    if len(text_data[irow].split()) < 2:
        drop_rows.append(irow)
        
text_data = text_data.drop(drop_rows)
drop_data = FAA_data.drop(drop_rows)
drop_data.to_csv("../../data/FAA_data/Maintenance_Text_data_nona.csv")