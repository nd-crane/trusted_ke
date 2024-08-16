### Setup Process

[![Paper](https://img.shields.io/badge/Paper-Read%20Now-brightgreen?logo=academia)](https://arxiv.org/pdf/2109.06067.pdf) \
[![GitHub](https://img.shields.io/badge/GitHub-PLMarker-black?logo=github)](https://github.com/thunlp/PL-Marker/tree/master?tab=readme-ov-file)

1. Create a python virtual environment inside pl-marker and activate

2. Clone the PL-Marker git repo

3. See setup instructions in github README:
    1. Perform these commands as listed, while venv is activated:
        pip3 install -r requirement.txt
        pip3 install --editable ./transformers

    2. No need to set up apex since we are not retraining the models. Also note that apex requires GPUs on your machine and cuda to be installed

    3. Download the SciERC dataset from https://cloud.tsinghua.edu.cn/d/7dafc9a3d84d4151a755/ (optional -- only necessary if you want to run the model on that dataset to confirm their results). The ACE-2005 dataset is available for download with purchase.

    4. Download trained models sciner-scibert and scire-scibert, as well as ace05ner-bert and ace05re-bert, and ace05ner-albert and ace05re-albert from https://cloud.tsinghua.edu.cn/d/5e4a117bc0e5407b9cee/

    5. Create a directory in PL-Marker called sciner_models, and copy or move sciner-scibert there. Create a directory in PL-Marker called scire_models, and copy or move scire-scibert there. Do the same with the ace05 models.

    6. If you downloaded the scierc dataset, you can paste the commands in the Quick Start section of the PL-Marker github to evaluate the model on that dataset and confirm their results.

4. Create JSONL formatted data for the input. See create_jsonl_data.ipynb. That notebook transforms the FAA data to JSONL format and saves it in PL-Marker/scierc. Alternatively, use the .json file already created, now in pl-marker, and copy to pl-marker/PL-Marker/scierc and pl-marker/PL-Marker/ace05 (mkdir these folders). Note that the data directories have to at least contain the strings scierc and ace, respectively, since the ner and re scripts use the data directory name to determine which set of relations to use.

5. Copy sciner_models/sciner-scibert to sciner_models/sciner-scibert_faa. Do the same to all other models (i.e. make a duplicate folder with the _faa suffix)

Your directory tree from pl-marker should look like this:\
*Just the scierc models and data directory is listed for brevity, but assume that the same goes for ace05. The dev, train, and test files are present in scierc if you have downloaded the scierc data, but are not necessary otherwise*
.\
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

9. Create a directory called bert_models in pl-marker (adjacent to PL-Marker). Run the following commands to download the base models, also found in the PL-Marker github documentation:

mkdir -p bert_models/bert-base-uncased \
wget -P bert_models/bert-base-uncased https://huggingface.co/bert-base-uncased/resolve/main/pytorch_model.bin \
wget -P bert_models/bert-base-uncased https://huggingface.co/bert-base-uncased/resolve/main/vocab.txt \
wget -P bert_models/bert-base-uncased https://huggingface.co/bert-base-uncased/resolve/main/config.json

mkdir -p bert_models/albert-xxlarge-v1 \
wget -P bert_models/albert-xxlarge-v1 https://huggingface.co/albert-xxlarge-v1/resolve/main/pytorch_model.bin \
wget -P bert_models/albert-xxlarge-v1 https://huggingface.co/albert-xxlarge-v1/resolve/main/spiece.model \
wget -P bert_models/albert-xxlarge-v1 https://huggingface.co/albert-xxlarge-v1/resolve/main/config.json \
wget -P bert_models/albert-xxlarge-v1 https://huggingface.co/albert-xxlarge-v1/resolve/main/tokenizer.json

mkdir -p bert_models/scibert-uncased \
wget -P bert_models/scibert-uncased https://huggingface.co/allenai/scibert_scivocab_uncased/resolve/main/pytorch_model.bin \
wget -P bert_models/scibert-uncased https://huggingface.co/allenai/scibert_scivocab_uncased/resolve/main/vocab.txt \
wget -P bert_models/scibert-uncased https://huggingface.co/allenai/scibert_scivocab_uncased/resolve/main/config.json

10. Run these commands for each task. Note that NER has to complete before you can do RE. Note that the NER task can take about an hour and a half, while RE takes about 20 minutes.

Note: We changed the model_name_or_path variable to use sciner-scibert etc. instead of the "../bert_models/scibert-uncased" listed in the documentation. We downloaded scibert-uncased as well as bert-base-uncased and used them in the model_name_or_path argument, and determined that they gave the same outputs as sciner-scibert and ace05ner-bert, respectively. The same goes for using them in the relation extraction stage as well.

**SCIERC**

NER:

CUDA_VISIBLE_DEVICES=0  python3  run_acener.py  --model_type bertspanmarker  \
    --model_name_or_path  ../bert_models/scibert-uncased  --do_lower_case  \
    --data_dir scierc  \
    --learning_rate 2e-5  --num_train_epochs 50  --per_gpu_train_batch_size  8  --per_gpu_eval_batch_size 16  --gradient_accumulation_steps 1  \
    --max_seq_length 512  --save_steps 2000  --max_pair_length 256  --max_mention_ori_length 8    \
    --do_eval  --evaluate_during_training   --eval_all_checkpoints  \
    --fp16  --seed 42  --onedropout  --lminit  \
    --test_file faa_plmarker.jsonl  \
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

**ACE 2005**

NER:

CUDA_VISIBLE_DEVICES=0  python3  run_acener.py  --model_type bertspanmarker  \
    --model_name_or_path  ../bert_models/bert-base-uncased  --do_lower_case  \
    --data_dir ace05  \
    --learning_rate 2e-5  --num_train_epochs 50  --per_gpu_train_batch_size  8  --per_gpu_eval_batch_size 16  --gradient_accumulation_steps 1  \
    --max_seq_length 512  --save_steps 2000  --max_pair_length 256  --max_mention_ori_length 8    \
    --do_eval  --evaluate_during_training   --eval_all_checkpoints  \
    --fp16  --seed 42  --onedropout  --lminit  \
    --test_file faa_plmarker.jsonl  \
    --output_dir ace05ner_models/ace05ner-bert-faa  --overwrite_output_dir  --output_results

CUDA_VISIBLE_DEVICES=0  python3  run_acener.py  --model_type albertspanmarker  \
    --model_name_or_path  ../bert_models/albert-xxlarge-v1  --do_lower_case  \
    --data_dir ace05  \
    --learning_rate 2e-5  --num_train_epochs 50  --per_gpu_train_batch_size  8  --per_gpu_eval_batch_size 16  --gradient_accumulation_steps 1  \
    --max_seq_length 512  --save_steps 2000  --max_pair_length 256  --max_mention_ori_length 8    \
    --do_eval  --evaluate_during_training   --eval_all_checkpoints  \
    --fp16  --seed 42  --onedropout  --lminit  \
    --test_file faa_plmarker.jsonl  \
    --output_dir ace05ner_models/ace05ner-albert-faa  --overwrite_output_dir  --output_results

RE:

CUDA_VISIBLE_DEVICES=0  python3  run_re.py  --model_type bertsub  \
    --model_name_or_path  ../bert_models/bert-base-uncased  --do_lower_case  \
    --data_dir ace05  \
    --learning_rate 2e-5  --num_train_epochs 10  --per_gpu_train_batch_size  8  --per_gpu_eval_batch_size 16  --gradient_accumulation_steps 1  \
    --max_seq_length 256  --max_pair_length 16  --save_steps 2500  \
    --do_eval  --evaluate_during_training   --eval_all_checkpoints  --eval_logsoftmax  \
    --fp16   \
    --test_file ace05ner_models/ace05ner-bert-faa/ent_pred_test.json  \
    --use_ner_results \
    --output_dir ace05re_models/ace05re-bert-faa

CUDA_VISIBLE_DEVICES=0  python3  run_re.py  --model_type albertsub  \
    --model_name_or_path  ../bert_models/albert-xxlarge-v1  --do_lower_case  \
    --data_dir ace05  \
    --learning_rate 2e-5  --num_train_epochs 10  --per_gpu_train_batch_size  8  --per_gpu_eval_batch_size 16  --gradient_accumulation_steps 1  \
    --max_seq_length 256  --max_pair_length 16  --save_steps 2500  \
    --do_eval  --evaluate_during_training   --eval_all_checkpoints  --eval_logsoftmax  \
    --fp16   \
    --test_file ace05ner_models/ace05ner-albert-faa/ent_pred_test.json  \
    --use_ner_results \
    --output_dir ace05re_models/ace05re-albert-faa

10. Run code in pred_results_parse.ipynb to put final triple predictions into a csv in data/results


--------------

#### Reproducibility Rating:

<img src="../../figs/star_clip.jpg" alt="Star" width="50" height="50"><img src="../../figs/star_clip.jpg" alt="Star" width="50" height="50"><img src="../../figs/star_clip.jpg" alt="Star" width="50" height="50">

*PL-Marker is deterministic given a certain seed in the NER stage*

Pros:
- The requirements.txt file is accurate
- The commands provided in the Quick Start were helpful for running the SciERC trained model.
- We confirmed their results on the SciERC dataset using their pretrained model.

Cons:
- The documentation on github does not make it clear how to "quick start" other models besides the SciERC-trained model. This led to us having to use the hyperparameters for the SciERC model when running ace05-bert.
- The documentation pointed to pretrained LLMs from Huggingface which could be finetuned using their scripts, and it also linked the PL-Marker finetuned models, presumably the result of those training scripts. However, we used evaluated with both the base pretrained models and the PL-Marker finetuned models, and found that they delivered the same output. We are open to suggestions on why this is.
- The ace05-albert models did not include a vocab.txt file, so we could not load the tokenizer for them.
- It was not clear how to interpret the output in ent_pred_test.json, which caused us to develop our own notebook (pred_results_parse.ipynb) to extract the results in a human-readable way
- There were no suggestions on how to use the model on a custom dataset. Although the instructions above on downloading and copying data may mostly be inferred from the instructions given in the quickstart for SciERC, we had to comb through the code in each script to verify that we were applying them in a valid way. For example, be mindful that if the data_dir does not have 'ace' or 'scierc' in it, the script will fail.
