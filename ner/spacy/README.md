### spaCy EntityRecognizer Setup

Documentation: https://spacy.io/api/entityrecognizer \
Pipeline documentation: https://spacy.io/usage/processing-pipelines

1. Install spacy in a virtual environment

2. Run spacy_ner.py

-------------

#### Reproducibility Rating:

<img src="../../star_clip.jpg" alt="Star" width="50" height="50"><img src="../../star_clip.jpg" alt="Star" width="50" height="50"><img src="../../star_clip.jpg" alt="Star" width="50" height="50"><img src="../../star_clip.jpg" alt="Star" width="50" height="50"><img src="../../star_clip.jpg" alt="Star" width="50" height="50">

spaCy has robust documentation, which makes it easy to set up and debug. EntityRecognizer is a default component of spaCy's nlp() pipeline. The pipeline tokenizes, tags, and parses text before performing NER. To access the entities found, simply call nlp(text).ents, where nlp is an instance of spacy.load("en_core_web_sm")
