# NEL Input and Output Overview

### BLINK:

**Input:** BLINK expects input in jsonl format. nel/blink/annotate_faa.py tranforms the FAA data into jsonl format and saves the indices and sentence numbers with each sentence. Each sentences is saved as a seperate line in the jsonl format because Flair, the tool which BLINK uses for NER, expects a single sentence as input. Because of this, BLINK sees each sentence separately and does not get to use the whole record as context if a record in the FAA data contains multiple sentences.\

**Output:** We created out own python script to run BLINK because we wanted to be able to keep the document number and sentence number annotation in the output. Also, since BLINK outputs Wikipedia urls instead of QIDs, we implemented a function to look up the corresponding QID for each Wikipedia article and save that. The run_blink.py script uses code from BLINK/main_dense.py with these additions. The run_blink.py script saves results to a csv in data/results/nel.\
BLINK contains a biencoder module which pulls a list of the most likely ID candidates for each entity out of a list of Wikipedia entry titles + first paragraph. It then feeds that list to a crossencoder module which reranks them. Output from just the biencoder and the biencoder + the crossencoder are available, so both are saved in the results csv.

---

### spaCy EntityLinker:

**Input:** spaCy Entity Linker allows you to pass the records in directly. Each record is treated independantly.

**Output**  Run sel_faa.py to to get the output. The output is stored as a CSV file in the data/results directory. 
The output is a list of extracted triplets [{"Identifier":QID,"label":name,"description":description},...]
Example: [{'indentifier': 8015236, 'label': 'William Matthew Prior', 'description': 'American painter'}]
 
---

### GENRE:

*** Jonathan do this ***

---

### ReFinED:

*** Jonathan do this ***
