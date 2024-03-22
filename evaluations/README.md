# Correctness Evaluation


We evaluate the correctness of the tools in two ways: **automatic** and **manual**.

## Automatic Evaluation (AE)
The automatic evaluation is done by comparing the tool's output with the gold standard data, regarding Named Entity Recognition (NER) and Named Entity Linking (NEL) tasks, .
Evaluations. 

Evaluations are saved in the [automatic_evaluations folder](../data/automatic_evaluations/).

## Manual Evaluation (ME)
The manual evaluation is done by a domain expert who will evaluate the tool's output and the gold standard dat, regarding Coreference Resolution (CR) and Relation Extraction (RE) tasks. 

Evaluations are saved in the [manual_evaluations folder](../data/manual_evaluations/).


## Evaluations 
| Coreference Resolution         | Named Entity Linking (NEL)       | Relation Extraction (RE)   |
|-------------------------------|---------------------------------|---------------------------|
| [ ] ASP                       | [ ] BLINK                       | [x] REBEL (ME)            |
| [ ] coref_mt5                 | [x] spaCy EntityLinker (AE)     | [ ] UniRel                |
| [ ] s2e-coref                 | [ ] GENRE                       | [ ] DeepStruct            |
| [ ] neuralcoref               | [ ] ReFinED                     | [ ] PL-Marker             |


 x Evaluated 

## Methodology for Comparing Tool Outputs with the Gold Standard

### Correctness evaluation for NEL
For each named entity in the NEL gold standard, compare the tool's linking decision against it.\
If the linking decision is correct, then the tool's QId is the same as the gold standard QId.\
This comparison will allow us to calculate the metrics such as precision, recall, and F1 score.

Another approach to consider is the adoption of **Ontology-based Topological (OT) metrics** which use features derived from the structure (topology) of the underlying base ontology.\
We can use two **OT metrics**, **Jiang Conrath (JC) metric** and **Class similarity**.

- **Class similarity**: an ontology-based measure based on Jaccard Similarity of the respective super class sets of two nodes inversely weighted by the instance counts of the classes. For this measure classes high up in the ontology with very high transitive instance counts are weighted lower than more specific classes with lower counts.

- **Jiang Conrath (JC) metric**: an ontology-based measure using the interpretation at [KGTK Semantic Similarity](https://github.com/usc-isi-i2/kgtk-similarity) of the Jiang Conrath ontological distance (see https://arxiv.org/abs/cmp-lg/9709008).  
They use instance counts (same as used for `class`) to compute probabilities and normalize to the distance through the `entity` node (`Q351201`) to get a similarity. If a node pair has multiple most-specific subsumers, the maximum similarity based on those will be used.

Those metrics are implemented in the [KGTK Semantic Similarity](https://github.com/usc-isi-i2/kgtk-similarity).

### Correctness evaluation for RE
We need to define a process to make that comparison. We can use the following steps:
1. Extract the relations from the gold standard data.
2. Extract the relations from the tool's output.
3. Compare the relations from the tool's output against the gold standard relations.
   1. That comparisson can't be done directly because the tool's output and the gold standard data are in different formats. We need to find a way to make that comparisson.
4. Calculate the metrics such as precision, recall, and F1 score.

### Correctness evaluation for CR
[TODO]

### Correctness evaluation for NER
[TODO]