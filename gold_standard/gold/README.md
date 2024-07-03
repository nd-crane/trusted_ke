# Gold Standard Preparation

### NER

The NER gold standard was created manually abiding by the following guidelines:

* Noun phrases consist of a head noun and modifying articles, adjectives, or other phrases. Entities drawn from noun phrases use the largest logical span of the noun phrase that can include modifiers which are inherent to the identitity of the head noun, and exclude modifiers and articles which are only incidental to it. For example, in the sentence, "Loose cowling on takeoff", the modifier, "loose," is excluded because it is only incidental to "cowling." However, in the sentence "Battery compartment door opened", the modifiying phrase, "battery compartment," is included because the door is inherently a battery compartment door.

* When nouns are used as modifiers as part of a named entity, they cannot also be their own named entities. For example, the "fuel" in "Pilot found water in fuel" is ignored, since it falls inside of the span of the Cause/Condition type named entity, "water in fuel".

### Coreference Resolution

The Coreference Resolution gold standard was created manually following CoNLL-2012 coreference resolution guidelines, including the OntoNotes tagging guidelines included in their [paper](https://aclanthology.org/W12-4501.pdf) (Pradhan, 2012). A summary of the most relevant guidelines to our work is as follows:

* Noun phrases consist of a head noun and modifying articles, adjectives, or other phrases. For example, in the phrase "wing fuel tank sumps", which can be annotated as ((wing (fuel (tank))) (sumps)), "sumps" is the head noun, and "wing fuel tank" is a modifing phrase. For coreference, *the largest logical span of a noun phrase is always used,* including all modifiers and articles.

* All pronouns are linked to the nouns they refer to, except uses of “there”, “it”, and “you” that don’t refer to anything (the general “you”, “make it”, “getting up there”, etc)

* When nouns are used as modifiers, the modifying nouns cannot be used in a coreference chain. For example, if a sentence were "While inspecting taxiway, personnel noticed taxiway light broken", "taxiway" and "taxiway" are not coreferences, since the second "taxiway" is a modifier and is part of the phrase "taxiway light."

* Generic mentions, such as plurals like "lights", cannot be coreferenced which each other but can be coreferenced with a specific mention to which they refer.

* Appositive phrases, such as “a Beech 1900D, N81SK”, or "Tim, the pilot", serve to ascribe some attribute to a head noun. In this case, the "N81SK" is described as "a Beech 1900D", and "Tim" is described as "the pilot." These make up appositive corerefences, which differ from identity coreferences, the kind we usually seek. In identity corferences, "it" referes to "N81SK" and it is understood that they are identical; however "a Beech 1900D" simply adds information. This difference in the nature of the coreferences led CoNLL-2012 to exclude appositive coreferences from evaluation. We follow them in doing so.

### NEL

The NEL gold standard was based on our NER gold standard entities. We then found Wikidata Q-identifiers by manual lookup of each entity and listed the most specific and correct Q-identifier if there was one. 

We note that many NER methods may create different output than our gold standard entities, and we do not want to penalize NEL tools for NER discrepancies. For example, in the sentence "While taxiing lost nosewheel steering and brakes",  we have "nosewheel steering" as an entity in our NER gold standard. In case an NEL tool only recognizes "steering" as the entity and links it to the QID for steering correctly (Q18891017), we perform a separate NER evaluation, and count the link between steering and Q18891017 as correct.

To accomplish this, in our NEL gold standard, we included primary, secondary, and up to tertiary entity-QID pairs for entities like "nosewheel steering," where subspans of the primary entity perform the same function in the sentence as the primary entity.

### RE
