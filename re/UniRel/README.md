### UniRel Setup
  
Github: https://github.com/wtangdev/UniRel/tree/main

Paper: https://arxiv.org/pdf/2211.09039.pdf

Setup:

1. Created a python virtual env venv using python 3.8 and activate it

2. Clone the GitHub Respository

3. In the requiements.txt remove the "+cu101" on torch and torchvision

4. Install the requirements.txt `pip install -r requirements.txt`

5. Download the Data listed on the ReadMe of the UniRel repository

6. Run the script `python3.8 pretrain_setup.py` from the bert-base-cased directory  to download the bert model from HuggingFace 

7. TBD - reguarding running on NYT Dataset
----------------------------
#### Reproducibility Rating:
