# RE Input and Output Overview

### REBEL:

**Input:** Raw text from each FAA record. Records are treated separately.
May either implement REBEL by loading the model with transformers from_pretrained(), in a Huggingface pipeline, or in a spacy pipeline, as described here: https://huggingface.co/Babelscape/rebel-large\
Current work with evaluating REBEL done on the results from the Huggingface pipeline usage (we created the script re/rebel/rebel_pipe.py to implement this, and rebel_main.py to implement the method using transformers)

**Output:** List of extracted triplets {"head":head entity, "relation": relation, "tail": tail entity} for each record put into the Huggingface nlp pipeline. rebel_pipe.py and rebel_main.py save results in a csv in tool_results.

---

### UniRel:

**Input:** Raw text from each FAA record. Each record is treated independantly and run with UniRel on the NYT dataset.

**Output:** Run unirel_faa.py to get the output. The output is stored as a CSV file in the tool_results directory. The output is a list of extracted triplets [(head_entity,relation,tail entity),...]
Sample Output:[[('FLIGHT', '/location/location/contains', 'BAGGAGE'), ('FLIGHT', '/location/location/contains', 'NOSE BAGGAGE')]]

---

### DeepStruct:

Regarding DeepStruct, while it offers a single pretrained model, preparing it for inference on unseen datasets requires some additional steps. 
First, the unsee dataset’s schema must be aligned with the one DeepStruct was trained on to ensure compatibility with the model’s recognized entity and relation types. 
Additionally, configuration files might need adjustments to properly format the input data. 
Considering the relation extraction task, DeepStruct schemas are based on datasets like NYT, CoNLL-04, ADE, and ACE-2005. 
We chose the NYT schema for our evaluation, which produced the highest RE F1 score of 84.6. This also ensures consistency and fairness when comparing DeepStruct with UniRel.

To run DeepStruct inference on our data, we utilized the `./data_scripts/nyt.sh` and `./tasks/mt/nyt_rel.sh` bash scripts provided by the DeepStruct authors, which is designed for processing NYT data and perform the RE task. These scripts generate a folder with files formatted according to DeepStruct’s expectations.

For our dataset, we configured the generated NYT folder by retaining all the files related to the dev set, [schemas.json](https://github.com/nd-crane/trusted_ke/blob/main/re/deepstruct/schemas.json) and tokenizers like `cached_nyt_re_test_T5TokenizerFast_512_512.pth`. However, we modified the [test.json](https://github.com/nd-crane/trusted_ke/blob/main/re/deepstruct/test.json) and [test.source](https://github.com/nd-crane/trusted_ke/blob/main/re/deepstruct/test.source) files, using the [prep_data.py script](https://github.com/nd-crane/trusted_ke/blob/main/re/deepstruct/prep_data.py). To avoid errors during execution, we also included an empty `test.target` file.

**Input:** 
Files: [test.json](https://github.com/nd-crane/trusted_ke/blob/main/re/deepstruct/test.json) and [test.source](https://github.com/nd-crane/trusted_ke/blob/main/re/deepstruct/test.source) 

**Output:** 
- Sample output: ( BARTLESVILLE ; contains ; BARTLESVILLE MUNICIPAL AIRPORT )
- Files:
  - 100 records on GS [test_nyt_100k.jsonl.hyps](https://github.com/nd-crane/trusted_ke/blob/main/re/deepstruct/test_nyt_100.jsonl.hyps)
  - Complete set [test_nyt_2k.jsonl.hyps](https://github.com/nd-crane/trusted_ke/blob/main/re/deepstruct/test_nyt_2k.jsonl.hyps) 


---

### PL-Marker:

**Input:** PL-Marker takes in jsonl data- see re/pl-marker/create_jsonl_data.ipynb, and re/pl-marker/faa_eval_faa.jsonl.\
*** Note to self: edit the create_jsonl_data.ipynb to just use spacy because I think it will do the same thing as what I did qualitatively***\

**Output:** PL-Marker performs both NER and RE. The NER script must be run before the RE script, since RE needs to use the named entities. The NER script (run_acener.py) saves predicted entities to a file called ent_pred_test.json:
Sample output: {"sentences": [["elect", "syst", "went", "dead", ",", "generator", "circuit", "breaker", "switch", "not", "engaged", "."], ["not", "time", "to", "ext", "."], ["gear", "manually", "."]], "ner": [[], [], []], "relations": [[], [], []], "doc_key": "faa_13", "predicted_ner": [[[0, 1, "Method"], [5, 8, "OtherScientificTerm"]], [], []]}\
The RE tool saves its output to a file called pred-results.json with this output:\
Sample output: {"0": [[0, []]], "3": [[1, []]], "7": [[0, []]], "9": [[1, []]], "10": [[1, []]], "11": [[0, []]], "13": [[0, []]], "17": [[0, []]], "19": [[1, []]], "25": [[0, []]], "26": [[0, [[[5, 7], [0, 0], "USED-FOR"]]]], ... }\
This output is then parsed in re/pl-marker/pred_results_parse.ipynb, and saved in a csv in tool_results
