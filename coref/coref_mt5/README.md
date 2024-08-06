### Coref_MT5 Setup

Github: https://github.com/google-research/google-research/tree/master/coref_mt5

Paper: https://aclanthology.org/2023.tacl-1.13.pdf

If you look at colabs/coreference_decoder.ipynb in the coref_mt5 repo, you will see that the function to load the model and run inferences is not implemented. We found a very helpful repository created by ianporada on Github, https://github.com/ianporada/mt5_coref_pytorch, which organizes the code in the notebook and fills in the missing model-implementation in Pytorch.

Note that the main.py included in this folder is an adaptation of his main.py; do not overwrite this main.py with the one from mt5_coref_pytorch.

1. git submodule add git@github.com:ianporada/mt5_coref_pytorch.git

2. [TO-DO] -- Priscila, can you add what you did for environment resolution?

4. Run the code in json_to_jsonl.ipynb to get the FAA data to a jsonl file compatible with ianporada's script.

5. Run main.py

6. Do post-processing on coref_mt5_raw.csv with coref_mt5_refomat.ipynb. This will transform the data to a form readable by the evaluation script.

-----

#### Reproducibility Rating:

<img src="../../star_clip.jpg" alt="Star" width="50" height="50"><img src="../../star_clip.jpg" alt="Star" width="50" height="50">

*Coref_mt5 is deterministic* [TO-DO -- we don't technically know this]

Google Research's coref_mt5 folder lacks any detail which can be used to guide the user to either start an mt5 server, as it says, or use the model checkpoint with the appropriate tokenizers, config, etc. Some of these answers can be determined by a careful reading of the paper, but some remains unclear.  [TO-DO -- Priscila, do you have anything to add?]
