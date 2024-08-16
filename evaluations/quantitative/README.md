# Quantitative Evaluations

## NER

Usage:\
python ner_semeval.py -d path/to/results/to/evaluate.csv -t set_of_types_to_use\
Add the option "--untyped" to perform label-agnostic eval with UTFAA. The weak scores are equivalent to Partial and strong are equivalent to Exact\
Note that the environment requirements are specified in a comment at the top of the script.

### Un-Typed Evaluation using UTFAA:
|                                          | Precision (Weak) | Recall (Weak) | F1 (Weak)     | Precision (Strong) | Recall (Strong) | F1 (Strong) |
|------------------------------------------|------------------|---------------|---------------|--------------------|-----------------|-------------|
| PL-Marker (ACE-2005 bert)                | 0.78             | 0.27          | 0.4           | 0.68               | 0.24            | 0.35        |
| NLTK ne_chunk (uppercased) *             | 0.43             | 0.37          | 0.4           | 0.29               | 0.25            | 0.27        |
| spaCy EntityRecognizer (en_core_web_lg)  | 0.6              | 0.16          | 0.26          | 0.39               | 0.11            | 0.17        |
| flair (OntoNotes)                        | 0.68             | 0.16          | 0.25          | 0.59               | 0.14            | 0.22        |
| PL-Marker (ACE-2005 albert-xxl)          | 0.79             | 0.14          | 0.24          | 0.7                | 0.12            | 0.21        |
| spaCy EntityRecognizer (en_core_web_sm)  | 0.56             | 0.13          | 0.21          | 0.36               | 0.084           | 0.14        |
| stanza (ontonotes_electra-large)         | 0.73             | 0.1           | 0.18          | 0.66               | 0.094           | 0.16        |
| stanza (ontonotes-ww-multi_electra-large)| 0.59             | 0.096         | 0.17          | 0.51               | 0.082           | 0.14        |
| stanza (ontonotes_nocharlm)              | 0.63             | 0.075         | 0.13          | 0.44               | 0.053           | 0.094       |
| PL-Marker (SciERC scibert-uncased)       | 0.69             | 0.074         | 0.13          | 0.46               | 0.049           | 0.089       |
| flair (CoNLL-2003)                       | 0.77             | 0.064         | 0.12          | 0.64               | 0.053           | 0.098       |
| stanza (ontonotes-ww-multi_nocharlm)     | 0.49             | 0.071         | 0.12          | 0.38               | 0.055           | 0.096       |
| stanza (ontonotes_charlm)                | 0.71             | 0.066         | 0.12          | 0.51               | 0.047           | 0.086       |
| stanza (ontonotes-ww-multi_charlm)       | 0.64             | 0.045         | 0.084         | 0.42               | 0.029           | 0.055       |
| stanza (conll03_charlm)                  | 0.54             | 0.04          | 0.075         | 0.42               | 0.031           | 0.059       |
| NLTK ne_chunk (lowercased)               | 0.0              | 0.0           | --            | 0.0                | 0.0             | --          |

\* note that the difference between nltk's output when given upper vs lowercased input is cause to doubt its overall effectiveness

### Benchmark-Annotated GS Evaluation:

Note that we can't eval pl-marker's SciERC NER unless we make a SciERC GS, which is likely not worthwhile.

#### CoNLL-2003 Labeled Entities
|                                          |Prec (Strict)|Rec (Strict)|F1 (Strict)|Prec (Exact)|Rec (Exact)|F1 (Exact)|Prec (Partial)| Rec (Partial)|F1 (Partial)|Prec (Type)|Rec (Type)|F1 (Type)|
|------------------------------------------|-------------|------------|-----------|------------|-----------|----------|--------------|--------------|------------|-----------|----------|---------|
| flair (CoNLL-03)                         | 0.43        | 0.41       | 0.42      | 0.45       | 0.43      | 0.44     | 0.54         | 0.51         | 0.52       | 0.52      | 0.5      | 0.51    |
| stanza (conll03_charlm)                  | 0.21        | 0.18       | 0.2       | 0.24       | 0.2       | 0.22     | 0.33         | 0.28         | 0.3        | 0.34      | 0.3      | 0.32    |

#### OntoNotes Labeled Entities
|                                          |Prec (Strict)|Rec (Strict)|F1 (Strict)|Prec (Exact)|Rec (Exact)|F1 (Exact)|Prec (Partial)| Rec (Partial)|F1 (Partial)|Prec (Type)|Rec (Type)|F1 (Type)|
|------------------------------------------|-------------|------------|-----------|------------|-----------|----------|--------------|--------------|------------|-----------|----------|---------|
| stanza (ontonotes_electra-large)         | 0.59        | 0.7        | 0.64      | 0.6        | 0.72      | 0.66     | 0.65         | 0.78         | 0.71       | 0.66      | 0.79     | 0.72    |
| stanza (ontonotes-ww-multi_electra-large)| 0.41        | 0.55       | 0.47      | 0.42       | 0.56      | 0.48     | 0.49         | 0.66         | 0.57       | 0.51      | 0.68     | 0.58    |
| flair (OntoNotes)                        | 0.32        | 0.61       | 0.42      | 0.36       | 0.68      | 0.47     | 0.4          | 0.77         | 0.53       | 0.4       | 0.76     | 0.52    |
| stanza (ontonotes_charlm)                | 0.32        | 0.25       | 0.28      | 0.34       | 0.26      | 0.3      | 0.44         | 0.34         | 0.38       | 0.43      | 0.33     | 0.37    |
| stanza (ontonotes_nocharlm)              | 0.23        | 0.22       | 0.23      | 0.31       | 0.3       | 0.31     | 0.41         | 0.4          | 0.4        | 0.3       | 0.29     | 0.29    |
| stanza (ontonotes-ww-multi_nocharlm)     | 0.22        | 0.25       | 0.23      | 0.26       | 0.3       | 0.28     | 0.36         | 0.42         | 0.39       | 0.28      | 0.33     | 0.31    |
| stanza (ontonotes-ww-multi_charlm)       | 0.31        | 0.18       | 0.22      | 0.36       | 0.21      | 0.27     | 0.57         | 0.33         | 0.42       | 0.56      | 0.32     | 0.41    |
| spaCy EntityRecognizer (en_core_web_sm)  | 0.1         | 0.19       | 0.13      | 0.18       | 0.35      | 0.24     | 0.24         | 0.46         | 0.31       | 0.16      | 0.31     | 0.21    |
| spaCy EntityRecognizer (en_core_web_lg)  | 0.071       | 0.16       | 0.098     | 0.14       | 0.32      | 0.2      | 0.18         | 0.41         | 0.25       | 0.092     | 0.21     | 0.13    |

#### ACE Phase-1 (Restricted Set) Entities
|                                          |Prec (Strict)|Rec (Strict)|F1 (Strict)|Prec (Exact)|Rec (Exact)|F1 (Exact)|Prec (Partial)| Rec (Partial)|F1 (Partial)|Prec (Type)|Rec (Type)|F1 (Type)|
|------------------------------------------|-------------|------------|-----------|------------|-----------|----------|--------------|--------------|------------|-----------|----------|---------|
| nltk (uppercased)                        | 0.0066      | 0.022      | 0.01      | 0.087      | 0.3       | 0.13     | 0.13         | 0.44         | 0.2        | 0.024     | 0.081    | 0.037   |
| nltk (lowercased)                        | 0.0         | 0.0        | --        | 0.0        | 0.0       | --       | 0.0          | 0.0          | --         | 0.0       | 0.0      | --      |

#### ACE-2005 Entities
|                                          |Prec (Strict)|Rec (Strict)|F1 (Strict)|Prec (Exact)|Rec (Exact)|F1 (Exact)|Prec (Partial)| Rec (Partial)|F1 (Partial)|Prec (Type)|Rec (Type)|F1 (Type)|
|------------------------------------------|-------------|------------|-----------|------------|-----------|----------|--------------|--------------|------------|-----------|----------|---------|
| PL-Marker (ACE-2005 bert)                | 0.53        | 0.47       | 0.5       | 0.54       | 0.49      | 0.51     | 0.67         | 0.6          | 0.64       | 0.77      | 0.69     | 0.73    |
| PL-Marker (ACE-2005 albert-xxl)          | 0.62        | 0.28       | 0.39      | 0.62       | 0.28      | 0.39     | 0.78         | 0.35         | 0.49       | 0.92      | 0.42     | 0.58    |

## CR

Usage:\
python cr_eval.py -d path/to/results/to/evaluate.csv -i id_col -c corefs_col -g gold/standard/to/use.csv\
The last three options are optional, and default to c5_id, corefs, and ../../OMIn_dataset/gold_standard/gold/coref_gold.csv. Make sure to specify the id_col if it is something other than c5_id, like c5_unique_id\
Note that the environment requirements are listed on the top of the script in a comment.

To evaluate CR tools:
* python cr_eval.py -d ../../tool_results/s2e-coref/s2e-coref.csv
* python cr_eval.py -d ../../tool_results/asp/asp_base.csv
* python cr_eval.py -d ../../tool_results/asp/asp_large.csv
* python cr_eval.py -d ../../tool_results/asp/asp_xl.csv
* python cr_eval.py -d ../../tool_results/neuralcoref/neuralcoref_lg.csv -i c5
* python cr_eval.py -d ../../tool_results/neuralcoref/neuralcoref_sm.csv -i c5
* python cr_eval.py -d ../../tool_results/coref_mt5/coref_mt5.csv

Con12 F1, or CoNLL-2012 F1, refers to the F1 metric used in CoNLL-2012. This is an average of the F1 scores from MUC, B-CUBED (here represented as B3 for brevity), and CEAF.

|                              | MUC Prec | MUC Rec | MUC F1 | B3 Prec | B3 Rec | B3 F1 | CEAF Prec | CEAF Rec | CEAF F1 | Con12 F1 | LEA Prec | LEA Rec | LEA F1 |
|------------------------------|----------|---------|--------|---------|--------|-------|-----------|----------|---------|----------|----------|---------|--------|
| s2e-coref                    | 0.88     | 0.74    | 0.8    | 0.87    |0.73    |0.79   | 0.87      | 0.72     | 0.79    | 0.79     | 0.87     | 0.73    | 0.79   |
| ASP (t0-3b)                  | 0.7      | 0.74    | 0.72   | 0.73    | 0.77   | 0.75  | 0.77      | 0.81     | 0.79    | 0.75     | 0.69     | 0.73    | 0.71   |
| ASP (flant5-large)           | 0.7      | 0.74    | 0.72   | 0.73    | 0.77   | 0.75  | 0.77      | 0.81     | 0.79    | 0.75     | 0.69     | 0.73    | 0.71   |
| ASP (flant5-xl)              | 0.73     | 0.58    | 0.65   | 0.75    | 0.59   | 0.66  | 0.80      | 0.62     | 0.70    | 0.67     | 0.72     | 0.57    | 0.64   |
| ASP (flant5-base)            | 0.67     | 0.53    |0.59    | 0.68    |0.54    |0.60   | 0.73      | 0.56     | 0.64    | 0.61     | 0.66     | 0.511   | 0.58   |
| neuralcoref (en_core_web_lg) | 0.57     | 0.42    |0.48    | 0.59    |0.43    |0.50   | 0.59      | 0.46     | 0.52    | 0.50     | 0.57     | 0.41    | 0.47   |
| coref_mt5                    | 0.8      | 0.21    |0.33    | 0.85    |0.20    |0.32   | 0.76      | 0.21     | 0.33    | 0.33     | 0.8      | 0.19    | 0.31   |
| neuralcoref (en_core_web_sm) | 0.1      | 0.053   | 0.069  | 0.2     | 0.1    | 0.14  | 0.29      | 0.16     | 0.21    | 0.14     | 0.1      | 0.054   | 0.07   |

ASP t0-3b and flant5-large do in fact have different output across the entire FAA dataset, they just happen to have the same exact output for the sample set.

## NEL

Usage:\
python nel_eval.py -d path/to/results/to/evaluate.csv -i id_col -e ent_col -q qid_col -g gold/standard/to/use.csv\
The last four options are optional, and default to c5_id, entities, qids, and ../../OMIn_dataset/gold_standard/processed/nel.csv. Make sure to specify the column names if you want to use something different.\
**Important Note:** Blink and SpacyEntity Linker list entities as their Wikidata titles, and have seperate mentions columns that contain the literal mention from the text that was recognized as an entity. Therefore, when processing these, ent_col should be set to mentions, since the gold standard NEL entities use text mentions. ReFinED and GENRE list the actual mention from the text as the entity and have a title column with the Wikidata title, so their ent_col is the default, entities.

To evaluate NEL tools:
* python nel_eval.py -d ../../tool_results/refined/refined_wiki_wikidata.csv (and so on with other refined results)
* python nel_eval.py -d ../../tool_results/blink/blink.csv -q bi_qid
* python nel_eval.py -d ../../tool_results/blink/blink.csv -q cross_qid
* python nel_eval.py -d ../../tool_results/spacy_entity_linker/spacy_entitylinker_lg.csv
* python nel_eval.py -d ../../tool_results/spacy_entity_linker/spacy_entitylinker_sm.csv
* python nel_eval.py -d ../../tool_results/genre/genre_independent.csv

Note that genre_independent.csv and genre_grouped.csv always get the same scores, so we evaluate them as one

|                                         |Prec (Strong)|Rec (Strong)|F1 (Strong)|JC (Strong)|Class (Strong)|Prec (Weak)|Rec (Weak)|F1 (Weak)|JC (Weak)|Class (Weak)|Prec (Flex)|Rec (Flex)|F1 (Flex)|JC (Flex)|Class (Flex)|
|-----------------------------------------|-------------|------------|-----------|-----------|--------------|-----------|----------|---------|---------|------------|-----------|----------|---------|---------|------------|
| spaCy EntityLinker (en_core_web_lg)     | 0.19        | 0.2        | 0.19      | 0.15      | 0.082        | 0.15      | 0.3      | 0.2     | 0.13    | 0.069      | 0.15      | 0.18     | 0.16    | 0.14    | 0.077      |
| spaCy EntityLinker (en_core_web_sm)     | 0.17        | 0.21       | 0.19      | 0.15      | 0.073        | 0.14      | 0.3      | 0.19    | 0.14    | 0.071      | 0.15      | 0.17     | 0.16    | 0.15    | 0.082      |
| BLINK (biencoder)                       | 0.64        | 0.068      | 0.12      | 0.82      | 0.77         | 0.57      | 0.08     | 0.14    | 0.68    | 0.64       | 0.64      | 0.052    | 0.096   | 0.8     | 0.75       |
| BLINK (crossencoder)                    | 0.61        | 0.065      | 0.12      | 0.82      | 0.77         | 0.52      | 0.074    | 0.13    | 0.64    | 0.6        | 0.61      | 0.05     | 0.092   | 0.8     | 0.75       |
| ReFinED (wiki_w_numbers, wikipedia)     | 0.67        | 0.058      | 0.11      | 0.89      | 0.87         | 0.53      | 0.056    | 0.1     | 0.84    | 0.81       | 0.71      | 0.049    | 0.092   | 0.9     | 0.88       |
| ReFinED (wiki_w_numbers, wikidata)      | 0.72        | 0.058      | 0.11      | 0.89      | 0.87         | 0.57      | 0.056    | 0.1     | 0.8     | 0.78       | 0.76      | 0.049    | 0.092   | 0.9     | 0.89       |
| ReFinED (wiki, wikidata)                | 0.35        | 0.03       | 0.055     | 0.84      | 0.74         | 0.3       | 0.041    | 0.073   | 0.74    | 0.65       | 0.36      | 0.028    | 0.051   | 0.82    | 0.72       |
| ReFinED (wiki, wikipedia)               | 0.33        | 0.03       | 0.055     | 0.8       | 0.71         | 0.29      | 0.041    | 0.073   | 0.71    | 0.62       | 0.35      | 0.028    | 0.051   | 0.78    | 0.69       |
| GENRE                                   | 0.12        | 0.0032     | 0.0063    | 0.32      | 0.28         | 0.059     | 0.0033   | 0.0063  | 0.27    | 0.2        | 0.2       | 0.0045   | 0.0087  | 0.37    | 0.33       |
| ReFinED (aida, wikidata)                | 0.0         | 0.0        | 0.0       | 0.84      | 0.48         | 0.17      | 0.0032   | 0.0063  | 0.73    | 0.5        | 0.0       | 0.0      | 0.0     | 0.61    | 0.33       |
| ReFinED (aida, wikipedia)               | 0.0         | 0.0        | 0.0       | 0.56      | 0.32         | 0.0       | 0.0      | 0.0     | 0.49    | 0.25       | 0.0       | 0.0      | 0.0     | 0.46    | 0.25       |
