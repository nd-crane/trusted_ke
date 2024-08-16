### Setup Process

[![Paper](https://img.shields.io/badge/Paper-Read%20Now-brightgreen?logo=academia)](https://arxiv.org/pdf/1911.03814.pdf) \
[![GitHub](https://img.shields.io/badge/GitHub-Repository-black?logo=github)](https://github.com/facebookresearch/BLINK)

1. Create a new conda environment named blink6, activate it, and run: conda env update --file environment.yml -n blink6

2. Add the blink repository with: git submodule add git@github.com:facebookresearch/BLINK.git

3. cd into BLINK

4. See step 2 in BLINK's git readme:\
    chmod +x download_blink_models.sh\
    ./download_blink_models.sh\

5. We skipped using the FAISS indexer.
    
6. Then move the main_dense.py script, since it needs to load the module blink without being inside of it:\
    mv blink/main_dense.py main_dense.py

7. BLINK takes in data in the following format:

       [ {\
                    "id": 0,\
                    "label": "unknown",\
                    "label_id": -1,\
                    "context_left": "".lower(),\
                    "mention": "Shakespeare".lower(),\
                    "context_right": "'s account of the Roman general Julius Caesar's murder by his friend Brutus is a meditation on duty.".lower(),\
                },\
                {\
                    "id": 1,\
                    "label": "unknown",\
                    "label_id": -1,\
                    "context_left": "Shakespeare's account of the Roman general".lower(),\
                    "mention": "Julius Caesar".lower(),\
                    "context_right": "'s murder by his friend Brutus is a meditation on duty.".lower(),\
                }\
                ]

In interactive mode, it uses a function called _annotate in main_dense.py to transform an input sentence to this form, which creates a dict for each mention found. Note that it uses flair for NER to locate these mentions. We created the script annotate_faa.py to utilize an edited version of _annotate to transform our data into this format and save it to a jsonl, faa_samples.jsonl. Since flair is trained to accept single sentences, we separate multi-sentence entries in FAA. To keep track of which sentence belongs to which FAA data entry/row, we added a "doc_idx" field to the dicts, by editing _annotate.

You can either recreate our results by running annotate_faa.py, or simply us the faa_samples.json provided.

9. Then, run run_blink.py. This script creates a blink_results.csv in tool_results. run_blink.py gets both the biencoder (fast) predictions as well as the crossencoder predictions. It also translates the wikipedia links which BLINK uses for NEL to wikidata QIDs, sync better with other NEL tools. Lastly, it stores the results to tool_results in a csv

----

#### Other Methods:

BLINK's repo also suggested installing with pip, as opposed to cloning the repo, using: pip install -e git+git@github.com:facebookresearch/BLINK#egg=BLINK

We did not have success running this since the command was missing the ssh and https specifications:
- pip install -e git+ssh://git@github.com:facebookresearch/BLINK#egg=BLINK
- pip install -e git+https://github.com/facebookresearch/BLINK#egg=BLINK

However, using these led to the error: Multiple top-level packages discovered in a flat-layout: ['elq', 'img', 'blink', 'elq_slurm_scripts'], since their setup.py script does not specify how to discover or organize these packages.

Try forking the repo and editing the setup.py script like so:
- line 8: from setuptools import setup, find_packages
- line 43: packages=find_packages(include=['blink*', 'elq*', 'img*'])

Be mindful that you still need to download the blink models.

----

#### Reproducibility Rating:

<img src="../../figs/star_clip.jpg" alt="Star" width="50" height="50"><img src="../../figs/star_clip.jpg" alt="Star" width="50" height="50"><img src="../../figs/star_clip.jpg" alt="Star" width="50" height="50"><img src="../../figs/star_clip.jpg" alt="Star" width="50" height="50">

*BLINK is deterministic.*

Although the documentation did not make it clear that we had to write our own annotation script to put data into the jsonl format, this was not a challenge to reproducibility, since the _annotate function was still relatively easy to find and implement.

Pros: BLINK is well-documented in all other respects than stated above, and the interactive version was very easy to use.

Cons: BLINK runs on python 3.7 and many other outdated dependencies. Its repo is now set to read-only by facebookresearch, so be mindful that it will not be receiving attention from its developers in the future. We were still able to get the environment working using conda.