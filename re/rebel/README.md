### REBEL Setup

Github: https://github.com/Babelscape/rebel

Paper: https://aclanthology.org/2021.findings-emnlp.204.pdf

Setup:

1. Created a python virtual env venv and activate it

2. Install torch as specified at https://pytorch.org/ under Install Pytorch

3. Got requirements.txt from the github, with wget https://raw.githubusercontent.com/Babelscape/rebel/main/requirements.txt

4. Change the == on the datasets line to <=, or you will encounter an error that datasets and transformers need different versions of huggingface-hub.

5. pip install -r requirements.txt

6. Run python scripts to obtain results. The pipe script uses Rebel as a component in a spacy pipeline, and takes longer
