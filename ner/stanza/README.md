### Stanza Setup

Documentation: https://stanfordnlp.github.io/stanza/ner.html

1. Install stanza in a virtual environment

2. Run stanza_ner.py

----------------

#### Reproducibility Rating:

<img src="../../figs/star_clip.jpg" alt="Star" width="50" height="50"><img src="../../figs/star_clip.jpg" alt="Star" width="50" height="50"><img src="../../figs/star_clip.jpg" alt="Star" width="50" height="50"><img src="../../figs/star_clip.jpg" alt="Star" width="50" height="50"><img src="../../figs/star_clip.jpg" alt="Star" width="50" height="50">

*Stanza NERProcessor is deterministic*

Stanza has robust documentation with examples for NER. It is easy to implement in just a few lines of code. NERProcessor is available as a pipeline component, and the entities it finds can be accessed via nlp(text).ents, where nlp is an instance of stanza.Pipeline()
