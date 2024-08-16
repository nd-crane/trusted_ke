### spaCy EntityRecognizer Setup

[![Documentation](https://img.shields.io/badge/Documentation-View%20Here-blue?logo=readthedocs)](https://spacy.io/api/entityrecognizer) \
[![Pipeline Documentation](https://img.shields.io/badge/Pipeline%20Documentation-View%20Here-blue?logo=readthedocs)](https://spacy.io/usage/processing-pipelines)

1. Install spacy in a virtual environment

2. Run spacy_ner.py

-------------

#### Reproducibility Rating:

<img src="../../figs/star_clip.jpg" alt="Star" width="50" height="50"><img src="../../figs/star_clip.jpg" alt="Star" width="50" height="50"><img src="../../figs/star_clip.jpg" alt="Star" width="50" height="50"><img src="../../figs/star_clip.jpg" alt="Star" width="50" height="50"><img src="../../figs/star_clip.jpg" alt="Star" width="50" height="50">

*spaCy EntityRecognizer is deterministic*

spaCy has robust documentation, which makes it easy to set up and debug. EntityRecognizer is a default component of spaCy's nlp() pipeline. The pipeline tokenizes, tags, and parses text before performing NER. To access the entities found, simply call nlp(text).ents, where nlp is an instance of spacy.load("en_core_web_sm")
