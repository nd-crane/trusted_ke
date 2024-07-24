# Automatic Evaluations

## NER

Usage:\
python ner_semeval.py -d path/to/results/to/evaluate.csv -g gold/standard/to/use.csv\
Add the option "--untyped" to perform label-agnostic eval with UTFAA. The weak scores are equivalent to Partial and strong are equivalent to Exact\
Note that the environment requirements are specified in a comment at the top of the script.

To evaluate NER tools:
* python ner_semeval.py -d ../../data/results/flair/flair_ner.csv -g ../../gold_standard/processed/ner_conll.csv
* python ner_semeval.py -d ../../data/results/stanza/stanza_ner.csv -g ../../gold_standard/processed/ner_on.csv
* python ner_semeval.py -d ../../data/results/spacy_entityrecognizer/spacy_ner_lg.csv -g ../../gold_standard/processed/ner_on.csv
* python ner_semeval.py -d ../../data/results/spacy_entityrecognizer/spacy_ner_sm.csv -g ../../gold_standard/processed/ner_on.csv
* python ner_semeval.py -d ../../data/results/nltk/nltk_ner_uppercased.csv -g ../../gold_standard/processed/ner_ace_nltk.csv
* python ner_semeval.py -d ../../data/results/pl-marker/pl-marker_ace05_bert_NER_jun17.csv -g ../../gold_standard/processed/ner_ace.csv
* python ner_semeval.py -d ../../data/results/pl-marker/pl-marker_ace05_albert_NER_jun17.csv -g ../../gold_standard/processed/ner_ace.csv

Note that we can't eval pl-marker's SciERC NER unless we make a SciERC GS, which is likely not worthwhile.

### Maintenance Un-Typed Entities

|                                         | Precision (Weak) | Recall (Weak) | F1 (Weak)     | Precision (Strong) | Recall (Strong) | F1 (Strong) |
|-----------------------------------------|-----------|---------|---------|------------------|---------------|-----------|
| nltk ne_chunk (uppercased) *            | 0.51893   | 0.46047 | 0.48796 | 0.31659          | 0.28656       | 0.30082   |
| spaCy EntityRecognizer (en_core_web_sm) | 0.74638   | 0.20356 | 0.31988 | 0.28571          | 0.06719       | 0.10880   |
| stanza                                  | 0.84091   | 0.07312 | 0.13455 | 0.36111          | 0.02569       | 0.04797   |
| PL-Marker (ACE05 bert) NER              | 0.03886   | 0.33399 | 0.06962 | 0.03286          | 0.28063       | 0.05882   |
| PL-Marker (SciERC) NER                  | 0.03846   | 0.13241 | 0.05961 | 0.01471          | 0.04941       | 0.02267   |
| flair                                   | 0.04745   | 0.07905 | 0.05930 | 0.03325          | 0.05534       | 0.04154   |
| PL-Marker (ACE05 albert-xxl) NER        | 0.03577   | 0.17194 | 0.05922 | 0.03139          | 0.15020       | 0.05193   |
| spaCy EntityRecognizer (en_core_web_lg) | 0.03099   | 0.24506 | 0.05503 | 0.01430          | 0.11265       | 0.02537   |
| nltk ne_chunk (lowercased)              | 0         | 0.0     | 0       | 0                | 0.0           | 0         |

\* note that the difference between nltk's output when given upper vs lowercased input is cause to doubt its overall effectiveness

**New results using SemEval script**
[TO-DO]

The results below are the ones included in the paper, but need to be updated:

### CoNLL-2003 Labeled Entities
|                                         | Strict  | Exact  | Partial  | Type    |
|-----------------------------------------|---------|--------|----------|---------|
| flair                                   | 0.4186  | 0.4419 | 0.5233   | 0.5116  |

### OntoNotes Labeled Entities
|                                         | Strict  | Exact  | Partial  | Type    |
|-----------------------------------------|---------|--------|----------|---------|
| stanza                                  | 0.2292  | 0.2917 | 0.4375   | 0.4167  |
| spaCy EntityRecognizer (en_core_web_sm) | 0.1341  | 0.2458 | 0.3073   | 0.2123  |
| spaCy EntityRecognizer (en_core_web_lg) | 0.0995  | 0.199  | 0.2587   | 0.1294  |

### ACE Phase-1 (Restricted Set) Entities
|                                         | Strict  | Exact  | Partial  | Type    |
|-----------------------------------------|---------|--------|----------|---------|
| nltk (uppercased)                       | 0.01015 | 0.1218 | 0.1929   | 0.03723 |

### ACE-2005 Entities
|                                         | Strict  | Exact  | Partial  | Type    |
|-----------------------------------------|---------|--------|----------|---------|
| PL-Marker (ACE05 bert) NER              | 0.5093  | 0.5252 | 0.6525   | 0.7533  |
| PL-Marker (ACE05 albert-xxl) NER        | 0.3958  | 0.3958 | 0.4982   | 0.5866  |

## CR

Usage:\
python cr_eval.py -d path/to/results/to/evaluate.csv -i id_col -c corefs_col -g gold/standard/to/use.csv\
The last three options are optional, and default to c5_id, corefs, and ../../gold_standard/gold/coref_gold.csv. Make sure to specify the id_col if it is something other than c5_id, like c5_unique_id\
Note that the environment requirements are listed on the top of the script in a comment.

To evaluate CR tools:
* python cr_eval.py -d ../../data/results/s2e-coref/s2e-coref_updated_format.csv
* python cr_eval.py -d ../../data/results/asp/asp.csv
* python cr_eval.py -d ../../data/results/ncoref/crosslingual_coref_with_errors.csv -i c5
* python cr_eval.py -d ../../data/results/coref_mt5/coref_mt5.csv

Con12 F1, or CoNLL-2012 F1, refers to the F1 metric used in CoNLL-2012. This is an average of the F1 scores from MUC, B-CUBED (here represented as B3 for brevity), and CEAF.

|             | MUC Prec | MUC Rec | MUC F1 | B3 Prec | B3 Rec | B3 F1 | CEAF Prec | CEAF Rec | CEAF F1 | Con12 F1 | LEA Prec | LEA Rec | LEA F1 |
|-------------|----------|---------|--------|---------|--------|-------|-----------|----------|---------|----------|----------|---------|--------|
| s2e-coref   | 0.87500  | 0.73684 |0.80000 | 0.87097 |0.72973 |0.79412| 0.86667   | 0.72222  | 0.78788 | 0.79400  | 0.87097  | 0.72973 | 0.79412|
| ASP         | 0.66666  | 0.52632 |0.58824 | 0.68391 |0.53604 |0.60101| 0.72619   | 0.56481  | 0.63542 | 0.60822  | 0.65517  | 0.51351 | 0.57576|
| neuralcoref | 0.57143  | 0.42105 |0.48485 | 0.58929 |0.42793 |0.49581| 0.59286   | 0.46111  | 0.51875 | 0.49980  | 0.57143  | 0.40541 | 0.47431|
| coref_mt5   | 0.80000  | 0.21053 |0.33333 | 0.85000 |0.19820 |0.32144| 0.76000   | 0.21111  | 0.33043 | 0.32840  | 0.80000  | 0.18919 | 0.30601|

## NEL

Usage:\
python nel_eval.py -d path/to/results/to/evaluate.csv -i id_col -e ent_col -q qid_col -g gold/standard/to/use.csv\
The last four options are optional, and default to c5_id, entities, qids, and ../../gold_standard/processed/nel.csv. Make sure to specify the column names if you want to use something different.\
**Important Note:** Blink and SpacyEntity Linker list entities as their Wikidata titles, and have seperate mentions columns that contain the literal mention from the text that was recognized as an entity. Therefore, when processing these, ent_col should be set to mentions, since the gold standard NEL entities use text mentions. ReFinED and GENRE list the actual mention from the text as the entity and have a title column with the Wikidata title, so their ent_col is the default, entities.

To evaluate NEL tools:
* python nel_eval.py -d ../../data/results/refined/refined.csv -q ids
* python nel_eval.py -d ../../data/results/blink/blink_results_new.csv -e mention -q bi_qid
* python nel_eval.py -d ../../data/results/blink/blink_results_new.csv -e mention -q cross_qid
* python nel_eval.py -d ../../data/results/spacy_entity_linker/spacy_entitylinker.csv -e mentions
* python nel_eval.py -d ../../data/results/genre/genre_independent.csv -i c5_unique_id

Note that genre_independent.csv and genre_grouped.csv always get the same scores, so we evaluate them as one

### NEL Eval (Strong Matching - Strong Matching and Primary GS)
|                                         | Precision | Recall  | F1      | JC Similarity | Class Similarity |
|-----------------------------------------|-----------|---------|---------|---------------|------------------|
| ReFinED                                 | 0.58333   | 0.03590 | 0.06763 | 0.80268  | 0.83960     |
| BLINK (biencoder)                       | 0.63636   | 0.03571 | 0.06763 | 0.69958  | 0.74749     |
| BLINK (crossencoder)                    | 0.63636   | 0.03571 | 0.06763 | 0.65093  | 0.71347     |
| spaCy EntityLinker (en_core_web_lg)     | 0.13426   | 0.13615 | 0.13520 | 0.06686  | 0.12793     |
| GENRE                                   | 0.0       | 0.0     | 0       | 0.11320  | 0.24401     |

### NEL Eval (Weak Matching - Weak Matching and Primary GS)
|                                         | Precision | Recall  | F1      | JC Similarity | Class Similarity |
|-----------------------------------------|-----------|---------|---------|---------------|------------------|
| spaCy EntityLinker (en_core_web_lg)     | 0.11871   | 0.21290 | 0.15242 | 0.05244  | 0.10101     |
| BLINK (crossencoder)                    | 0.60606   | 0.05168 | 0.09524 | 0.64975  | 0.68388     |
| BLINK (biencoder)                       | 0.60606   | 0.05168 | 0.09524 | 0.64523  | 0.68311     |
| ReFinED                                 | 0.46666   | 0.03646 | 0.06763 | 0.67026  | 0.70516     |
| GENRE                                   | 0.0625    | 0.00260 | 0.00499 | 0.21851  | 0.24305     |

### NEL Eval (Flexible - Strong Matching and Extended GS (Specific Entities w/o QIDs Given General QID))
|                                         | Precision | Recall  | F1      | JC Similarity | Class Similarity |
|-----------------------------------------|-----------|---------|---------|---------------|------------------|
| spaCy EntityLinker (en_core_web_lg)     | 0.11905   | 0.13216 | 0.12526 | 0.06507  | 0.11494     |
| ReFinED                                 | 0.58333   | 0.03189 | 0.06048 | 0.80268  | 0.83960     |
| BLINK (biencoder)                       | 0.63636   | 0.03175 | 0.06048 | 0.69958  | 0.74749     |
| BLINK (crossencoder)                    | 0.63636   | 0.03175 | 0.06048 | 0.65093  | 0.71347     |
| GENRE                                   | 0.0       | 0.0     | 0       | 0.11320  | 0.24401     |