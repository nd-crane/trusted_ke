import json
import pandas as pd
import re

# Load the CSV file
csv_file_path = '../../OMIn_dataset/data/FAA_data/Maintenance_Text_data_nona.csv'
df = pd.read_csv(csv_file_path)

# Extract the necessary columns
important_columns = df[['c5', 'c119']].copy()
important_columns.columns = ['id', 'sentence']  # Renaming for clarity

# Drop rows where 'sentence' is NaN
important_columns.dropna(subset=['sentence'], inplace=True)

# Generate test.source content
source_lines = []
for _, row in important_columns.iterrows():
    source_lines.append(f"Dataset : faa Task : Relation Extraction Sentence : {row['sentence']}")

source_content = "\n".join(source_lines)

# Save the source content to test.source file
source_file_path = 'test.source'
with open(source_file_path, 'w') as source_file:
    source_file.write(source_content)

# Improved tokenizer function
def improved_tokenize(text):
    # Tokenize the text while keeping punctuation and other characters
    return re.findall(r'\w+|[^\w\s]', text)

# POS tagging function (placeholder)
def simple_pos_tag(tokens):
    return ['NN'] * len(tokens)  # Simplified POS tagging

# Generate test.json content
json_data = []
for _, row in important_columns.iterrows():
    sentence = row['sentence']
    tokens = improved_tokenize(sentence)
    pos_tags = simple_pos_tag(tokens)
    
    entry = {
        "id": row['id'],
        "tokens": tokens,
        "spo_list": [],
        "spo_details": [],
        "pos_tags": pos_tags
    }
    json_data.append(entry)

# Save the JSON content to test.json file
json_file_path = 'test.json'
with open(json_file_path, 'w') as json_file:
    json.dump(json_data, json_file, indent=4)

json_file_path, source_file_path
