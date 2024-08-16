### NLTK Setup

[![Documentation](https://img.shields.io/badge/Documentation-View%20Here-blue?logo=readthedocs)](https://www.nltk.org/api/nltk.chunk.ne_chunk.html) \
[![Documentation for Chunk Package](https://img.shields.io/badge/Documentation%20for%20chunk%20package-View%20Here-blue?logo=readthedocs)](https://www.nltk.org/api/nltk.chunk.ne_chunk.html) \
[![GitHub](https://img.shields.io/badge/GitHub-Repository-black?logo=github)](https://github.com/nltk/nltk/tree/develop/nltk/chunk)

1. Install nltk in a virtual environment

2. Run nltk_ner.py

*IMPORTANT NOTE:* The results change dramatically when the input is left uppercased vs when it is lowercased. The lowercased returns no results, whereas the uppercased returns many entities with the ORG label. We infer that this is due to the prevalence of organizations referred to by capital letter acronyms.

------

#### Reproducibility Rating:

<img src="../../figs/star_clip.jpg" alt="Star" width="50" height="50"><img src="../../figs/star_clip.jpg" alt="Star" width="50" height="50"><img src="../../figs/star_clip.jpg" alt="Star" width="50" height="50"><img src="../../figs/star_clip.jpg" alt="Star" width="50" height="50">

*ne_chunk is deterministic*

The NLTK documentation for ne_chunk does not include any code samples or demos. However, it is easy to implement simply by installing nltk and calling the ne_chunk method, which returns a nltk tree object like so:\
        (S\
          F./NNP\
          (PERSON Henly/NNP)\
          was/VBD\
          born/VBN\
          in/IN\
          (GPE San/NNP Francisco/NNP)\
          and/CC\
          he/PRP\
          works/VBZ\
          at/IN\
          (ORGANIZATION Microsoft/NNP)\
          ./.)\
Extracting the entities from the tree took some extra experimentation, after which we identified a reliable method using the subtrees and leaves methods of the tree object.
