# RE Input and Output Overview

### REBEL:

**Input:** Raw text from each FAA record. Records are treated separately but sentences are not explicitly divided up. ** Need to check if spacy nlp does this internally **\
May either implement REBEL using transformers or in a Huggingface pipeline, as described here: https://huggingface.co/Babelscape/rebel-large\
Current work with evaluating REBEL done on the results from the Huggingface pipeline usage (we created the script re/rebel/rebel_pipe.py to implement this, and rebel_main.py to implement the method using transformers)

**Output:** List of extracted triplets {"head":head entity, "relation": relation, "tail": tail entity} for each record put into the Huggingface nlp pipeline. rebel_pipe.py and rebel_main.py save results in a csv in data/results.

---

### UniRel:

**Input:** Raw text from each FAA record. Each record is treated independantly and run with UniRel on the NYT dataset.

**Output:** Run unirel_faa.py to get the output. The output is stored as a CSV file in the data/results directory. The output is a list of extracted triplets [(head_entity,relation,tail entity),...]
Sample Output:[[('FLIGHT', '/location/location/contains', 'BAGGAGE'), ('FLIGHT', '/location/location/contains', 'NOSE BAGGAGE')]]

---

### DeepStruct:

*** Jonathan do this ***

---

### PL-Marker:

**Input:** PL-Marker takes in jsonl data- see re/pl-marker/create_jsonl_data.ipynb, and re/pl-marker/faa_eval_faa.jsonl.\
*** Note to self: edit the create_jsonl_data.ipynb to just use spacy because I think it will do the same thing as what I did manually***\

**Output:** PL-Marker performs both NER and RE. The NER script must be run before the RE script, since RE needs to use the named entities. The NER script (run_acener.py) saves predicted entities to a file called ent_pred_test.json:
Sample output: {"sentences": [["elect", "syst", "went", "dead", ",", "generator", "circuit", "breaker", "switch", "not", "engaged", "."], ["not", "time", "to", "ext", "."], ["gear", "manually", "."]], "ner": [[], [], []], "relations": [[], [], []], "doc_key": "faa_13", "predicted_ner": [[[0, 1, "Method"], [5, 8, "OtherScientificTerm"]], [], []]}\
The RE tool saves its output to a file called pred-results.json with this output:\
Sample output: {"0": [[0, []]], "3": [[1, []]], "7": [[0, []]], "9": [[1, []]], "10": [[1, []]], "11": [[0, []]], "13": [[0, []]], "17": [[0, []]], "19": [[1, []]], "25": [[0, []]], "26": [[0, [[[5, 7], [0, 0], "USED-FOR"]]]], ... }\
This output is then parsed in re/pl-marker/pred_results_parse.ipynb, and saved in a csv in data/results/re
