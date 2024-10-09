# Gold Standard Data
The gold standard data is a subset of the [Complete Set of FAA data](../data/FAA_data/Maintenance_Text_data_nona.csv) created to evaluate the correctness of the tools regarding Named Entity Recognition (NER), Coreference Resolution (CR), and Named Entity Linking (NEL) tasks.

## Gold Standard Preparation

The Gold Standard dataset is derived from a [selected random subset of 100 records](../data/FAA_data/FAA_sample_100.csv) from the [Complete Set of Processed FAA data](../data/FAA_data/Maintenance_Text_data_nona.csv).

The gold standard datasets were hand crafted by our team, following guidelines described below. For those interested in the gold standard creation process, the raw result from our team, including notes, is available in the [raw folder](raw/), and the processed files are available in the [processed folder](processed/). The data preparation process, including the steps taken to create the Gold Standard dataset, is registered in the [process_gs.ipynb](process_gs.ipynb) notebook.

We have a gold standard for the each of following tasks:

- [Named Entity Recognition (NER)](processed/ner.csv)
- [Coreference Resolution (CR)](processed/cr.csv)
- [Named Entity Linking (NEL)](processed/nel.csv)


# Annotator Guidelines

## NER

Because no NER benchmark focuses on entity types relevant to data from the maintenance or aviation domains, we gathered a small team of annotators who labeled un-typed named entities that constituted the essential information in each record of the FAA dataset. We call this dataset the un-typed FAA GS, or [UTFAA](processed/ner.csv). This is our primary GS for evaluation, since it indicates how useful the zero-shot output of each tool is for the aviation maintenance domain.

Additionally, we label the same 100 sample records following the guidelines published for CoNLL-2003, ACE-2005, and OntoNotes. We also remove the vehicle-type entities from our ACE-2005-labeled GS (there were no weapon-type entities to remove) to create our ACE-Phase-1-labeled GS, which is used to evaluate NLTK. These benchmark-annoted GSs are denoted [CoNLLFAA](processed/ner_conll.csv), [ACE05FAA](processed/ner_ace.csv), [ACE1FAA](processed/ner_ace_nltk.csv), and [ONFAA](processed/ner_on.csv).

See the table below for a comparison between the benchmark-annotated GSs and UTFAA, obtained with [ner_overlap.ipynb](ner_overlap.ipynb). Total refers to the total number of entities generated for the set of 100 sample records by each benchmark-annotated GS. Match and Partial refer to the number of entities in each benchmark-annotated GS that match or partially match an entity in our GS, regardless of label. Overlap is the sum of the matches and partial matches divided by the total number of entities in our GS, which is 510.

|               | Total | Match | Partial | Overlap |
|---------------|-------|-------|---------|---------|
| Conll-2003    | 44    | 36    | 8       | 0.086   |
| ACE-2005      | 195   | 133   | 54      | 0.35    |
| ACE Phase 1   | 122   | 89    | 26      | 0.22    |
| OntoNotes 5.0 | 61    | 52    | 9       | 0.12    |

### Un-Typed NER GS (UTFAA)

The NER gold standard was created manually abiding by the following guidelines:

* We follow ACE-2005 to label persons, locations, organizations, geo-political entities (GPEs), facilities, weapons, and vehicles. We make a few exceptions. First, we include "ground" and "land", since they are distinct locations in aviation, where they are often used to differentiate from airspace. We also exclude articles from our entities, but keep all other modifiers. Lastly, we do not include relative clauses or relative pronouns in our GS, since they are unhelpful as a basis for NEL.

* We follow OntoNotes 5.0 to label dates, times, quanitities, and cardinals.

* Additionally, we label entities which fall into one of the following categories: vehicle system/component, operational items (fuel, oil, load, etc.), failures, causes of failures, symptoms of failures, phases of flight (takeoff, climb, landing, etc.), types of flight (ferry flight, test flight, etc.), and procedures (maintenance, safety checks, etc.). Future work could involve formalizing these categories into well-defined entity types. We follow ACE-2005 in all syntactical rules such as inclusion of modifiying phrases (with the exception of articles), nesting entities, treating appositives, etc.

* We ignore all typos and words that are cut off at the end of the record. However, we do include shorthand and acronyms (``ACFT" for aircraft, ``PROP" for propeller, etc.)

### Benchmark-Annotated NER GSs (CoNLLFAA, ACE1FAA, ACE05FAA, ONFAA)

See annotation guidelines:
* [CoNLL-2003](https://www.cnts.ua.ac.be/conll2003/ner/annotation.txt)
* [ACE-2005](https://www.ldc.upenn.edu/sites/www.ldc.upenn.edu/files/english-entities-guidelines-v5.6.6.pdf)
* [OntoNotes 5.0](https://catalog.ldc.upenn.edu/docs/LDC2013T19/OntoNotes-Release-5.0.pdf)

### Coreference Resolution

The Coreference Resolution gold standard was created manually following CoNLL-2012 coreference resolution guidelines, including the OntoNotes tagging guidelines included in their [paper](https://aclanthology.org/W12-4501.pdf) (Pradhan, 2012). A summary of the most relevant guidelines to our work is as follows:

* Noun phrases consist of a head noun and modifying articles, adjectives, or other phrases. For example, in the phrase "wing fuel tank sumps", which can be annotated as ((wing (fuel (tank))) (sumps)), "sumps" is the head noun, and "wing fuel tank" is a modifing phrase. For coreference, *the largest logical span of a noun phrase is always used,* including all modifiers and articles.

* All pronouns are linked to the nouns they refer to, except uses of “there”, “it”, and “you” that don’t refer to anything (the general “you”, “make it”, “getting up there”, etc)

* When nouns are used as modifiers, the modifying nouns cannot be used in a coreference chain. For example, if a sentence were "While inspecting taxiway, personnel noticed taxiway light broken", "taxiway" and "taxiway" are not coreferences, since the second "taxiway" is a modifier and is part of the phrase "taxiway light."

* Generic mentions, such as plurals like "lights", cannot be coreferenced which each other but can be coreferenced with a specific mention to which they refer.

* Appositive phrases, such as “a Beech 1900D, N81SK”, or "Tim, the pilot", serve to ascribe some attribute to a head noun. In this case, the "N81SK" is described as "a Beech 1900D", and "Tim" is described as "the pilot." These make up appositive corerefences, which differ from identity coreferences, the kind we usually seek. In identity corferences, "it" referes to "N81SK" and it is understood that they are identical; however "a Beech 1900D" simply adds information. This difference in the nature of the coreferences led CoNLL-2012 to exclude appositive coreferences from evaluation. We follow them in doing so.

### NEL

Our NEL gold standard is based on the named entities identified in our UTFAA gold standard. We then found Wikidata Q-identifiers (QIDs) by manually looking up each entity and listing the most specific Q-identifier if there was a correct one. All of the NEL tools we evaluate use QIDs or Wikipedia-based identifiers, such as titles or links to entries, which can be easily translated into QIDs. This enabled us to directly compare the links predicted by each NEL tool with those in the gold standard.

We also created a Flexible NEL GS, which includes additional entity-QID links, motivated by the fact that differing mention spans may change the appropriate QID for each entity. For example, in the sentence "WHILE TAXIING LOST NOSEWHEEL STEERING AND BRAKES", we have "NOSEWHEEL STEERING" as an entity in our UTFAA NER GS. If an NEL tool only recognizes "STEERING" as the entity and links it to the QID for steering correctly (Q18891017), this would be excluded from the evaluation set under strong entity-matching and counted as incorrect under weak entity-matching. Our Flexible GS makes a flexible evaluation possible, where if an exact match for "NOSEWHEEL STEERING" is not found, the evaluator moves to a secondary entity-QID link, ("STEERING", Q18891017), and evaluates the predicted entity-QID against it. To accomplish this, we included primary, secondary, and up to tertiary entity-QID pairs for entities like "NOSEWHEEL STEERING," where sub-spans of the primary entity share the same semantic role in the sentence.

The [NEL GS](processed/nel.csv) includes all linked entities, primary through tertiary, so that there is one GS file. Secondary and tertiary links are ignored in non-flexible evaluation.
