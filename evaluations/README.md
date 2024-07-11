# Correctness Evaluation


We evaluate the correctness of the tools in two ways: **automatic** and **manual**.

## Automatic Evaluation (AE)
The automatic evaluation is done by comparing the tool's output with the gold standard data, regarding Named Entity Recognition (NER), Coreference Resolution (CR), and Named Entity Linking (NEL) tasks.
Evaluations. 

Evaluations are saved in the [automatic_evaluations folder](../data/automatic_evaluations/).

## Manual Evaluation (ME)
The manual evaluation is done by a domain expert who will evaluate the tool's output and the gold standard data, regarding Relation Extraction (RE) tasks. 

Evaluations are saved in the [manual_evaluations folder](../data/manual_evaluations/).


| Named Entity Recognition (NER)| Coreference Resolution (CR)   | Named Entity Linking (NEL)       | Relation Extraction (RE)   |
|-------------------------------|-------------------------------|---------------------------------|---------------------------|
| [x] spaCy EntityRecognizer    | [ ] ASP                       | [x] BLINK                       | [x] REBEL                 |
| [x] flair NER                 | [x] coref_mt5                 | [x] spaCy EntityLinker          | [ ] UniRel                |
| [x] stanza NERProcessor       | [x] s2e-coref                 | [x] GENRE                       | [ ] DeepStruct            |
| [x] nltk ne_chunk             | [x] neuralcoref               | [x] ReFinED                     | [ ] PL-Marker (SciERC)    |
| [x] PL-Marker (SciERC) NER    |                               |                                 | [ ] PL-Marker (ACE05 bert) |
| [x] PL-Marker (ACE05 bert) NER |                              |                                 | [ ] PL-Marker (ACE05 albert-xxl) |
| [x] PL-Marker (ACE05 albert-xxl) NER |                        |                                 |                           |


 x Evaluated 

## Methodology for Comparing Tool Outputs with the Gold Standard

### Correctness evaluation for NER

We provide two F1 metrics for NER evaluation: a strict and a non-strict. The strict evaluation counts a predicted entity as correct only if it exactly matches a gold standard entity. In the non-strict evaluation, a predicted entity is counted correct if it contains any substring of the gold standard entity, or if the gold standard entity contains any substring of the predicted entity.

We do not evaluate correctness of entity labels.

*Note:* Some tools, like PL-Marker, run an NER subtask as well as their primary function. We provide an NER evaluation for those tools as well, and they are listed with the label "NER" in the automatic README. On top of that, we also do an NER evaluation of each NEL tool, using the entities found for entity linking. This is not intended as a primary metric for NEL evaluation. 

### Correctness evaluation for CR

We report 4 metrics for CR evaluation, because they each capture a different aspect of a tool's performance:
* MUC (Vilain et al., 1995)
* B-CUBED (Bagga and Baldwin, 1998)
* CEAF (Luo, 2005)
* LEA (Moosavi and Strube, 2016)
We also follow CoNLL-2012 in reporting the unweighted average of MUC, B-CUBED, and CEAF

### Correctness evaluation for NEL

Our NEL evaluation approach is the following.

For each named entity in the NEL gold standard, compare the tool's linking decision against it.\
If the linking decision is correct, then the tool's QId is the same as the gold standard QId.\
This comparison will allow us to calculate the metrics such as precision, recall, and F1 score.

Another approach to consider is the adoption of **Ontology-based Topological (OT) metrics** which use features derived from the structure (topology) of the underlying base ontology.\
We can use two **OT metrics**, **Jiang Conrath (JC) metric** and **Class similarity**.

- **Class similarity**: an ontology-based measure based on Jaccard Similarity of the respective super class sets of two nodes inversely weighted by the instance counts of the classes. For this measure classes high up in the ontology with very high transitive instance counts are weighted lower than more specific classes with lower counts.

- **Jiang Conrath (JC) metric**: an ontology-based measure using the interpretation at [KGTK Semantic Similarity](https://github.com/usc-isi-i2/kgtk-similarity) of the Jiang Conrath ontological distance (see https://arxiv.org/abs/cmp-lg/9709008).  
They use instance counts (same as used for `class`) to compute probabilities and normalize to the distance through the `entity` node (`Q351201`) to get a similarity. If a node pair has multiple most-specific subsumers, the maximum similarity based on those will be used.

Those metrics are implemented in the [KGTK Semantic Similarity](https://github.com/usc-isi-i2/kgtk-similarity).

See below an example of the output of the KGTK Semantic Similarity tool:

|    | q1        | q2        | q2_description                                        | q2_label          | class    | jc       |
|----|-----------|-----------|-------------------------------------------------------|-------------------|----------|----------|
| 0  | Q1875633 | Q1875633 | propellents used to power aircraft or aviation...    | aviation fuel     | 1.000000 | 1.000000 |
| 1  | Q1875633 | Q42501    | any material that stores energy that can later...    | combustible matter| 0.684539 | 0.885428 |
| 2  | Q1875633 | Q15766923 | scientific journal                                    | Fuel              | 0.029833 | 0.062413 |
| 3  | Q1875633 | Q5507117  | short-lived Bay Area post-hardcore musical act       | Fuel              | 0.000000 | 0.000000 |


We take our gold standard entities from the NER gold standard, and found their correct QIDs by manual lookup.

However, we note that many NER methods may create different output than our gold standard entities, and we do not want to penalize NEL tools for NER discrepancies. For example, in the sentence "WHILE TAXIING LOST NOSEWHEEL STEERING AND BRAKES",  we have "nosewheel steering" as an entity in our NER gold standard, since we prefer to include identity-changing modifiers for NER. In case an NEL tool only recognizes "steering" as the entity and links it to the QID for steering correctly (Q18891017), we perform a separate NER evaluation, and obtain a semantic similarity score of 1.000000 for the link between steering and Q18891017.

To accomplish this, in our NEL gold standard, we included primary, secondary, and up to tertiary entity-QID pairs for entities like "nosewheel steering," where subspans of the primary entity perform the same function in the sentence as the primary entity. This also accomodates those entities which do not have a QID themselves, but have a subspan which does (see Case 1).

<table>
 <row>
  <td>

   **Example**: FORWARD CARGO DOOR OPENED AS AIRCRAFT TOOK OFF. OBJECTS DROPPED OUT. RETURNED. FAILED TO SEE WARNING LIGHT.

Our gold standard holds that “FORWARD CARGO DOOR” is the correct entity to recognize, but also lists secondary and tertiary entities, “CARGO DOOR” and “DOOR” with their correct QIDs.

*Case 1*: Tool recognizes FORWARD CARGO DOOR as the entity and returns QIDx
FORWARD CARGO DOOR does not have a QID, so we move to the secondary entity/QID pair - we get the semantic distance between QIDx and the QID for CARGO DOOR.

*Case 2*: Tool recognizes CARGO DOOR as the entity and returns QIDx. We get the semantic distance between QIDx and the QID for CARGO DOOR

*Case 3*: Tool recognizes DOOR as the entity and returns QIDx. We get the semantic distance between QIDx and the QID for DOOR as in Case 2. However, since the QID for the more specific entity, CARGO DOOR, would still be valid in this case, based on the context in the sentence, we also get the semantic distance between QIDx and the QID for CARGO DOOR (and would keep getting more specific QIDs if available), and report the best score.
</td>
</row>
</table>

*Other Notes*

1. We toss out links for any phrases which are not primary, secondary, or tertiary entities for the entry. For example, in the entry "CRASH OCCURRED DURING FORCED LANDING AFTER ENGINE FAILURE DURING TAKEOFF. AIRCRAFT HAD NOT HAD ANNUAL INSPECTION.", with correct entities and QIDs listed below:

|    | Primary Entity | Primary QID | Secondary Entity | Secondary QID | Tertiary Entity | Tertiary QID |
|----|-----------|-----------|-------------------------------------------------------|-------------------|----------|----------|
| 0  | CRASH | Q238053 |  | | | |
| 1  | LANDING | Q844947 |  | |  |  |
| 2  | ENGINE FAILURE | Q46375738 | FAILURE | Q1121708 |  |  |
| 3  | TAKEOFF | Q854248  |  |  |  |  |
| 4  | AIRCRAFT | Q11436  |  |  |  |  |
| 5  | INSPECTION | Q1137655  |  |  |  |  |

If the NEL tool returns ANNUAL and its QID, or ENGINE and its QID, or any other words which are not listed, those results are ignored but not penalized.

2. In the case that an entity refers to another entity in the same entry, those entities are given the same set of primary and secondary QIDs. For example, in the sentence "BAGGAGE CART WAS BLOWN INTO PARKED AIRCRAFT BY JET BLAST. BRAKES WERE INOPERATIVE ON CART.", the set of entities and QIDs is as follows:

|    | Primary Entity | Primary QID | Secondary Entity | Secondary QID | Tertiary Entity | Tertiary QID |
|----|-----------|-----------|-------------------------------------------------------|-------------------|----------|----------|
| 0  | BAGGAGE CART | Q14277552 | CART | Q234668 | | |
| 1  | AIRCRAFT | Q11436 |  | |  |  |
| 2  | JET BLAST | Q1996324 | BLAST | Q179057 |  |  |
| 3  | BRAKES | Q1534839  |  |  |  |  |
| 4  | CART | Q14277552 | CART | Q234668 | | |

Note that CART is given the primary QID corresponding to "baggage cart", and the secondary QID corresponding to "cart." If only the QID for "cart" were listed, we would be penalizing an NEL tool which infered from context that the cart was a baggage cart.

### Correctness evaluation for RE
We need to define a process to make that comparison. We can use the following steps:
1. Extract the relations from the gold standard data.
2. Extract the relations from the tool's output.
3. Compare the relations from the tool's output against the gold standard relations.
   1. That comparisson can't be done directly because the tool's output and the gold standard data are in different formats. We need to find a way to make that comparisson.
4. Calculate the metrics such as precision, recall, and F1 score.

### Accuracy evaluation for RE

Since we do not have a gold standard for RE, we cannot report an F1 score. Instead, we report 4 metrics for RE, which we evaluate manually: syntactic accuracy, semantic accuracy, consistency, and number of hallucinations. These are described below:

*Syntactic Accuracy*\
Syntactic accuracy is the degree to which the output of the tool follows the grammatical rules in our set of guidelines. A triple is either completely syntactically accurate (1), half syntactically accurate (0.5), or syntactically inaccurate (0), depending on whether both, one of, or neither of the head and tail entities are correct, respectively. The grammatical rules are as follows:
* Head and tail entities must consist of complete phrases. "Complete phrase" signifies a word or phrase which can be treated as a noun or a verb. For example, the triple ("COWLING","part of","ENGINE IN") is inaccurate, since "engine in" is not a complete phrase.
* If a word or phrase is used as a modifier in a sentence (and is thus not its own phrase in that particular sentence), it may still be counted as a complete phrase if it can function as a noun, verb, noun phrase, or verb phrase in another context. For example, in the sentence "WING FUEL TANK SUMPS WERE NOT DRAINED DURING PREFLIGHT", ("sumps","part of","wing fuel tank") and ("fuel tank sumps", "part of", "wing") would both be syntactically accurate.
* If a head or tail entity includes words or phrases which modify a part of the sentence outside of that included in the entity, it is inaccurate. For example, in the sentence "ENGINE COWLING SEPARATED FROM ENGINE IN FLIGHT," the subject is "engine cowling", and the verb is "separated", modified by "in flight" and "from engine." Because "in flight" modifies "separated," the predicted entity "engine in flight" would be syntactically inaccurate.
* Verbs and verb phrases may only be used as entities if the relation can accept an event-type entity. Verb phrases also do not need to have a subject. For example: ("IMPROPER PREFLIGHT", "has effect", "CRASHED") is syntactically accurate.
* Complete clauses (subject-verb) may only be used as entities if the relation can accept an event-type entity.
* An head entity may be a subspan of its tail entity, and vice versa.
* Head and tail entities must be the entity type expected by the relation. For example, the relation "place of birth" must have a location as the head and a person as the tail. These expected entity types are not well-defined here, but are judged by the world-knowledge of the evaluator.
* If a relation necessitates that both the head and the tail entity be of the same type, such as "subclass of", and the head and tail entities are of different types (broadly defined types such as "event" and "object"), then it is given a syntactic accuracy score of 0.5

*Semantic Accuracy*\
Semantic accuracy is the degree to which the output of the tool adheres to the real world. A triple is either completely semantically accurate (1) or semantically inaccurate (0). We follow the guidelines below:
* The evaluator is encouraged to use their domain expertise as well as all outside knowledge available.
* If a head or tail entity is an incomplete phrase, or includes extraneous words, the triple will still be counted as semantically accurate if using subspans of those entities enables a sensible triple. For example, in the record, "ENGINE RAN ROUGH. PILOT LANDED IN FIELD," if the triple were ("engine", "used by", "pilot landed") were given, it would be counted as semantically accurate, since ("engine","used by","pilot") is accurate, and it would be syntactically 50% accurate.

*Consistency*\
Consistency is the degree to which the set of output triples for each record/document are free of contridictions. Percent consistency is calculated via the expression: (Num_Triples - Num_Inconsistencies)/(Num_Triples), where Num_Inconsistencies is the number of triples such that if they were removed from the set of output triples, the remaining set would be consistent. For example, if there are 3 triples generated for a document, and 2 of them contradict each other, there is 1 inconsistency, since if one of the contradicting triples were removed, the remaining 2 would be consistent. In this case, it would receive a consistency score of 0.6667.
* An example of contradicting triples would be ("Brookline, MA","place of birth","John F. Kennedy") and ("John F. Kennedy","has place of birth","Boston, MA")
* Most relations do not necessitate a one-to-one relation, however. In the record, "CRASHED WHEN LOAD WEDGED IN TREES. IMPROPER PREFLIGHT," if the triples ("IMPROPER PREFLIGHT", "has effect", "CRASHED") and ("CRASHED","has cause","LOAD WEDGED") were generated, this would still be consistent, since an event may have multiple causes.

*Number of Hallucinations*\
Some tools do not constrain their output such that entities must be mentions which appear in the input text. This leads to occurances of hallucinated entities, such as in the case of "ACFT DISPATCHER HARRASSMENT OF PILOT. PILOT FORGOT TO REMOVE TIEDROPE." and ("TRAIL","different from","PILOT"). Since TRAIL does not occur in the document, it is counted as a hallucination. We report the number of hallucinated entities in the output data.

**Note that the syntactic and semantic accuracy metrics are an unweighted average of the scores of all triples generated, while consistency is an average of the scores for each document which has any generated triples. Number of hallucinations is a simple count for all output.**
