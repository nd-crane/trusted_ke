### s2e-coref Setup

[![Paper](https://img.shields.io/badge/Paper-Read%20Now-brightgreen?logo=academia)](https://aclanthology.org/2021.acl-short.3.pdf) \
[![GitHub](https://img.shields.io/badge/GitHub-Repository-black?logo=github)](https://github.com/yuvalkirstain/s2e-coref)

1. git submodule add git@github.com:yuvalkirstain/s2e-coref.git

2. Create a python virtual enviornment and activate it, and run pip install -r s2e-coref/requirements.txt. You will also need to run pip install gitpython

3. Run setup.sh to grab faa.conll from data/FAA_data and copy it three times in the data folder, saved as <dev, train, test>.english.v4_gold_conll. We do not need train/test/dev splits because we are only using one set to evaluate, but minimze.py expects the folder to be laid out in this way

4. Run export DATA_DIR=data and export MODEL_DIR=model

5. Run python s2e-coref/minimze.py $DATA_DIR (transforms .conll data into jsonlines accepted by run_coref.py)

6. Change line 4 of modeling.py to from transformers.models.bert.modeling_bert import ACT2FN

7. In run_coref.py, add LongformerTokenizer to line 9, and replace line 90 with: tokenizer = LongformerTokenizer.from_pretrained(args.tokenizer_name, cache_dir=args.cache_dir) Otherwise it will load LongformerTokenizerFast, which causes an error in eval.py when it instantiates a BucketBatchSampler. Also comment out lines 148-151

9. Follow directions on github for evaluation. Note that you'll likely want to run run_coref.py within the s2e-coref folder, so you should make your environment variables point to the parent directory

10. Use interpret_predictions.ipynb to transform the raw results to a human readable csv, saved in tool_results/s2e-coref

-----

#### Reproducibility Rating:

<img src="../../figs/star_clip.jpg" alt="Star" width="50" height="50"><img src="../../figs/star_clip.jpg" alt="Star" width="50" height="50"><img src="../../figs/star_clip.jpg" alt="Star" width="50" height="50">

*s2e-coref is deterministic*

s2e-coref was easy to implement. The documentation on the github walks the newcomer through each step needed to prepare and run the model. requirements.txt was missing a few requirements, and the changes listed on #6 and #7 of the setup need to be implemented. However, those changes were simple to track down and likely due to software updates in the respective packages.

A larger issue was the preparation of our data into CoNLL-12 format. There is no standard open source method to process custom datasets into CoNLL-12 format, so the user must create their own script. Depending on which tagger and parser is used in the script, the CoNLL-12 formatted data will turn out differently. This introduces variability in results across implementations of s2e-coref.
