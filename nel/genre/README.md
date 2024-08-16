### GENRE Setup
[![Paper](https://img.shields.io/badge/Paper-Read%20Now-brightgreen?logo=academia)](https://arxiv.org/pdf/2010.00904.pdf) \
[![GitHub](https://img.shields.io/badge/GitHub-Repository-black?logo=github)](https://github.com/facebookresearch/GENRE)

0. If not already in the genre directory:
    1. `mkdir genre`
    2. `cd genre`
1. Create Environment:
    1. `python3.8 -m venv genre_venv`
    2. `source genre_venv/bin/activate`
    3. `pip install wheel`
2. Install Fairseq
    1. `git clone git@github.com:psaboia/fairseq.git`
    2. `cd fairseq`
    3.  `pip install --editable ./`
    4.  `cd -`
3. Install other dependencies
   1. `pip install transformers`
   2. `pip install BeautifulSoup4`
4. Install GENRE
   1. `git clone  git@github.com:facebookresearch/GENRE.git`
   2. `cd GENRE`
   3. `pip install --editable ./`
   4. `cd -`
5. Download Model
   1. `mkdir model`
   2. `cd model`
   3. `wget http://dl.fbaipublicfiles.com/GENRE/fairseq_e2e_entity_linking_aidayago.tar.gz`
   4. `tar -xf fairseq_e2e_entity_linking_aidayago.tar.gz`
   5. `cd -`
6. Run the script to output the GENRE Results
   1. `pip install pandas`
   2. `python3.8 genre_faa.py`
  
7. Use genre_reformat.ipynb to do post-processing on results

Results are in the data/results/genre folder
----------------------------

#### Reproducibility Rating:

<img src="../../figs/star_clip.jpg" alt="Star" width="50" height="50"><img src="../../figs/star_clip.jpg" alt="Star" width="50" height="50">

GENRE is not deterministic. Each sentence has to be separately trained in the model. Therefore, it takes a long time just to run the results with the model.

GENRE also relies on Fairseq and changes needed to be made to Fairseq so that it could integrate with GENRE. That is why we cloned our forked version of Fairseq in step 2 of the setup process.
