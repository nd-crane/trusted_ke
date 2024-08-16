### ReFinED Setup
[![Papers](https://img.shields.io/badge/Papers-Read%20Now-brightgreen?logo=academia)](https://arxiv.org/pdf/2207.04108.pdf) [![Papers](https://img.shields.io/badge/Papers-Read%20Now-brightgreen?logo=academia)](https://arxiv.org/pdf/2207.04106.pdf) \
[![GitHub](https://img.shields.io/badge/GitHub-Repository-black?logo=github)](https://github.com/amazon-science/ReFinED)

1. Get ReFinED
    1. `git clone git@github.com:amazon-science/ReFinED.git`
    2. `cd ReFined`
2. Setup Virtual Environment
    1. `virtualenv ReFined_venv`
    2. `source ReFined_venv/bin/activate`
    3. `pip install -r requirements.txt`
3. Add the src folder to your Python Path
    1. `export PYTHONPATH=$PYTHONPATH:src` (This temporarily puts it in your path)
4. Run the script to get ReFinED results
   1. `pip install pandas`
   2. `python3  refined_faa.py`
  
5. Do post-processing on results using reformat_refined.ipynb


Results are in the tool_results/refined folder
----------------------------

#### Reproducibility Rating:

<img src="../../figs/star_clip.jpg" alt="Star" width="50" height="50"><img src="../../figs/star_clip.jpg" alt="Star" width="50" height="50"><img src="../../figs/star_clip.jpg" alt="Star" width="50" height="50"><img src="../../figs/star_clip.jpg" alt="Star" width="50" height="50"><img src="../../figs/star_clip.jpg" alt="Star" width="50" height="50">

ReFinED is deterministic.
It is an easy and quick set up. It was accomplished by just following the Github README for ReFinED.
ReFinED also provided a sample script where the text could be directly passed into the model.
