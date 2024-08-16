# Correctness Evaluation


We evaluate the correctness of the tools in two ways: **quantitative** and **qualitative**.

## Quantitative Evaluation
The quantitative evaluation is done by comparing the tool's output with the gold standard data, regarding Named Entity Recognition (NER), Coreference Resolution (CR), and Named Entity Linking (NEL) tasks.
Evaluations.

Quantitative Evaluations may be easily recreated with the scripts available in the [quantitative evaluations folder](quantitative), and are transcribed in [quantitative/README.md](quantitative/README.md)

## Qualitative Evaluation
The qualitative evaluation is done by a domain expert who evaluates the tool's output, regarding Relation Extraction (RE) tasks. 

Qualitative evaluations are saved in the [qualitative_evaluations folder](qualitative), and are summarized in [qualitative/README.md](qualitative/README.md).

## Methodology for Comparing Tool Outputs with the Gold Standard

### Correctness evaluation for NER

We follow SemEval 

We provide two F1 metrics for NER evaluation: a strong-matching and a weak-matching. The strong-matching evaluation counts a predicted entity as correct only if it exactly matches a gold standard entity. In the weak-matching evaluation, a predicted entity is counted correct if it contains any substring of the gold standard entity, or if the gold standard entity contains any substring of the predicted entity.

We do not evaluate correctness of entity labels when evaluating against the [un-typed NER GS](../OMIn_dataset/gold_standard/processed/ner.csv).

We evaluate each NER tool against each GS: the [un-typed UTFAA](../OMIn_dataset/gold_standard/processed/ner.csv), and the benchmark-annotated [CoNLLFAA](../OMIn_dataset/gold_standard/processed/ner_conll.csv), [ACE1FAA](../OMIn_dataset/gold_standard/processed/ner_ace_nltk.csv), [ACE05FAA](../OMIn_dataset/gold_standard/processed/ner_ace.csv), and [ONFAA](../OMIn_dataset/gold_standard/processed/ner_on.csv).

For UTFAA, we evaluate just entity spans and ignore labels. We report an F1 score with strong-matching and one with weak-matching. In strong-matching, a predicted entity is correct only if it exactly matches a gold standard entity. In weak-matching, a predicted entity is counted correctly if it contains any substring of the gold standard entity, or if the gold standard entity contains any substring of the predicted entity.

In the example: ``"Narrative: The cargo door was latched before takeoff by Mr. Bowen. Runway conditions at Steven's Village was extreme"``, the entities should be ``"cargo door"``, ``"takeoff"``, ``"Mr. Bowen"``, ``"runway conditions"``, and ``"Steven's Village"``. However, flair returns ``"Bowen"`` and ``"Steven's Village"`` as the entities. Therefore, ``"Bowen"`` is marked as incorrect in the strong-matching evaluation, but correct in the weak-matching evaluation since it is a substring of ``"Mr. Bowen"``.

For the benchmark-annotated GSs, we follow SemEval (2013) in reporting four F1 metrics: Strict, Type, Exact, and Partial. In Strict and Type, an entity must be labeled with the correct type to be correct. In Strict and Exact, an entity must exactly (strong) match the gold standard entity to be correct, while in Type and Partial, an entity may be a partial (weak) match. Note that Exact and Partial are equivalent to the label-agnostic strong and weak matching used for UTFAA, respectively.

### Correctness evaluation for CR

We report 4 metrics for CR evaluation, because they each capture a different aspect of a tool's performance:
* MUC (Vilain et al., 1995)
* B-CUBED (Bagga and Baldwin, 1998)
* CEAF (Luo, 2005)
* LEA (Moosavi and Strube, 2016)
We also follow CoNLL-2012 in reporting the unweighted average of MUC, B-CUBED, and CEAF

### Correctness evaluation for NEL

We evaluate NEL tools in two ways: F1 score and Ontology-based Topological (OT) metrics.

To calculate the F1 score, we follow the equations in [Shen et. al.](https://arxiv.org/pdf/2109.12520), who follow GERBIL. We define a true positive as a predicted entity which matches both the entity and the QID in a gold standard link. A false positive is a predicted entity which matches an entity but not its QID in a gold standard link. A false negative exists when there is no matching predicted entity for a gold standard entity-QID link. Predicted entities without any QID, as well as predicted entities-QID links without a matching gold entity, are not included in the evaluation.

In addition to the F1 score, we provide Ontology-based Topological metrics that use features derived from the structure (topology) of the underlying base ontology. We use two OT metrics, Jiang Conrath (JC) metric and class similarity for examination as implemented in [KGTK Semantic Similarity](https://github.com/usc-isi-i2/kgtk-similarity).

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

For the OT metrics, we evaluate the intersection of entities in the gold and predicted sets. This intersection consists of predicted entities that have a matching entity in the gold standard, where both predicted and gold entities are linked with a QID. We then report a micro-average across all linked entities in the intersection, excluding those for which a score could not be obtained due to limitations in the KB.

For each metric, we also implement three evaluation strategies: strong-matching, weak-matching, and flexible. Strong and weak matching follow the definitions described above for NER. The type of matching affects which predicted entities are included in the evaluation set.

Flexible evaluation makes use of the secondary and tertiary links in the [NEL GS](../OMIn_dataset/gold_standard/processed/nel.csv). In Flexible evaluation, if a predicted linked entity exactly matches either the primary, secondary, or tertiary link, it is correct. Flexible evaluation utilizes strong-matching.

Example: ``"Forward cargo door opened as aircraft took off. Objects dropped out. Returned. Failed to see warning light."``

The primary, secondary, and tertiary entities are laid out below.  In strong and weak-matching evaluation, only ("aircraft",Q11436) would be included in the gold standard. In flexible evaluation, ("door", Q36794), ("aircraft",Q11436), and ("light", Q1146001) would be included.

|    | Primary Entity | Primary QID | Secondary Entity | Secondary QID | Tertiary Entity | Tertiary QID |
|----|-----------|-----------|-------------------------------------------------------|-------------------|----------|----------|
| 0  | forward cargo door | | cargo door | | door| Q36794|
| 1  | aircraft | Q11436 |  | |  |  |
| 2  | warning light | | light | Q1146001 |  |  |

Secondary entities are also linked to primary QIDs when available, and so too with tertiary entities to secondary and primary QIDs. This is done so that if a tool links a more "general" mention to the QID for the fitting, context-specific Wikidata entity, rather than the general QID, it is not penalized. For example, the GS for a document in the FAA data includes the primary link ("forced landing", Q1975745) and the secondary link ("landing", Q844947). If a tool predicted ("landing",Q1975745), that would be counted as correct, since it inferred from context that it was a forced landing and linked it to the corresponding QID.

## Methodology for RE Qualitative Evalution

Since we do not have a gold standard for RE, we cannot report an F1 score. Instead, we report 3 metrics for RE, which we evaluate qualitatively: syntactic accuracy, semantic accuracy, and consistency. We also report the number of hallucinations found in the set of sampled evaluation data. Lastly, we report the total number of triples generated, and the percent of documents with any triples generated, for the entire FAA dataset. These are described below:

*Syntactic Accuracy*\
Syntactic accuracy is the degree to which the output of the tool follows the grammatical rules in our set of guidelines. A triple is either completely syntactically accurate (1.0), half syntactically accurate (0.5), or syntactically inaccurate (0.0), depending on whether both, one of, or neither of the head and tail entities are correct, respectively. The grammatical rules are as follows:
* Head and tail entities must consist of complete phrases. "Complete phrase" signifies a word or phrase which can be treated as a noun or a verb. For example, the triple ("COWLING","part of","ENGINE IN") is inaccurate, since "engine in" is not a complete phrase.
* If a word or phrase is used as a modifier in a sentence (and is thus not its own phrase in that particular sentence), it may still be counted as a complete phrase if it can function as a noun, verb, noun phrase, or verb phrase in another context. For example, in the sentence "WING FUEL TANK SUMPS WERE NOT DRAINED DURING PREFLIGHT", ("sumps","part of","wing fuel tank") and ("fuel tank sumps", "part of", "wing") would both be syntactically accurate.
* **Exception** to the above two rules: personal pronouns may be entities, and should be intepretted the same as the person they refer to.
* If a head or tail entity includes words or phrases which modify a part of the sentence outside of that included in the entity, it is inaccurate. For example, in the sentence "ENGINE COWLING SEPARATED FROM ENGINE IN FLIGHT," the subject is "engine cowling", and the verb is "separated", modified by "in flight" and "from engine." Because "in flight" modifies "separated," the predicted entity "engine in flight" would be syntactically inaccurate.
* Verbs and verb phrases may only be used as entities if the relation can accept an event-type entity. Verb phrases also do not need to have a subject. For example: ("IMPROPER PREFLIGHT", "has effect", "CRASHED") is syntactically accurate.
* Complete clauses (subject-verb) may only be used as entities if the relation can accept an event-type entity.
* An head entity may be a subspan of its tail entity, and vice versa.
* Head and tail entities must be the entity type expected by the relation. For example, the relation "place of birth" must have a location as the head and a person as the tail. These expected entity types are not well-defined here, but are judged by the world-knowledge of the evaluator.
* If a relation necessitates that both the head and the tail entity be of the same type, such as "subclass of", and the head and tail entities are of different types (broadly defined types such as "event" and "object"), then it is given a syntactic accuracy score of 0.5

*Semantic Accuracy*\
Semantic accuracy is the degree to which the output of the tool adheres to the real world. A triple is either completely semantically accurate (1.0) or semantically inaccurate (0.0). We follow the guidelines below:
* The evaluator is encouraged to use their domain expertise as well as all outside knowledge available.
* If a head or tail entity is an incomplete phrase, or includes extraneous words, the triple will still be counted as semantically accurate if using subspans of those entities enables a sensible triple. For example, in the record, "ENGINE RAN ROUGH. PILOT LANDED IN FIELD," if the triple were ("engine", "used by", "pilot landed") were given, it would be counted as semantically accurate, since ("engine","used by","pilot") is accurate, and it would be syntactically 50% accurate.

*Consistency*\
Consistency is the degree to which the set of output triples for each record/document are free of contridictions. Percent consistency is calculated via the expression: (Num_Triples - Num_Inconsistencies)/(Num_Triples), where Num_Inconsistencies is the number of triples such that if they were removed from the set of output triples, the remaining set would be consistent. For example, if there are 3 triples generated for a document, and 2 of them contradict each other, there is 1 inconsistency, since if one of the contradicting triples were removed, the remaining 2 would be consistent. In this case, it would receive a consistency score of 0.6667.
* An example of contradicting triples would be ("Brookline, MA","place of birth","John F. Kennedy") and ("John F. Kennedy","has place of birth","Boston, MA")
* Most relations do not necessitate a one-to-one relation, however. In the record, "CRASHED WHEN LOAD WEDGED IN TREES. IMPROPER PREFLIGHT," if the triples ("IMPROPER PREFLIGHT", "has effect", "CRASHED") and ("CRASHED","has cause","LOAD WEDGED") were generated, this would still be consistent, since an event may have multiple causes.

**Note that for syntactic accuracy, semantic accuracy, and consistency, the proper number of significant figures to report would be 1. However, this does not give us much information, so we report up to 3**

*Number of Hallucinations*\
Some tools do not constrain their output such that entities must be mentions which appear in the input text. This leads to occurances of hallucinated entities, such as in the case of "ACFT DISPATCHER HARRASSMENT OF PILOT. PILOT FORGOT TO REMOVE TIEDROPE." and ("TRAIL","different from","PILOT"). Since TRAIL does not occur in the document, it is counted as a hallucination. We report the number of hallucinated entities in the output data.

**Note that the syntactic and semantic accuracy metrics are an unweighted average of the scores of all triples generated, while consistency is an average of the scores for each document which has any generated triples. Number of hallucinations is a simple count for all output.**

*Triples Counts*\
Lastly, we report two figures based on the output for the entire FAA dataset: the total number of triples found, as well as the percent of documents/records which have some predicted triples. This is done in the second sheet in each evaluation excel sheet.

## The Relations Sets:
| Training Set | Tools | Relations |
|--------------|-------|-----------|
| NYT | UniRel, DeepStruct | ['/business/company/advisors','/business/company/founders','/business/company/industry','/business/company/major_shareholders','/business/company/place_founded','business/company_shareholder/major_shareholder_of','/business/person/company','/location/administrative_division/country','/location/country/administrative_divisions','location/country/capital','/location/location/contains',   '/location/neighborhood/neighborhood_of','/people/deceased_person/place_of_death','/people/ethnicity/geographic_distribution','/people/ethnicity/people','/people/person/children','/people/person/ethnicity','/people/person/nationality','/people/person/place_lived','/people/person/place_of_birth','/people/person/profession','/people/person/religion','/sports/sports_team/location','/sports/sports_team_location/teams'] |
| ACE05 | PL-Marker, DeepStruct | ['PER-SOC', 'ART', 'ORG-AFF', 'GEN-AFF', 'PHYS', 'PART-WHOLE'] |
| SciERC | PL-Marker | ['PART-OF', 'USED-FOR', 'FEATURE-OF', 'CONJUNCTION', 'HYPONYM-OF', 'COMPARE'] |
| (wikidata) | REBEL | ['has part', 'part of', 'different from', 'subclass of', 'instance of', 'has effect', 'has cause', 'located in the administrative territorial entity', 'product or material produced', 'facet of', 'manufacturer', 'point in time', 'connects with', 'uses', 'used by', 'operator', 'location', 'follows', 'followed by', 'opposite of', 'item operated', 'contains administrative territorial entity', 'country', 'shares border with', 'use']* |

\* Relations shown in order of most commonly appearing in output on FAA data. These are the top 25. See all relations for REBEL at https://raw.githubusercontent.com/Babelscape/rebel/main/data/relations_count.tsv

**Syntax Constraints for Each Relation**

For all NYT relations, the head must correspond to the descriptor in the middle of the slashes, e.g., for the relation '/business/company/advisors', the head entity must be a company. Similarly, the tail must correspond to the rightmost descriptor, e.g., in this example, it must be a group of people.

For all REBEL relations (Wikidata properties), the head and tail entities must match usage in Wikidata. This is judged by the evaluator. Some notable properties are:
* 'different from' is only used when head and tail entities share a similar name. The 'different from' relation is used to distinguish entities named the same way or similarly enough that they need to be distinguished.
* 'has effect' and 'has cause' may have noun phrases or verb phrases on either end
* 'has part', 'part of', 'subclass of','instance of', and 'facet of' all imply that the head and tail entities must correspond in entity type. We say correspond in a loose sense here, referring mainly to differences between an event, a physical object, and time, quantity, or date, and an abstract concept.

The remaining relations' syntactic constraints are described here:

**ACE-2005:**
| Relation | Head | Tail |
|----------|------|------|
| PER-SOC  | Person(s) | Person(s) |
| ART      | Person | Physical Object |
| ORG-AFF  | Person | Organization |
| GEN-AFF  | Any    | Any |
| PHYS     | Anything with a physical form | Anything with a physical form |
| PART-WHOLE | Type must correspond to Tail (see REBEL 'part of') | vice versa |

**SciERC:**
| Relation     | Head | Tail |
|--------------|------|------|
| PART-OF      | Type must correspond to Tail (see REBEL 'part of') | vice versa |
| USED-FOR     | Any | Any |
| FEATURE-OF   | Type must correspond to Tail (see REBEL 'part of') | vice versa |
| CONJUNCTION  | Type must correspond to Tail (see REBEL 'part of') | vice versa |
| HYPONYM-OF   | Type must correspond to Tail (see REBEL 'part of') | vice versa |
| COMPARE      | Type must correspond to Tail (see REBEL 'part of') | vice versa |
