### Setup Process

Github: https://github.com/thunlp/PL-Marker/tree/master?tab=readme-ov-file

Paper: https://arxiv.org/pdf/2109.06067.pdf

1. Create a python virtual environment inside pl-marker and activate

2. Clone the PL-Marker git repo

3. See setup instructions in github README:
    1. Perform these commands as listed, while venv is activated:
        pip3 install -r requirement.txt
        pip3 install --editable ./transformers

    2. No need to set up apex since we are not retraining the models. Also note that apex requires GPUs on your machine and cuda to be installed

    3. Download the SciERC dataset from https://cloud.tsinghua.edu.cn/d/7dafc9a3d84d4151a755/ (optional -- only necessary if you want to run the model on that dataset to confirm their results). If you do not do this, at least create a directory called scierc in PL-Marker, since the data in step 3 will be saved there.

    4. Download trained models from https://cloud.tsinghua.edu.cn/d/5e4a117bc0e5407b9cee/ . Specifically sciner-scibert and scire-scibert

    5. Follow these commands listed under training script, in the directory above PL-Marker:

        mkdir -p bert_models/scibert_scivocab_uncased
        wget -P bert_models/scibert_scivocab_uncased https://huggingface.co/allenai/scibert_scivocab_uncased/resolve/main/pytorch_model.bin
        wget -P bert_models/scibert_scivocab_uncased https://huggingface.co/allenai/scibert_scivocab_uncased/resolve/main/vocab.txt
        wget -P bert_models/scibert_scivocab_uncased https://huggingface.co/allenai/scibert_scivocab_uncased/resolve/main/config.json

        However, change scibert_scivocab_uncased to scibert_uncased

    5. Create a directory in PL-Marker called sciner_models, and copy or move sciner-scibert there. Create a directory in PL-Marker called scire_models, and copy or move scire-scibert there.

    6. Note the commands in the Quick Start section. Optional - if you downloaded the scierc dataset, you can paste these commands to evaluate the model on that dataset and confirm their results.

4. Create JSONL formatted data for the input. See create_jsonl_data.ipynb. That notebook transforms the FAA data to JSONL format and saves it in PL-Marker/scierc. Alternatively, use the .json file already created, now in pl-marker, and move to pl-marker/PL-Marker/scierc

5. Copy sciner_models/sciner-scibert to sciner_models/sciner-scibert_faa

6. Copy scire_models/scire-scibert to scire_models/scire-scibert_faa

Your directory tree from pl-marker should look like this:
.\
├── bert_models\
│   └── scibert-uncased\
│       ├── config.json\
│       ├── pytorch_model.bin\
│       └── vocab.txt\
└── PL-Marker\
    ├── LICENSE\
    ├── README.md\
    ├── conll.py\
    ├── figs\
    │   └── overview.jpg\
    ├── preprocess_ontonotes.py\
    ├── requirement.txt\
    ├── run_acener.py\
    ├── run_levitatedpair.py\
    ├── run_ner.py\
    ├── run_ner_BIO.py\
    ├── run_re.py\
    ├── run_re_unidirect.py\
    ├── scierc\
    │   ├── dev.json\
    │   ├── faa_eval_faa.json\
    │   ├── test.json\
    │   └── train.json\
    ├── sciner_models\
    │   └── sciner-scibert-faa\
    │       ├── config.json\
    │       ├── ent_pred_test.json\
    │       ├── pytorch_model.bin\
    │       ├── results.json\
    │       ├── special_tokens_map.json\
    │       ├── tokenizer_config.json\
    │       ├── training_args.bin\
    │       └── vocab.txt\
    ├── scire_models\
    │   └── scire-scibert-faa\
    │       ├── config.json\
    │       ├── pred_results.json\
    │       ├── pytorch_model.bin\
    │       ├── results.json\
    │       ├── special_tokens_map.json\
    │       ├── tokenizer_config.json\
    │       ├── training_args.bin\
    │       └── vocab.txt\
    ├── scripts\
    │   ├── ...\
    ├── sumup.py\
    └── transformers\
        ├── ...

7. Change the following lines in run_acener.py. Because we do not have correct 'ner' labels in the faa_eval_faa.json files, when it tries to calculate an f1 score, it runs into a divide by zero error. Changing these lines will avoid that:
    1. Comment out 751-763 (from "precision_score ..." to "logger.info...")
    2. Replace results with None on line 783
    3. Comment out 1070-1076 (from "result =..." to "logger.info...")

8. Do a similar process on run_re.py
    1. Comment out 998-1014 (from "ner_p =..." to "logger.info")
    2. Replace results with None on line 1016
    3. Comment out 1316-1329 (from "result =..." to "json.dump")

9. Run these commands for each task. Note that NER has to complete before you can do RE. Note that the NER task can take about an hour and a half, while RE takes about 20 minutes.

NER:

CUDA_VISIBLE_DEVICES=0  python3  run_acener.py  --model_type bertspanmarker  \
    --model_name_or_path  ../bert_models/scibert-uncased  --do_lower_case  \
    --data_dir scierc  \
    --learning_rate 2e-5  --num_train_epochs 50  --per_gpu_train_batch_size  8  --per_gpu_eval_batch_size 16  --gradient_accumulation_steps 1  \
    --max_seq_length 512  --save_steps 2000  --max_pair_length 256  --max_mention_ori_length 8    \
    --do_eval  --evaluate_during_training   --eval_all_checkpoints  \
    --fp16  --seed 42  --onedropout  --lminit  \
    --train_file train.json --dev_file dev.json --test_file faa_eval_faa.json  \
    --output_dir sciner_models/sciner-scibert-faa  --overwrite_output_dir  --output_results

RE:

CUDA_VISIBLE_DEVICES=0  python3  run_re.py  --model_type bertsub  \
    --model_name_or_path  ../bert_models/scibert-uncased  --do_lower_case  \
    --data_dir scierc  \
    --learning_rate 2e-5  --num_train_epochs 10  --per_gpu_train_batch_size  8  --per_gpu_eval_batch_size 16  --gradient_accumulation_steps 1  \
    --max_seq_length 256  --max_pair_length 16  --save_steps 2500  \
    --do_eval  --evaluate_during_training   --eval_all_checkpoints  --eval_logsoftmax  \
    --fp16   \
    --test_file sciner_models/sciner-scibert-faa/ent_pred_test.json  \
    --use_ner_results \
    --output_dir scire_models/scire-scibert-faa

10. Run code in pred_results_parse.ipynb to put final triple predictions into a csv in data/results

----------

#### Reproducibility Rating:

<img src="../../star_clip.jpg" alt="Star" width="50" height="50"><img src="../../star_clip.jpg" alt="Star" width="50" height="50"><img src="../../star_clip.jpg" alt="Star" width="50" height="50">

*PL-Marker is deterministic*

Pros:
- The requirements.txt file is accurate
- The commands provided in the Quick Start were helpful for running the SciERC trained model.
- We confirmed their results on the SciERC dataset using their pretrained model.

Cons:
- The documentation on github does not make it clear how to "quick start" other models besides the SciERC-trained model. This led to us having to use the hyperparameters for the SciERC model when running ace05-bert.
- The ace05-albert models did not include a vocab.txt file, so we could not load the tokenizer for them.
- It was not clear how to interpret the output in ent_pred_test.json, which caused us to develop our own notebook (pred_results_parse.ipynb) to extract the results in a human-readable way
- There were no suggestions on how to use the model on a custom dataset. Although the instructions above on downloading and copying data may mostly be inferred from the instructions given in the quickstart for SciERC, we had to comb through the code in each script to verify that we were applying them in a valid way. For example, be mindful that if the data_dir does not have 'ace' or 'scierc' in it, the script will fail.
