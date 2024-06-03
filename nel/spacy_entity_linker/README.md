### spaCy Entity Linker Setup
SpaCy Python Package: https://pypi.org/project/spacy-entity-linker/

1. Create Conda environment: `conda create --name spacy_entity_linker`
2. Activate Conda Environment `conda activate spacy_entity_linker`
3. `pip install spacy`
4. `python -m spacy download en_core_web_lg`
5. `pip install spacy_entity_linker`
6. `python -m spacy_entity_linker "download_knowledge_base"`
7. `pip install pandas`
8. Run on either the MaintNet or FAA Data: `python nel/spacy_entity_linker/sel_maintnet.py` or `python nel/spacy_entity_linker/sel_faa.py`

Results are in the data/results/spacy_entity_linker folder
----------------------------

#### Reproducibility Rating:

<img src="../../star_clip.jpg" alt="Star" width="50" height="50"><img src="../../star_clip.jpg" alt="Star" width="50" height="50"><img src="../../star_clip.jpg" alt="Star" width="50" height="50"><img src="../../star_clip.jpg" alt="Star" width="50" height="50"><img src="../../star_clip.jpg" alt="Star" width="50" height="50">

spaCy is deterministic.
It is also easy to setup since SpaCy Entity Linker interfaces with pip 
