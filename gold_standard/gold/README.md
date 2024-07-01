# Gold Standard Preparation

### NER

The NER gold standard was created manually by consensus from three associates from our team, abiding by the following guidelines:
* Types of entities include:

| Entity Type | Definition | Examples |
|-------------------------------|-------------------------------|---------------------------------|
| Person | Proper name, or role referring to a specific person | "Mr. Timothy Allen Wells", "Pilot" |
| Organization | Named organization | "Northwest Airlines" |
| Place | Named place | "Iowa City, IA", "Gate B-52" |
| Date | Calendar Date | "Mar 14, 1995" |
| Time | Time of Day | "1147 AM local time" |
| Cardinal | Number that describes "how many" of something | "one", "3" |
| Ordinal | Number that describes the place something holds in an order | "1st", "second" |
| Accident/Incident Type | Encompasses wide range of events and specific issues which necessitate accident/incident reports | "lost control", "crashed", "damage" |
| Aircraft | Any phrase referring to a specific aircraft | "aircraft", "N153JC", "Bell Helicopter Model BHT-47-G5" |
| Equipment | Any part of an aircraft and any other equipment involved in accidents | "engine", "left wing" |
| Phase of Flight | Normal phase of flight | "takeoff", "descent" |
| Flight/Operation Type | Type or purpose of flight or operation. If "flight" by itself, is tagged as Flight/Operation Type, not Phase of Flight,  by default. | "ferry flight", "cargo trip" |
| Procedure | Action taken or not taken by crew relating to operation and safety of flight | "secured fuel caps", "maintenance" |
| Cause/Condition | Underlying causes or environmental conditions contributing to accident/incident | "icing", "water in fuel" |

* Entities drawn from noun phrases use the largest logical span of the noun phrase that can include modifiers which are inherent to the identitity of the core noun, and exclude modifiers and articles which are only incidental to it. For example, in the sentence, "Loose cowling on takeoff", the modifier, "loose," is excluded because it is only incidental to "cowling." However, in the sentence "Battery compartment door opened", the modifiying phrase, "battery compartment," is included because the door is inherently a battery compartment door.

* If a word or phrase which belongs to one of the above categories falls inside of the span of another named entity, it is superceded by the named entity. For example, although "fuel" may be an entity its own right elsewhere, the "fuel" in "water in fuel" is ignored, since the phrase "water in fuel" is a Cause/Condition type named entity.

### Coreference Resolution

### NEL

### RE
