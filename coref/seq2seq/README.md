### seq2seq Setup

Github: https://github.com/google-research/google-research/tree/master/coref_mt5

Paper: https://arxiv.org/pdf/2211.12142v1.pdf

1. Download coreference_decoder.ipynb from the github: wget https://raw.githubusercontent.com/google-research/google-research/master/coref_mt5/colabs/coreference_decoder.ipynb

2. Note that the requirements.txt on the github just contains a numpy version. numpy>=1.21.5. You actually need more than this, so just use the environment.yml included here. Create a fresh conda environment called seq2seq and activate it. Run conda env update --file environment.yml

3. (With conda environment activated!) Run python -m ipykernel install --user --name seq2seq

4. Open coreference_decoder.ipynb as a jupyter notebook, and select seq2seq as your kernel

5. Step through the notebook.

6. 


JK

1. Note that the Github contains a requirements.txt and a notebook in colabs/ called coreference_decoder.ipynb. The requirements.txt solely contains the specification numpy>=1.21.5, and more requirements are actually needed, so please follow the instructions here instead. In addition, no need to download the coreference_decoder.ipynb notebook, since we have copied the code to coreference_decoder.py seen here.

2. While in the seq2seq directory, do: git clone https://github.com/huggingface/transformers.git

3. Create a python virtual environment venv and activate it. Do: pip install numpy tensorflow\[and-cuda\] nltk sentencepiece ./transformers

4. Run coreference_decoder.py


Can't download because the checkpoint is not suitable for porting to other architectures. https://cloud.google.com/blog/products/ai-machine-learning/train-fast-on-tpu-serve-flexibly-on-gpu-switch-your-ml-infrastructure-to-suit-your-needs

