### s2e-coref Setup

Github: https://github.com/yuvalkirstain/s2e-coref

Paper: https://aclanthology.org/2021.acl-short.3.pdf

1. git submodule add git@github.com:yuvalkirstain/s2e-coref.git

2. Create a python virtual enviornment and activate it, and run pip install -r s2e-coref/requirements.txt. You will also need to run pip install gitpython

3. Run setup.sh to grab faa.conll from data/FAA_data and copy it three times in the data folder, saved as <dev, train, test>.english.v4_gold_conll. We do not need train/test/dev splits because we are only using one set to evaluate, but minimze.py expects the folder to be laid out in this way

4. Run export DATA_DIR=data and export MODEL_DIR=model

5. Run python s23-coref/minimze.py (transforms .conll data into jsonlines accepted by run_coref.py)

6. Change line 4 of modeling.py to from transformers.models.bert.modeling_bert import ACT2FN

7. In run_coref.py, add LongformerTokenizer to line 9, and replace line 90 with: tokenizer = LongformerTokenizer.from_pretrained(args.tokenizer_name, cache_dir=args.cache_dir) Otherwise it will load LongformerTokenizerFast, which causes an error in eval.py when it instantiates a BucketBatchSampler

8. Follow directions on github for evaluation

9. It'll error on eval.py line 139 but it doesn't matter since it will have completed creating output/preds.jsonl

10. Use interpret_predictions.ipynb to transform the raw results to a human readable csv, saved in data/results/s2e-coref