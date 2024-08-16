### REBEL Setup

[![Paper](https://img.shields.io/badge/Paper-Read%20Now-brightgreen?logo=academia)](https://aclanthology.org/2021.findings-emnlp.204.pdf) \
[![GitHub](https://img.shields.io/badge/GitHub-Repository-black?logo=github)](https://github.com/Babelscape/rebel)

Setup:

1. Created a python virtual env venv and activate it

2. Install torch as specified by [Pytorch](https://pytorch.org/get-started/locally/)

4. Got requirements.txt from the github, with wget https://raw.githubusercontent.com/Babelscape/rebel/main/requirements.txt

5. Change the == on the datasets line to <=, or you will encounter an error that datasets and transformers need different versions of huggingface-hub.

6. pip install -r requirements.txt

7. Run python scripts to obtain results. The script code was taken from the [documentation on Huggingface](https://huggingface.co/Babelscape/rebel-large) The pipe script uses Rebel as a component in a Huggingface pipeline, and takes longer

Example:

python rebel_pipe.py --dataset_path ../../OMIn_dataset/data/FAA_data/Maintenance_Text_Data_nona.csv --text_col c119 -id_col c5 -output_path ../../tool_results/rebel/rebel_pipe.csv

python rebel_main.py --dataset_path ../../OMIn_dataset/data/FAA_data/Maintenance_Text_Data_nona.csv --text_col c119 -id_col c5 -output_path ../../tool_results/rebel/rebel_main.csv

You may also specify hyperparameters in the rebel_main.py script:\
python rebel_main.py --dataset_path ../../OMIn_dataset/data/FAA_data/Maintenance_Text_Data_nona.csv --text_col c119 -id_col c5 -output_path ../../tool_results/rebel/rebel_main.csv --max_length 128 --length_penalty -1 --num_beams 5 --num_return_sentences 3

The defaults for these hyperparameters is as follows:
* max_length 256
* length_penalty 0
* num_beams 1
* num_return_sentences 1


----------------------------

#### Reproducibility Rating:

<img src="../../figs/star_clip.jpg" alt="Star" width="50" height="50"><img src="../../figs/star_clip.jpg" alt="Star" width="50" height="50"><img src="../../figs/star_clip.jpg" alt="Star" width="50" height="50"><img src="../../figs/star_clip.jpg" alt="Star" width="50" height="50"><img src="../../figs/star_clip.jpg" alt="Star" width="50" height="50">

*The Huggingface pipeline implementation of REBEL is deterministic, however, the direct implementation is not*

REBEL's documentation is informative and to-the-point, and the requirements.txt file is accurate. Making it available as a Huggingface pipeline component makes it versatile and easy to use. Using the model directly allows the user to specify number of beams and length penalty as well as the number of sentences to return.

After a number of trials (output available in tool_results/rebel), we determined that the Huggingface pipeline implementation of REBEL is deterministic, however, the direct implementation is not, regardless of hyperparameter settings. Because of this, we only use the spacy pipeline results when evaluating. To see how REBEL's results vary with hyperparameter settings and repeated runs, see tool_results/rebel.

Moreover, we also found that REBEL is extremely sensitive to noise. An added space between a word and a period, or even a space after a period, will change the results that even the spacy pipeline implementation produces. This can lead to completely different triples, even if the entities in the triples themselves are not adjacent to the added space in the sentence. 
