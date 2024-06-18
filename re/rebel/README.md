### REBEL Setup

Github: https://github.com/Babelscape/rebel

Paper: https://aclanthology.org/2021.findings-emnlp.204.pdf

Setup:

1. Created a python virtual env venv and activate it

2. Install torch as specified by [Pytorch](https://pytorch.org/get-started/locally/)

4. Got requirements.txt from the github, with wget https://raw.githubusercontent.com/Babelscape/rebel/main/requirements.txt

5. Change the == on the datasets line to <=, or you will encounter an error that datasets and transformers need different versions of huggingface-hub.

6. pip install -r requirements.txt

7. Run python scripts to obtain results. The script code was taken from the [documentation on Huggingface](https://huggingface.co/Babelscape/rebel-large) The pipe script uses Rebel as a component in a spacy pipeline, and takes longer

----------------------------

#### Reproducibility Rating:

<img src="../../star_clip.jpg" alt="Star" width="50" height="50"><img src="../../star_clip.jpg" alt="Star" width="50" height="50"><img src="../../star_clip.jpg" alt="Star" width="50" height="50"><img src="../../star_clip.jpg" alt="Star" width="50" height="50"><img src="../../star_clip.jpg" alt="Star" width="50" height="50">

*The spaCy pipeline implementation of REBEL is deterministic, however, the direct implementation is not*

REBEL's documentation is informative and to-the-point, and the requirements.txt file is accurate. Making it available as a spacy component makes it versatile and easy to use. Using the model directly allows the user to specify number of beams and length penalty as well as the number of sentences to return.

After a number of trials (output available in data/results/rebel), we determined that the spaCy pipeline implementation of REBEL is deterministic, however, the direct implementation is not, regardless of hyperparameter settings. Because of this, we only use the spacy pipeline results when evaluating. To see how REBEL's results vary with hyperparameter settings and repeated runs, see data/results/rebel.

Moreover, we also found that REBEL is extremely sensitive to noise. An added space between a word and a period, or even a space after a period, will change the results that even the spacy pipeline implementation produces. This can lead to completely different triples, even if the entities in the triples themselves are not adjacent to the added space in the sentence. 
