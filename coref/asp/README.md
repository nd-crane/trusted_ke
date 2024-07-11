### ASP Setup

Github: https://github.com/lyutyuh/ASP

Paper: https://arxiv.org/pdf/2210.14698.pdf

1. git submodule add git@github.com:lyutyuh/ASP.git

2. Create a new conda environment with python=3.8, activate it. Install pytorch=1.12 as appropriate for your system, then install transformers=4.23.1. Then run conda env update --file environment.yml. 

4. Run setup.sh to grab faa.conll from data/FAA_data and copy it three times in the ASP.data folder, saved as <dev, train, test>.english.v4_gold_conll. We do not need train/test/dev splits because we are only using one set to evaluate, but minimize.py expects the folder to be laid out in this way

5. Replace ASP/configs/coref.conf with the coref.conf in this folder, or make the edits on line 3-8 accordingly.

6. Change "ontonotes_coref" to "faa_conll" on line 38 and 80 in util/tensorize_coref.py

7. Add the line "util.runner.logger.info(doc_key)" below line 82 in run_coref.py

8. (Done) jsonlines minimized versions of the data are available in minimized_data to copy into ASP/data/faa_conll if you want to skip this step. Otherwise, from the ASP folder, run python ./data/t5minimize_coref.py ./data/faa_conll/ ./data/faa_conll/. Note that it has created jsonlines documents in the faa_conll folder.

9. Run evaluate_coref via: python evaluate_coref.py flant5_base tliu/asp-coref-flan-t5-base <GPU_ID> > eval.out 2>&1

10. Use the parse_output.ipynb notebook to extract data from eval.out and save it to a csv in results