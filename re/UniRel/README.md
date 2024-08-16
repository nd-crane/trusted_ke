### UniRel Setup
  
[![Paper](https://img.shields.io/badge/Paper-Read%20Now-brightgreen?logo=academia)](https://arxiv.org/pdf/2211.09039.pdf) \
[![GitHub](https://img.shields.io/badge/GitHub-Repository-black?logo=github)](https://github.com/wtangdev/UniRel/tree/main)

Setup:

1. Created a python virtual env venv using python 3.8 and activate it

2. Clone the GitHub Respository

3. In the requiements.txt remove the "+cu101" on torch and torchvision

4. Install the requirements.txt `pip install -r requirements.txt`

5. Download the Data listed on the ReadMe of the UniRel repository

6. Run the script `python3.8 pretrain_setup.py` from the bert-base-cased directory  to download the bert model from HuggingFace 

7. Run the script `python3.8 unirel_faa.py` to run the UniRel NYT model on the FAA data

8. Do post-processing with unirel_reformat.ipynb
----------------------------
#### Reproducibility Rating:
<img src="../../figs/star_clip.jpg" alt="Star" width="50" height="50"><img src="../../figs/star_clip.jpg" alt="Star" width="50" height="50"><img src="../../figs/star_clip.jpg" alt="Star" width="50" height="50"><img src="../../figs/star_clip.jpg" alt="Star" width="50" height="50">

The UniRel GitHub README is easy to follow and is accuarate.
The requirements.txt is mostly accurate except for the changes required in step 3.
UniRel allows the user to pass in raw text as seen in their  predict.py
Only one additional argument (model) had to be passed into the UniRel class in order for unirel_faa.py to work.
