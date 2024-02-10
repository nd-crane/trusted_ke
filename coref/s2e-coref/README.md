### s2e-coref Setup

Github: https://github.com/yuvalkirstain/s2e-coref

Paper: https://aclanthology.org/2021.acl-short.3.pdf

Notes:\
conll_data is publically available trial data obtained from https://conll.cemantix.org/2012/data.html\
data is the folder used for FAA experiments\
test_data is the folder used to confirm the results of format_conll.py in recreating conll-formatted data.\
create_conll_raw_data.ipynb generates conll_raw.json from the data in conll_data. It reconstructs the original sentences in a normal, readable format.\
check_format_conll_acc.ipynb compares the results from running format_conll.py on conll_raw.json and the gold data in conll_data.

Setup:

1. Download requirements.txt from the github, create a python virtual enviornment and activate it, and run pip install -r requirements.txt

2. Process FAA dataset into conll format (May skip this step and use data in data folder if no interest in recreating results). Run format_conll.py ____ **** NOTE! EDIT format_conll.py SO THAT IT TAKES ARGUMENTS

3. Then minimize the conll data into jsonlines format using minimize.py from the github: python minimize.py data (May also skip this step and use the data in data folder)

4. 