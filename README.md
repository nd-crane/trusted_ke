# Survey of Knowledge Extraction Tools for Maintenance Data

University of Notre Dame | Center for Research Computing | Trusted AI\
Kate Mealey, Jonathan Karr, Danny Finch, Alyssa Riter, Priscila Moreira, Eli Phillips, Paul Brenner, Charles Vardeman

---
Released code from our paper: ____\
Please open an issue if there are any questions.

---


The following is a survey of knowledge extraction tools for maintenance data. The survey includes tools for Named Entity Recognition (NER), Coreference Resolution (CR), Named Entity Linking (NEL), and Relation Extraction (RE). The survey provides an overview of each tool's methodology, base model, and relation set, where applicable. 

The survey also includes a comparison of the tools' outputs with the [gold standard data](gold_standard/README.md), which is a subset of the Complete Set of FAA data created to evaluate the correctness of the tools regarding NER, NEL, and RE tasks.

KE tools at a glance:

| Coreference Resolution         | Named Entity Linking (NEL)       | Relation Extraction (RE)   |
|-------------------------------|---------------------------------|---------------------------|
| [ ] ASP                       | [x] BLINK                       | [x] REBEL                 |
| [ ] coref_mt5                 | [x] spaCy EntityLinker          | [ ] UniRel                |
| [ ] s2e-coref                 | [ ] GENRE                       | [ ] DeepStruct            |
| [x] neuralcoref               | [ ] ReFinED                     | [x] PL-Marker             |

---

## Coreference Resolution

### ASP: Autoregressive Structured Prediction with Language Models

Github: https://github.com/lyutyuh/ASP \
Paper: https://arxiv.org/pdf/2210.14698.pdf

Research Institution: Google Research

The Autoregressive Structured Prediction (ASP) framework represents structures as sequences of actions to build pieces of the target structure step by step. It focuses on tasks such as named entity recognition, end-to-end relation extraction, and coreference resolution, achieving state-of-the-art results without relying on data augmentation or task-specific feature engineering. The ASP framework utilizes a conditional language model to predict structure-building actions, allowing the model to capture intra-structure dependencies more effectively while leveraging pre-trained language models.

Base Model: T5

### coref_mt5: Coreference Resolution through a seq2seq Transition-Based System

Github: https://github.com/google-research/google-research/tree/master/coref_mt5 \
Paper: https://arxiv.org/pdf/2211.12142v1.pdf

Research Institution: Google Research

coref_mt5's methodology for coreference resolution involves a text-to-text (seq2seq) approach, where a single sentence, along with prior context, is encoded as a string and fed into a model to predict coreference links. The system utilizes a transition-based approach, particularly the Link-Append system, which encodes prior coreference decisions in the input to the seq2seq model and predicts new coreference links as its output.

Base Model: mT5

### s2e-coref: Start-To-End Coreference Resolution

Github: https://github.com/yuvalkirstain/s2e-coref \
Paper: https://aclanthology.org/2021.acl-short.3.pdf

Research Institution: University of Tel Aviv

The s2e coreference resolution model introduces a lightweight approach that eliminates the need for constructing span representations, handcrafted features, and pruning heuristics. Instead, it propagates information to the boundaries of spans and computes mention and antecedent scores through a series of bilinear functions over their contextualized representations, resulting in a significantly lighter memory footprint and the ability to process multiple documents in a single batch without truncation or sliding windows. This approach stands out for its simplicity, efficiency, and reliance on lightweight bilinear functions between pairs of endpoint token representations, distinguishing it from the more complex and memory-intensive standard models.

Base Model: longformer-large

### neuralcoref

Github: https://github.com/huggingface/neuralcoref \
Blog Post: https://medium.com/huggingface/state-of-the-art-neural-coreference-resolution-for-chatbots-3302365dcf30

Created by spaCy

Neuralcoref's methodology for coreference resolution involves training a neural model on a non-probabilistic slack-rescaled max-margin objective, which computes scores for pairs of mentions and individual mentions. This scoring system is an adaptation of previous work by Kevin Clark and Christopher Manning, utilizing deep-learning python tools, spaCy for high-speed parsing, and recent word embedding techniques to compute embeddings for unknown words on the fly. The system also incorporates speaker information in the conversation and is implemented on top of spaCy and Numpy, making it unique in its approach to handling informal language and speaker context in coreference resolution.

Not LLM-based

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

From https://spacy.io/api/entitylinker :\
"An EntityLinker component disambiguates textual mentions (tagged as named entities) to unique identifiers, grounding the named entities into the “real world”. It requires a KnowledgeBase, as well as a function to generate plausible candidates from that KnowledgeBase given a certain textual mention, and a machine learning model to pick the right candidate, given the local context of the mention. EntityLinker defaults to using the InMemoryLookupKB implementation."

Not LLM-based

### GENRE: Generative ENtity REtrieval

Github: https://github.com/facebookresearch/GENRE \
Paper: https://arxiv.org/pdf/2010.00904.pdf

Research Institution: Facebook AI Research

GENRE's methodology for named entity linking involves utilizing a sequence-to-sequence model to generate textual entity identifiers, or entity names, in an autoregressive manner. This approach allows GENRE to directly capture the relations between context and entity names, effectively cross-encoding both, and to efficiently compute the exact softmax for each output token without the need for negative data downsampling. Additionally, GENRE employs a constrained decoding strategy that forces each generated name to be in a predefined candidate set, ensuring that the generated output is a valid entity name.

Base Model: BART

### ReFinED: Representation and Fine-grained typing for Entity Disambiguation

Github: https://github.com/amazon-science/ReFinED \
Papers: https://arxiv.org/pdf/2207.04108.pdf, https://arxiv.org/pdf/2207.04106.pdf

Research Institution: Amazon Alexa AI

ReFinED is an efficient end-to-end entity linking model that utilizes fine-grained entity types and entity descriptions to perform mention detection, fine-grained entity typing, and entity disambiguation in a single forward pass. It targets a large catalog of entities, including zero-shot entities, and is capable of generalizing to large-scale knowledge bases such as Wikidata. ReFinED's unique approach involves combining information from entity types and descriptions in a simple transformer-based encoder, which yields strong performance and scalability for web-scale information extraction.

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
