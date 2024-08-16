### ASP Setup

[![Paper](https://img.shields.io/badge/Paper-Read%20Now-brightgreen?logo=academia)](https://arxiv.org/pdf/2210.14698.pdf) \
[![GitHub](https://img.shields.io/badge/GitHub-Repository-black?logo=github)](https://github.com/lyutyuh/ASP)

1. git submodule add git@github.com:lyutyuh/ASP.git

2. Create a new conda environment with python=3.8, activate it. Install pytorch=1.12 as appropriate for your system, then install transformers=4.23.1. Then run conda env update --file environment.yml. 

4. Run setup.sh to grab faa.conll from data/FAA_data and copy it three times in the ASP.data folder, saved as <dev, train, test>.english.v4_gold_conll. We do not need train/test/dev splits because we are only using one set to evaluate, but minimize.py expects the folder to be laid out in this way

5. Replace ASP/configs/coref.conf with the coref.conf in this folder, or make the edits on line 3-8 accordingly.

6. Change "ontonotes_coref" to "faa_conll" on line 38 and 80 in util/tensorize_coref.py

7. Add the line "util.runner.logger.info(doc_key)" below line 82 in run_coref.py

8. (Done) jsonlines minimized versions of the data are available in minimized_data to copy into ASP/data/faa_conll if you want to skip this step. Otherwise, from the ASP folder, run python ./data/t5minimize_coref.py ./data/faa_conll/ ./data/faa_conll/. Note that it has created jsonlines documents in the faa_conll folder.

9. To run the base model: python evaluate_coref.py flant5_base tliu/asp-coref-flan-t5-base <GPU_ID> > eval_base.out 2>&1

10. To run the large model: python evaluate_coref.py flant5_t5_large tliu/asp-coref-flan-t5-large <GPU_ID> > eval_large.out 2>&1

11. To run the xl model: python evaluate_coref.py flant5_xl tliu/asp-coref-flan-t5-xl <GPU_ID> > eval_xl.out 2>&1

12. To run the t0_3b model, first, replace runner.py in ASP/util to the runner.py script in this folder. This changes the path to the model in loading - the [config at tliu/asp-coref-t0-3b](https://huggingface.co/tliu/asp-coref-t0-3b/blob/main/config.json) has paths in the creator's local system. It is not clear that replacing those paths with "tliu/asp-coref-t0-3b", as we did, was the correct approach, but it does work. Then run: python evaluate_coref.py t0_3b tliu/asp-coref-t0-3b <GPU_ID> > eval_t0.out 2>&1

13. Use the parse_output.ipynb notebook to extract data from eval.out and save it to a csv in results

-----

#### Reproducibility Rating:

<img src="../../figs/star_clip.jpg" alt="Star" width="50" height="50"><img src="../../figs/star_clip.jpg" alt="Star" width="50" height="50"><img src="../../figs/star_clip.jpg" alt="Star" width="50" height="50"><img src="../../figs/star_clip.jpg" alt="Star" width="50" height="50">

*ASP is deterministic*

ASP has clear documentation, and even has a section on how to use it on new/custom datasets. Its scripts are also intuitive to use, with a small number of regularly-formatted arguments necessary for each task. However, it was not clear that we did have to change "ontonotes_coref" to our own name throughout the scripts. Secondly, ASP outputs its predictions in logging statements but does not save that information anywhere. This caused us to add an extra logging statement for document number to the script, and create a notebook to parse the logs for the appropriate predictions.

A larger issue was the preparation of our data into CoNLL-12 format. There is no standard open source method to process custom datasets into CoNLL-12 format, so the user must create their own script. Depending on which tagger and parser is used in the script, the CoNLL-12 formatted data will turn out differently. This introduces variability in results across implementations of s2e-coref.
