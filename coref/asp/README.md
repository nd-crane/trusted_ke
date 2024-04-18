### ASP Setup

Github: https://github.com/lyutyuh/ASP

Paper: https://arxiv.org/pdf/2210.14698.pdf

1. git submodule add git@github.com:lyutyuh/ASP.git

2. Clone nvidia-apex: git clone https://github.com/NVIDIA/apex # do we still do this?

3. Create a new conda environment, activate it. Install pytorch as appropriate for your system. Then run conda env update --file environment.yml

4. Run setup.sh to grab faa.conll from data/FAA_data and copy it three times in the ASP.data folder, saved as <dev, train, test>.english.v4_gold_conll. We do not need train/test/dev splits because we are only using one set to evaluate, but minimize.py expects the folder to be laid out in this way

5. Replace ASP/configs/coref.conf with the coref.conf in this folder, or make the edits on line 3-8 accordingly.

6. Change "ontonotes_coref" to "faa_conll" on line 38 and 80 in util/tensorize_coref.py

7. (Done) jsonlines minimized versions of the data are available in minimized_data to copy into ASP/data/faa_conll if you want to skip this step. Otherwise, from the ASP folder, run python ./data/t5minimize_coref.py ./data/faa_conll/ ./data/faa_conll/. Note that it has created jsonlines documents in the faa_conll folder.

8. Run evaluate_coref via: python evaluate_coref.py flant5_base tliu/asp-coref-flan-t5-base <GPU_ID> > eval.out 2>&1

9. 



Current steps taken with asp environment:\
6. Create a conda virtual environment from the environment.yml file
7. Install pandas
9. conda install -c nvidia cuda-nvcc
10. from apex: pip install -v --disable-pip-version-check --no-cache-dir --no-build-isolation --global-option="--cpp_ext" --global-option="--cuda_ext" ./
11. conda install pytorch torchvision torchaudio pytorch-cuda=12.1 -c pytorch -c nvidia
12. mamba install conda-forge::nvidia-apex
13. mamba install torch