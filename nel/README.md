# NEL Input and Output Overview

### BLINK:

**Input:** BLINK expects input in jsonl format. nel/blink/annotate_faa.py transforms the FAA data into jsonl format and saves the indices and sentence numbers with each sentence. Each sentences is saved as a separate line in the jsonl format because Flair, the tool which BLINK uses for NER, expects a single sentence as input. Because of this, BLINK sees each sentence separately and does not get to use the whole record as context if a record in the FAA data contains multiple sentences.

**Output:** We created our own Python script to run BLINK because we wanted to be able to keep the document number and sentence number annotation in the output. Also, since BLINK outputs Wikipedia URLs instead of QIDs, we implemented a function to look up the corresponding QID for each Wikipedia article and save that. The run_blink.py script uses code from BLINK/main_dense.py with these additions. The run_blink.py script saves results to a CSV in tool_results/blink.\
BLINK contains a biencoder module that pulls a list of the most likely ID candidates for each entity out of a list of Wikipedia entry titles + first paragraph. It then feeds that list to a crossencoder module which reranks them. Output from just the bi-encoder and the bi-encoder + the cross-encoder are available, so both are saved in the results CSV.

---

### spaCy EntityLinker:

**Input:** spaCy Entity Linker allows you to pass the records in directly. Each record is treated independently.

**Output**  Run sel_faa.py to to get the output. The output is stored as a CSV file in the tool_results directory. 
The output is a list of linked entities for each document [{"Identifier":QID,"label":name,"description":description},...], which is then parsed and exploded so that each entity and link is on its own row of the csv.
Example: [{'indentifier': 8015236, 'label': 'William Matthew Prior', 'description': 'American painter'}]
 
---

### GENRE:

**Input:** With GENRE you can pass each of the strings as a list into the model. Each record is treated independently.

Example Input: ["In 1921, Einstein received a Nobel Prize."]

**Output:**  Run genre_faa.py to get the output. The output is stored as a CSV file in the tool_results directory. 
The model outputs a list of possible outputs and scores them using their mechanism. We return the best score. Note that the script takes substantially longer to run than the other tools since part of the model re-runs for every sentence being passed in.

Example Output: [[{'text': 'In 1921, { Einstein } [ Albert Einstein ] received a { Nobel Prize } [ Nobel Prize in Physiology or Medicine ].', 'score': tensor(-0.9068)}, {'text': 'In 1921, { Einstein } [ Albert Einstein ] received a { Nobel Prize } [ Nobel Prize in Physiology or Medicine ] {. } [ Nobel Prize in Physiology or Medicine ]', 'score': tensor(-0.9301)}, {'text': 'In 1921, { Einstein } [ Albert Einstein ] received a { Nobel Prize } [ Nobel Prize in Physiology or Medicine ] {. } [ Albert Einstein ]', 'score': tensor(-0.9942)}, {'text': 'In 1921, { Einstein } [ Albert Einstein ] received a { Nobel Prize } [ Nobel Prize in Physiology or Physiology ].', 'score': tensor(-1.0778)}, {'text': 'In 1921, { Einstein } [ Albert Einstein ] received a { Nobel Prize } [ Nobel Prize in Physiology or Medicine ] {. } [ Ernest Einstein ]', 'score': tensor(-1.1164)}]]

---

### ReFinED:

**Input:** With ReFinED you can pass each of the strings as a list into refined.process_text(). Each record is treated independently.

Example Input: refined.process_text("England won the FIFA World Cup in 1966.")

**Output:**  Run refined_faa.py to get the output. The output is stored as a CSV file. 

Example Output: [['England', Entity(wikidata_entity_id=Q47762, wikipedia_entity_title=England national football team), 'ORG'], ['FIFA World Cup', Entity(wikidata_entity_id=Q19317, wikipedia_entity_title=FIFA World Cup), 'EVENT'], ['1966', Entity(...), 'DATE']]
