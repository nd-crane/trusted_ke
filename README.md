# Survey of Knowledge Extraction Tools for Maintenance Data

University of Notre Dame | Center for Research Computing | Trusted AI\
Kate Mealey, Jonathan Karr, Danny Finch, Alyssa Riter, Priscila Moreira, Eli Phillips, Paul Brenner, Charles Vardeman

---
Released code from our paper: ____\
Please open an issue if there are any questions.

---


The following is a survey of knowledge extraction tools for maintenance data. The survey includes tools for Named Entity Recognition (NER), Coreference Resolution (CR), Named Entity Linking (NEL), and Relation Extraction (RE). The survey provides an overview of each tool's methodology, base model, and relation set, where applicable. 

The survey also includes a comparison of the tools' outputs with the [Gold Standard Data](gold_standard/README.md), which is a subset of the Complete Set of FAA data created to evaluate the correctness of the tools regarding NER, NEL, and RE tasks. There are two types os correctness evaluations: **automatic** and **manual**. For more details on the correctness evaluations, please refer to the [Correctness Evaluation](evaluations/README.md).

KE tools at a glance:

| Named Entity Recognition (NER)| Coreference Resolution (CR)   | Named Entity Linking (NEL)       | Relation Extraction (RE)   |
|-------------------------------|-------------------------------|---------------------------------|---------------------------|
| [x] spaCy EntityRecognizer    | [x] ASP                       | [x] BLINK                       | [x] REBEL                 |
| [x] flair NER                 | [x] coref_mt5                 | [x] spaCy EntityLinker          | [x] UniRel                |
| [x] stanza NERProcessor       | [x] s2e-coref                 | [x] GENRE                       | [ ] DeepStruct            |
| [x] nltk ne_chunk             | [x] neuralcoref               | [x] ReFinED                     | [x] PL-Marker (SciERC)    |

---

README's polished:

| Named Entity Recognition (NER)| Coreference Resolution (CR)   | Named Entity Linking (NEL)       | Relation Extraction (RE)   |
|-------------------------------|-------------------------------|---------------------------------|---------------------------|
| [x] spaCy EntityRecognizer    | [ ] ASP                       | [x] BLINK                       | [x] REBEL                 |
| [x] flair NER                 | [ ] coref_mt5                 | [x] spaCy EntityLinker          | [x] UniRel                |
| [x] stanza NERProcessor       | [x] s2e-coref                 | [x] GENRE                       | [ ] DeepStruct            |
| [x] nltk ne_chunk             | [x] neuralcoref               | [ ] ReFinED                     | [x] PL-Marker (SciERC)    |

-----

## Named Entity Recognition

The set of labels for our NER tools are listed below:
|           | Labels | Tools w/ this Label Set |
|-----------|--------|-------------------------|
| OntoNotes | Cardinal, Date, Event, Facility (FAC), Geo-Political Entity (GPE), Language, Law, Location (LOC), Money, Nationalities, religious, or political groups (NORP), Ordinal, Organization (ORG), Percent, Person, Product, Quantity, Time, Work_Of_Art | spaCy, stanza |
| CoNLL-03  | Person, Organization, Location, Misc Names | flair |
| ACE-2005  | Person, Organization, Location, Facility, Weapon, Vehicle, Geo-Political Entity (GPE) | NLTK |

### spaCy EntityRecognizer

Documentation: https://spacy.io/api/entityrecognizer

Created by spaCy

EntityRecognizer identifies non-overlapping labeled spans of tokens using a transition-based algorithm. spaCy notes that: "the loss function optimizes for whole entity accuracy, so if your inter-annotator agreement on boundary tokens is low, the component will likely perform poorly on your problem. The transition-based algorithm also assumes that the most decisive information about your entities will be close to their initial tokens. If your entities are long and characterized by tokens in their middle, the component will likely not be a good fit for your task." EntityRecognizer recognizes the 18 entity types in OntoNotes.

Not LLM-based.

_Used by:_ Our implementation of CoNLL-2012 format processing

### flair NER

Github: https://github.com/flairNLP/flair \
Documentation: https://flairnlp.github.io/docs/intro

Research Institution: Humboldt University of Berlin

Flair ships several models which can be used for NER (or "tagging"), including their standard model, which recognizes 4 entity types and was trained for the CoNLL-03 task. They use transformer models, which they develop, and publish on Huggingface.

Model: flair/ner-english

_Used by:_ BLINK

### stanza NERProcessor

Documentation: https://stanfordnlp.github.io/stanza/ner.html \
Stanza Github: https://github.com/stanfordnlp/stanza/tree/main

Created by StanfordNLP

Stanza NERProcessor recognizes spans of mentions belonging to the 18 entity types found in the OntoNotes NER task.

Not used by any other tools in the pipeline.

### NLTK ne_chunk

Documentation: https://www.nltk.org/api/nltk.chunk.ne_chunk.html \
Github: https://github.com/nltk/nltk/tree/develop/nltk/chunk

Created by NLTK

NLTK ne_chunk takes in a list of POS-tagged tokens as input and creates a parse tree where named entities and their labels are stored as subtrees. It recognizes the seven entity types in ACE 2005.

Not used by any other tools in the pipeline.

---

## Coreference Resolution

### ASP: Autoregressive Structured Prediction with Language Models

Github: https://github.com/lyutyuh/ASP \
Paper: https://arxiv.org/pdf/2210.14698.pdf

Research Institution: Google Research

The Autoregressive Structured Prediction (ASP) framework utilizes a conditional language model trained over structure-building actions, as opposed to strings, allowing the model to capture intra-structure dependencies more effectively and build pieces of the target structure step by step. It focuses on tasks such as named entity recognition, end-to-end relation extraction, and coreference resolution.

Base Model: T5

### coref_mt5: Coreference Resolution through a seq2seq Transition-Based System

Github: https://github.com/google-research/google-research/tree/master/coref_mt5 \
Paper: https://arxiv.org/pdf/2211.12142v1.pdf

Research Institution: Google Research

coref_mt5's methodology for coreference resolution uses a seq2seq approach, where a single sentence, along with prior context, is encoded as a string and fed into a model to predict coreference links. The system utilizes a transition-based approach, particularly the Link-Append system, which encodes prior coreference decisions in the input to the seq2seq model and predicts new coreference links as its output.

Base Model: mT5

### s2e-coref: Start-To-End Coreference Resolution

Github: https://github.com/yuvalkirstain/s2e-coref \
Paper: https://aclanthology.org/2021.acl-short.3.pdf

Research Institution: Tel Aviv University

The s2e coreference resolution model introduces a lightweight approach that avoids constructing span representations. Instead, it uses the boundaries of spans to computes mention and antecedent scores, through a series of bilinear functions over their contextualized representations.

Base Model: longformer-large

### neuralcoref

Github: https://github.com/huggingface/neuralcoref \
Blog Post: https://medium.com/huggingface/state-of-the-art-neural-coreference-resolution-for-chatbots-3302365dcf30

Created by spaCy

Neuralcoref's methodology for coreference resolution uses the spaCy parser for mention-detection, and ranks possible mention-coreference pairs using a feedforward neural network developed by Clark and Manning, Stanford University (https://cs.stanford.edu/people/kevclark/resources/clark-manning-emnlp2016-deep.pdf).

Base Model: spaCy english model (we used en_core_web_sm) **** Jonathan can you verify??*****

---

## Named Entity Linking

### BLINK: Scalable Zero-shot Entity Linking with Dense Entity Retrieval

Github: https://github.com/facebookresearch/BLINK \
Paper: https://arxiv.org/pdf/1911.03814.pdf

Research Institution: Facebook AI Research

BLINK introduces a two-stage zero-shot entity linking algorithm, utilizing a bi-encoder for dense entity retrieval and a cross-encoder for re-ranking. The bi-encoder independently embeds the mention context and entity descriptions in a dense space, while the cross-encoder concatenates the mention and entity text for more precise ranking. This approach demonstrates state-of-the-art performance on recent zero-shot benchmarks and traditional non-zero-shot evaluations, showcasing its effectiveness without the need for explicit entity embeddings or manually engineered mention tables.

Uses Flair for NER: https://github.com/flairNLP/flair \
Base Model: BERT

### spaCy EntityLinker

Documentation: https://spacy.io/api/entitylinker

Created by spaCy

spaCy EntityLinker is spaCy's NEL pipeline component. It uses the InMemoryLookupKB knowledge base to match mentions with external entities. InMemoryLookupKB contains Candidate components which store basic information about their entities, like frequency in text and possible aliases.

Not LLM-based

### GENRE: Generative ENtity REtrieval

Github: https://github.com/facebookresearch/GENRE \
Paper: https://arxiv.org/pdf/2010.00904.pdf

Research Institution: Facebook AI Research

GENRE utilizes a sequence-to-sequence model to autoregressively generate textual entity identifiers. This approach allows GENRE to directly capture the relations between context and entity names, effectively cross-encoding both, and to efficiently compute the exact softmax for each output token without the need for negative data downsampling. Additionally, GENRE employs a constrained decoding strategy that forces each generated name to be in a predefined candidate set, ensuring that the generated output is a valid entity name.

Base Model: BART

### ReFinED: Representation and Fine-grained typing for Entity Disambiguation

Github: https://github.com/amazon-science/ReFinED \
Papers: https://arxiv.org/pdf/2207.04108.pdf, https://arxiv.org/pdf/2207.04106.pdf

Research Institution: Amazon Alexa AI

ReFinED is an efficient end-to-end entity linking model that utilizes fine-grained entity types and entity descriptions to perform mention detection, fine-grained entity typing, and entity disambiguation in a single forward pass. It targets a large catalog of entities, including zero-shot entities, and is capable of generalizing to large-scale knowledge bases such as Wikidata.

Base Model: RoBERTa

---

## Relation Extraction

### REBEL: Relation Extraction By End-to-end Language generation

Github: https://github.com/Babelscape/rebel \
Paper: https://aclanthology.org/2021.findings-emnlp.204.pdf

Research Institution: Sapienza University of Rome, Babelscape

REBEL's methodology for relation extraction involves utilizing an autoregressive seq2seq model based on BART to express relation triplets as a sequence of text, simplifying the task of extracting triplets of relations between entities from raw text. This approach allows REBEL to perform end-to-end relation extraction for over 200 different relation types, and its flexibility enables it to adapt to new domains and datasets with minimal training time. Additionally, REBEL introduces a novel triplet linearization approach using special tokens, enabling the model to output relations in the form of triplets while minimizing the number of tokens that need to be decoded.

Base Model: BART-large

Relation set: Subset of 220 relations from Wikidata properties, found here: https://github.com/Babelscape/rebel/blob/main/data/relations_count.tsv

### UniRel: Unified Representation and Interaction for Joint Relational Triple Extraction

Github: https://github.com/wtangdev/UniRel/tree/main \
Paper: https://arxiv.org/pdf/2211.09039.pdf

Research Institution: University of Science and Technology of China

UniRel's methodology for relation extraction involves unifying the representations of entities and relations by jointly encoding them within a concatenated natural language sequence. This approach fully exploits the contextualized correlations between entities and relations and leverages the semantic knowledge learned from pre-training. Additionally, UniRel proposes unified interactions to capture the interdependencies between entity-entity interactions and entity-relation interactions, achieved through the proposed Interaction Map built upon the off-the-shelf self-attention mechanism within any Transformer block.

Base Model: bert-base-cased

Relation set: 25 relations from the NYT dataset, found here: https://github.com/wtangdev/UniRel/blob/main/dataprocess/rel2text.py#L30

['/business/company/advisors','/business/company/founders','/business/company/industry','/business/company/major_shareholders','/business/company/place_founded','business/company_shareholder/major_shareholder_of','/business/person/company','/location/administrative_division/country','/location/country/administrative_divisions','location/country/capital','/location/location/contains',   '/location/neighborhood/neighborhood_of','/people/deceased_person/place_of_death','/people/ethnicity/geographic_distribution','/people/ethnicity/people','/people/person/children','/people/person/ethnicity','/people/person/nationality','/people/person/place_lived','/people/person/place_of_birth','/people/person/profession','/people/person/religion','/sports/sports_team/location','/sports/sports_team_location/teams']

### DeepStruct

Github: https://github.com/wang-research-lab/deepstruct \
Paper: https://arxiv.org/pdf/2205.10475.pdf

Research Institutions: UC Berkeley, Tsinghua University

DEEPSTRUCT's methodology for relation extraction involves a sequence-to-sequence extraction approach using augmented natural languages. It formulates the task as two unit tasks: entity prediction to generate entities and relation prediction to generate relations, with a focus on generating triples for a wide set of structure prediction tasks in an end-to-end fashion. This approach decomposes structure prediction tasks into a collection of triple generation tasks, providing a unified representation for various structure prediction tasks without the need for introducing new data augmentation.

Base Model: GLM

[TO-DO: This list of relations may be incorrect, since ACE-O5 is specifically pl-marker's adaptation of ACE0-05 relations]

| Dataset | Relation Set |
|----------|----------|
| CoNLL 04 | ['Work-For', 'Kill', 'Organization-Based-In', 'Live-In', 'Located-In'] |
| ADE | ['Adverse-Effect'] |
| NYT | ['/business/company/advisors','/business/company/founders','/business/company/industry','/business/company/major_shareholders','/business/company/place_founded','business/company_shareholder/major_shareholder_of','/business/person/company','/location/administrative_division/country','/location/country/administrative_divisions','location/country/capital','/location/location/contains',   '/location/neighborhood/neighborhood_of','/people/deceased_person/place_of_death','/people/ethnicity/geographic_distribution','/people/ethnicity/people','/people/person/children','/people/person/ethnicity','/people/person/nationality','/people/person/place_lived','/people/person/place_of_birth','/people/person/profession','/people/person/religion','/sports/sports_team/location','/sports/sports_team_location/teams'] |
| ACE05 | ['PER-SOC', 'ART', 'ORG-AFF', 'GEN-AFF', 'PHYS', 'PART-WHOLE'] |

### PL-Marker: Packed Levitated Marker for Entity and Relation Extraction

Github: https://github.com/thunlp/PL-Marker/tree/master?tab=readme-ov-file \
Paper: https://arxiv.org/pdf/2109.06067.pdf

Research Institution: Tsinghua University

PL-Marker is a method for entity and relation extraction. The key innovation is the strategic use of levitated markers in the encoding phase to model the interrelation between spans and span pairs. Levitated markers are pairs of markers associated with a span, sharing the same position embedding with the start and end tokens of the corresponding span. They are used to classify multiple pairs of entities simultaneously and accelerate the inference process. The document also introduces neighborhood-oriented and subject-oriented packing strategies to consider the interrelation between spans and span pairs, enhancing the modeling of entity boundary information and the interrelation between same-subject span pairs.

PL-Marker uses different models for each dataset among ACE 2004, ACE2005, and SciERC:

| Dataset | Base Model | Relation Set |
|----------|----------|----------|
| ACE04 | albert-xxlarge-v1 or bert-base-uncased | ['PER-SOC', 'OTHER-AFF', 'ART', 'GPE-AFF', 'EMP-ORG', 'PHYS'] |
| ACE05 | albert-xxlarge-v1 or bert-base-uncased | ['PER-SOC', 'ART', 'ORG-AFF', 'GEN-AFF', 'PHYS', 'PART-WHOLE'] |
| SciERC | scibert_scivocab_uncased | ['PART-OF', 'USED-FOR', 'FEATURE-OF', 'CONJUNCTION', 'EVALUATE-FOR', 'HYPONYM-OF', 'COMPARE'] |
