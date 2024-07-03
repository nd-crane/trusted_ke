# Automatic Evaluations

### NER

|                                  | Precision | Recall  | F1      |
|----------------------------------|-----------|---------|---------|
| flair                            | 0.04745   | 0.07905 | 0.05930 |
| spaCy                            | 0.74638   | 0.20356 | 0.31988 |
| stanza                           | 0.84091   | 0.07312 | 0.13455 |
| nltk ne_chunk (uppercased)       | 0.51893   | 0.46047 | 0.48796 |
| nltk ne_chunk (lowercased)       | 0.00000   | 0.00000 | 0.00000 |
| PL-Marker (SciERC) NER           | 0.03846   | 0.13241 | 0.05961 |
| PL-Marker (ACE05 bert) NER       | 0.03886   | 0.33399 | 0.06962 |
| PL-Marker (ACE05 albert-xxl) NER |    |  |  |