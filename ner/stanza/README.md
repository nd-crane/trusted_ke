### Stanza Setup

[![Documentation](https://img.shields.io/badge/Documentation-View%20Here-blue?logo=readthedocs)](https://stanfordnlp.github.io/stanza/ner.html) \
[![GitHub](https://img.shields.io/badge/GitHub-Repository-black?logo=github)](https://github.com/stanfordnlp/stanza/tree/main)

1. Install stanza in a virtual environment

2. Run stanza_ner.py

----------------

#### Reproducibility Rating:

<img src="../../figs/star_clip.jpg" alt="Star" width="50" height="50"><img src="../../figs/star_clip.jpg" alt="Star" width="50" height="50"><img src="../../figs/star_clip.jpg" alt="Star" width="50" height="50"><img src="../../figs/star_clip.jpg" alt="Star" width="50" height="50"><img src="../../figs/star_clip.jpg" alt="Star" width="50" height="50">

*Stanza NERProcessor is deterministic*

Stanza has robust documentation with examples for NER. It is easy to implement in just a few lines of code. NERProcessor is available as a pipeline component, and the entities it finds can be accessed via nlp(text).ents, where nlp is an instance of stanza.Pipeline()
