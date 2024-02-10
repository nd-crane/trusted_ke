# Survey of Knowledge Extraction Tools for Maintenance Data

University of Notre Dame | Center for Research Computing | Trusted AI\
Kate Mealey, Jonathan Karr, Danny Finch, Alyssa Riter, Priscila Moriera, Eli Phillips, Paul Brenner, Charles Vardeman

---
Released code from our paper: ____
Please open an issue if there are any questions.

---
KE tools at a glance:

| Coreference Resolution | Named Entity Linking (NEL) | Relation Extraction (RE) |
|----------|----------|----------|
| ASP | BLINK | REBEL |
| coref_mt5 | spaCy EntityLinker | UniRel |
| s2e-coref | GENRE | DeepStruct |
| neuralcoref | ReFinED | PL-Marker |

---

## Coreference Resolution

### ASP: Autoregressive Structured Prediction with Language Models

Github: https://github.com/lyutyuh/ASP\
Paper: https://arxiv.org/pdf/2210.14698.pdf\

Research Institution: Google Research

[short desc of tool]

Base Model: T5

### coref_mt5: Coreference Resolution through a seq2seq Transition-Based System

Github: https://github.com/google-research/google-research/tree/master/coref_mt5\
Paper: https://arxiv.org/pdf/2211.12142v1.pdf\

Research Institution: Google Research

[short desc of tool]

Base Model: mT5

### s2e-coref: Start-To-End Coreference Resolution

Github: https://github.com/yuvalkirstain/s2e-coref\
Paper: https://aclanthology.org/2021.acl-short.3.pdf\

Research Institution: University of Tel Aviv

[short desc of tool]

Base Model: longformer-large

### neuralcoref

Github: https://github.com/huggingface/neuralcoref
Blog Post: https://medium.com/huggingface/state-of-the-art-neural-coreference-resolution-for-chatbots-3302365dcf30

Created by spaCy

[short desc of tool]

Not LLM-based

---

## Named Entity Linking

### BLINK: Scalable Zero-shot Entity Linking with Dense Entity Retrieval

Github: https://github.com/facebookresearch/BLINK\
Paper: https://arxiv.org/pdf/1911.03814.pdf\

Research Institution: Facebook AI Research

[short desc of tool]

Uses Flair for NER: https://github.com/flairNLP/flair\
Base Model: BERT

### spaCy EntityLinker

Documentation: https://spacy.io/api/entitylinker

Created by spaCy

[short desc of tool]

Not LLM-based

### GENRE: Generative ENtity REtrieval

Github: https://github.com/facebookresearch/GENRE\
Paper: https://arxiv.org/pdf/2010.00904.pdf\

Research Institution: Facebook AI Research

[short desc of tool]

Base Model: BART **** Jonathan please check ****

### ReFinED: Representation and Fine-grained typing for Entity Disambiguation

Github: https://github.com/amazon-science/ReFinED\
Papers: https://arxiv.org/pdf/2207.04108.pdf, https://arxiv.org/pdf/2207.04106.pdf\

Research Institution: Amazon Alexa AI

[short desc of tool]

Base Model: *** Jonathan please find it? Maybe they trained the wiki model and the aida model from scratch though ***

---

## Relation Extraction

### REBEL: Relation Extraction By End-to-end Language generation

Github: https://github.com/Babelscape/rebel\
Paper: https://aclanthology.org/2021.findings-emnlp.204.pdf\

Research Institution: Sapienza University of Rome, Babelscape

[short desc of model]

Base Model: BART-large

Relation set: Subset of 220 relations from Wikidata properties, found here: https://github.com/Babelscape/rebel/blob/main/data/relations_count.tsv

### UniRel: Unified Representation and Interaction for Joint Relational Triple Extraction

Github: https://github.com/wtangdev/UniRel/tree/main\
Paper: https://arxiv.org/pdf/2211.09039.pdf\

Research Institution: University of Science and Technology of China

[short desc of model]

Base Model: bert-base-cased

Relation set: 25 relations from the NYT dataset, found here: https://github.com/wtangdev/UniRel/blob/main/dataprocess/rel2text.py#L30

### DeepStruct

Github: https://github.com/wang-research-lab/deepstruct\
Paper: https://arxiv.org/pdf/2205.10475.pdf\

Research Institutions: UC Berkeley, Tsinghua University

[short desc of model]

Base Model: GLM

Relation set: *** Jonathan please find this -- DeepStruct is trained on CoNLL04, ADE, NYT, and ACE2005, which each have a different relation set ***

### PL-Marker: Packed Levitated Marker for Entity and Relation Extraction

Github: https://github.com/thunlp/PL-Marker/tree/master?tab=readme-ov-file\
Paper: https://arxiv.org/pdf/2109.06067.pdf\

Research Institution: Tsinghua University

[short desc of model]

PL-Marker uses different models for each dataset among ACE 2004, ACE2005, and SciERC:

| Dataset | Base Model | Relation Set |
|----------|----------|----------|
| ACE04 | albert-xxlarge-v1 or bert-base-uncased | ['PER-SOC', 'OTHER-AFF', 'ART', 'GPE-AFF', 'EMP-ORG', 'PHYS'] |
| ACE05 | albert-xxlarge-v1 or bert-base-uncased | ['PER-SOC', 'ART', 'ORG-AFF', 'GEN-AFF', 'PHYS', 'PART-WHOLE'] |
| SciERC | scibert_scivocab_uncased | ['PART-OF', 'USED-FOR', 'FEATURE-OF', 'CONJUNCTION', 'EVALUATE-FOR', 'HYPONYM-OF', 'COMPARE'] |
