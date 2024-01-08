### Setup Process

Github: https://github.com/facebookresearch/BLINK?tab=readme-ov-file
Paper: https://arxiv.org/pdf/1911.03814.pdf

1. Create a new conda environment named blink6, activate it, and run: conda env update --file environment.yml -n blink6

2. Add the blink repository with: git submodule add git@github.com:facebookresearch/BLINK.git

3. cd into BLINK

4. See step 2 in BLINK's git readme:\
    chmod +x download_blink_models.sh\
    ./download_blink_models.sh\
    
5. Then move the main_dense.py script, since it needs to load the module blink without being inside of it:\
    mv blink/main_dense.py main_dense.py

6. If you want to recreate faa_samples.jsonl, run annotate_faa.py. It converts the faa data into the jsonl format which blink expects. The NER tool which blink uses, flair, treats all sentences independently. Because of this, annotate_faa.py seperates each sentence in the FAA data and compiles one long consecutive list (losing the "doc" structure of seperating each entry). To keep track of which sentence belongs to which FAA data entry/row, see the "doc_idx" field in faa_samples.jsonl

7. Then, run run_blink.py. This script creates a blink_results.csv in data/results