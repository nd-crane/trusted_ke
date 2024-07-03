# Automatic Evaluations

### NER

|                                  | Precision | Recall  | F1      | Precision Strict | Recall Strict | F1 Strict |
|----------------------------------|-----------|---------|---------|------------------|---------------|-----------|
| nltk ne_chunk (uppercased) *     | 0.51893   | 0.46047 | 0.48796 | 0.31659          | 0.28656       | 0.30082   |
| spaCy                            | 0.74638   | 0.20356 | 0.31988 | 0.28571          | 0.06719       | 0.10880   |
| stanza                           | 0.84091   | 0.07312 | 0.13455 | 0.36111          | 0.02569       | 0.04797   |
| PL-Marker (ACE05 bert) NER       | 0.03886   | 0.33399 | 0.06962 | 0.03286          | 0.28063       | 0.05882   |
| PL-Marker (SciERC) NER           | 0.03846   | 0.13241 | 0.05961 | 0.01471          | 0.04941       | 0.02267   |
| flair / Blink NER                | 0.04745   | 0.07905 | 0.05930 | 0.03325          | 0.05534       | 0.04154   |
| PL-Marker (ACE05 albert-xxl) NER | 0.03577   | 0.17194 | 0.05922 | 0.03139          | 0.15020       | 0.05193   |
| nltk ne_chunk (lowercased)       | 0         | 0.0     | 0       | 0                | 0.0           | 0         |

\* note that the difference between nltk's output when given upper vs lowercased input is cause to doubt its overall effectiveness
