### Coref_MT5 Setup

[![Paper](https://img.shields.io/badge/Paper-Read%20Now-brightgreen?logo=academia)](https://arxiv.org/pdf/2211.12142v1.pdf) \
[![GitHub](https://img.shields.io/badge/GitHub-Repository-black?logo=github)](https://github.com/google-research/google-research/tree/master/coref_mt5)

If you look at `colabs/coreference_decoder.ipyn` in the **coref_mt5** repo, you will see that the function to load the model and run inferences is not implemented. 
We found a very helpful repository created by ianporada on Github, [https://github.com/ianporada/mt5_coref_pytorch](https://github.com/ianporada/mt5_coref_pytorch), which organizes the code in the notebook and fills in the missing model implementation in Pytorch.

Note that the main.py included in this folder is an adaptation of his main.py; do not overwrite this main.py with the one from mt5_coref_pytorch.

1. **Setup the environment**
   
   - Create a virtual environment with python=3.10, activate it, and install packages in the requirements.txt:
     
     ```bash
     python3.10 -m venv .venv
     source .venv/bin/activate
     pip install -r requirements.txt
     ```
    
   - Add [ianporada](https://github.com/ianporada/mt5_coref_pytorch) GitHub repo as a submodule and initialize it as follows:
     
     ```bash
     git submodule add git@github.com:ianporada/mt5_coref_pytorch.git
     git submodule update --init --recursive
     ```

2. **Preprocessing FAA data**\
First, run the `coref_mt5_refomat.ipynb` notebook to process the FAA Data and produce the `json` file. Next, execute the `json_to_jsonl.ipynb` notebook to convert the `json` file into the `jsonl` format compatible with ianporada's script. Ensure you run the notebooks in this order for correct data formatting.
That should produce the file `faa.jsonl`.

3. **Run the main script**
   ```bash
   python main.py --input_fname faa.jsonl
   ```
4. **Prepare the output data for the evaluation script**\
   Post-processing `coref_mt5_raw.csv` using the `coref_mt5_refomat.ipynb` notebook.
   This will transform the raw CSV data into a format that's compatible with our evaluation script.
 


-----

#### Reproducibility Rating:

<img src="../../figs/star_clip.jpg" alt="Star" width="50" height="50"><img src="../../figs/star_clip.jpg" alt="Star" width="50" height="50">

*Coref_mt5 is deterministic*

The [coref_mt5 folder](https://github.com/google-research/google-research/tree/master/coref_mt5) in Google Research lacks detailed instructions to guide users in starting an mt5 server or using the model checkpoint with the appropriate tokenizers and configurations. While some of these details can be inferred from the corresponding paper, certain aspects remain unclear. Although a [T5X checkpoint](https://console.cloud.google.com/storage/browser/gresearch/correference_seq2seq/checkpoint_1140000;tab=objects?pli=1&prefix=&forceOnObjectsSortingFiltering=false) from their top-performing mT5 model is publicly available, we encountered issues when attempting to load it due to the lack of configuration details. To address this, we utilized the PyTorch-converted version of the T5X checkpoint, which was made available by Ian Porada on HuggingFace [link-append-xxl](https://huggingface.co/ianporada/link-append-xxl) and is used in his GitHub repository.
