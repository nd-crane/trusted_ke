# Automatic Evaluations

### NER

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

|                                         | Precision (Weak) | Recall (Weak) | F1 (Weak) | Precision (Strong) | Recall (Strong) | F1 (Strong) |
|-----------------------------------------|------------------|---------------|-----------|--------------------|-----------------|-------------|
| spacy_entityrecognizer (en_core_web_sm) | 0.74638          | 0.20356       | 0.31988   | 0.28571            | 0.067194        | 0.1088      |
| stanza                                  | 0.84091          | 0.073123      | 0.13455   | 0.36111            | 0.025692        | 0.04797     |
| flair                                   | 0.04745          | 0.079051      | 0.059303  | 0.033254           | 0.055336        | 0.041543    |
| spacy_entityrecognizer (en_core_web_lg) | 0.030992         | 0.24506       | 0.055026  | 0.014296           | 0.11265         | 0.025373    |

### CR

Con12 F1, or CoNLL-2012 F1, refers to the F1 metric used in CoNLL-2012. This is an average of the F1 scores from MUC, B-CUBED (here represented as B3 for brevity), and CEAF.

|             | MUC Prec | MUC Rec | MUC F1 | B3 Prec | B3 Rec | B3 F1 | CEAF Prec | CEAF Rec | CEAF F1 | Con12 F1 | LEA Prec | LEA Rec | LEA F1 |
|-------------|----------|---------|--------|---------|--------|-------|-----------|----------|---------|----------|----------|---------|--------|
| s2e-coref   | 0.87500  | 0.73684 |0.80000 | 0.87097 |0.72973 |0.79412| 0.86667   | 0.72222  | 0.78788 | 0.79400  | 0.87097  | 0.72973 | 0.79412|
| ASP         | 0.66666  | 0.52632 |0.58824 | 0.68391 |0.53604 |0.60101| 0.72619   | 0.56481  | 0.63542 | 0.60822  | 0.65517  | 0.51351 | 0.57576|
| neuralcoref | 0.57143  | 0.42105 |0.48485 | 0.58929 |0.42793 |0.49581| 0.59286   | 0.46111  | 0.51875 | 0.49980  | 0.57143  | 0.40541 | 0.47431|
| coref_mt5   | 0.80000  | 0.21053 |0.33333 | 0.85000 |0.19820 |0.32144| 0.76000   | 0.21111  | 0.33043 | 0.32840  | 0.80000  | 0.18919 | 0.30601|

### NEL

#### NEL Eval (Strong Matching and Primary Gold Standard)
|                                         | Precision | Recall  | F1      | JC Similarity | Class Similarity |
|-----------------------------------------|-----------|---------|---------|---------------|------------------|
| ReFinED                                 | 0.58333   | 0.03590 | 0.06763 | 0.80268  | 0.83960     |
| BLINK (biencoder)                       | 0.63636   | 0.03571 | 0.06763 | 0.69958  | 0.74749     |
| BLINK (crossencoder)                    | 0.63636   | 0.03571 | 0.06763 | 0.65093  | 0.71347     |
| spaCy EntityLinker (en_core_web_lg)     | 0.13426   | 0.13615 | 0.13520 | 0.06686  | 0.12793     |
| GENRE                                   | 0.0       | 0.0     | 0       | 0.11320  | 0.24401     |

#### NEL Eval (Weak Matching and Primary Gold Standard)
|                                         | Precision | Recall  | F1      | JC Similarity | Class Similarity |
|-----------------------------------------|-----------|---------|---------|---------------|------------------|
| spaCy EntityLinker (en_core_web_lg)     | 0.11871   | 0.21290 | 0.15242 | 0.05244  | 0.10101     |
| BLINK (crossencoder)                    | 0.60606   | 0.05168 | 0.09524 | 0.64975  | 0.68388     |
| BLINK (biencoder)                       | 0.60606   | 0.05168 | 0.09524 | 0.64523  | 0.68311     |
| ReFinED                                 | 0.46666   | 0.03646 | 0.06763 | 0.67026  | 0.70516     |
| GENRE                                   | 0.0625    | 0.00260 | 0.00499 | 0.21851  | 0.24305     |

#### NEL Eval (Strong Matching and Extended GS, Specific Entities w/o QIDs Given General QID
|                                         | Precision | Recall  | F1      | JC Similarity | Class Similarity |
|-----------------------------------------|-----------|---------|---------|---------------|------------------|
| spaCy EntityLinker (en_core_web_lg)     | 0.11905   | 0.13216 | 0.12526 | 0.06507  | 0.11494     |
| ReFinED                                 | 0.58333   | 0.03189 | 0.06048 | 0.80268  | 0.83960     |
| BLINK (biencoder)                       | 0.63636   | 0.03175 | 0.06048 | 0.69958  | 0.74749     |
| BLINK (crossencoder)                    | 0.63636   | 0.03175 | 0.06048 | 0.65093  | 0.71347     |
| GENRE                                   | 0.0       | 0.0     | 0       | 0.11320  | 0.24401     |

#### NEL NER Eval
|                                         | Precision (Weak) | Recall (Weak) | F1 (Weak)     | Precision (Strong) | Recall (Strong) | F1 (Strong) |
|-----------------------------------------|-----------|---------|---------|------------------|---------------|-----------|
| GENRE                                   | 0.96      | 0.04743 | 0.09040 | 0.30435          | 0.01383       | 0.02647   |
| ReFinED                                 | 0.03266   | 0.09881 | 0.04909 | 0.02090          | 0.06324       | 0.03142   |
| BLINK (crossencoder)                    | 0.03403   | 0.07708 | 0.04722 | 0.01773          | 0.03953       | 0.02448   |
| BLINK (biencoder)                       | 0.02890   | 0.06522 | 0.04005 | 0.01597          | 0.03557       | 0.02205   |
| spaCy EntityLinker (en_core_web_lg)     | 0.01602   | 0.54150 | 0.03111 | 0.01051          | 0.35375       | 0.02041   |


