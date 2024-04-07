# Processing json files to CoNLL-12 format

format_conll.py: script which takes json data as input, puts the data into conll-12 format, and saves an output file called formatted.conll\
*Ex:* python format_conll.py faa.json .

*Experiment using obtained conll-2012 data:*\
msnbc_0004.conll: data from the trial release of conll-12, also located in data/conll-2012/trial/data/english/annotations/bc/msnbc/msnbc_0004.conll\
create_conll_raw.py: transforms msnbc_0004.conll to conll_raw.json, which takes out the formatting, parsing, and labeling elements of conll-12 data and stores the original, natural text in a json format\
conll_raw.json: original msnbc data formatted as a json file by create_conll_raw.py\
msnbc_formatted.conll: output of format_conll.py when run on conll_raw.json\
check_format_conll_acc.ipynb: notebook which compares the original msnbc_0004.conll data with the data created by format_conll.py to test accuracy of script

*FAA data formatting*
create_faa_json.py: transforms the faa data to a json file in the format expected by format_conll.py\
faa.json: output of create_faa_json.py\
faa.conll: output of format_conll.py when run on faa.json

faa.json and faa.conll also copied and saved in data/FAA_data