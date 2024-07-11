# Relation Extraction Manual Evaluation

The excel sheets in this folder are initially created via the select_sample.py, then downloaded for manual evaluation and reuploaded. The evaluation metrics and guidelines are described in [evaluations](../README.md).

The metrics in the table below are also available in the excel sheets for their respective tools, and are summarized here for ease of comparison. 

|                          | # Triples Eval'd | Syntactic Acc | Semantic Acc | Consistency | # Hallucinations | # Triples | % Docs w/ Any Predicted Triples |
|--------------------------|------------------|---------------|--------------|-------------|------------------|-----------|---------------------------------|
| REBEL (pipeline)         | 181              | 0.863         | 0.298        | 0.987       | 3                | 4766      | 99.4                            |
| PL-Marker (bert) RE      | 18               | 1.0           | 0.944        | 1.0         | 0                | 289       | 1.01                            |
| PL-Marker (scierc) RE    | 9                | 1.0           | 0.556        | 1.0         | 0                | 127       | 4.00                            |
| Unirel                   | 6                | 0.25          | 0.0          | 1.0         | 0                | 87        | 1.96                            |
| PL-Marker (albert) RE    | 4                | 1.0           | 1.0          | 1.0         | 0                | 147       | 4.37                            |
