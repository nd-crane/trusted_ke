# Coreference Resolution Input and Output Overview

### ASP:

**Input:** CoNLL-12 formatted data. See our process for transforming and annotating the FAA data to follow CoNLL-12 format [here](../OMIn_dataset/data_processing/conll_12_format_processing), and the final faa.conll file [here](../OMIn_dataset/data/FAA_data/faa.conll)\
The CoNLL-12 formatted data is then processed into jsonlines by a script provided in the ASP remote repo, ASP/data/t5minimize_coref.py. The result of this script is available at [asp/minimized_data](asp/minimized_data).

Sample of minimized jsonl data: \
['▁core', 'ference', '▁resolution', ':', '<speaker>', '▁', '-', '</speaker>', '▁to', 'w', '▁plane', '▁became', '▁air', 'borne', '▁then', '▁settled', '▁', '\\', '.', '▁student', '▁thought', '▁to', 'w', '▁in', '▁trouble', '▁', '&', '▁released', '▁', '\\', '.', '▁hit', '▁tree', '▁', '\\', '.', '</s>']\
Each record in the FAA data, which is treated as its own doc in the CoNLL-12 format, is seen separate from the other records. The '\\' character denotes a break between sentences.\

**Output:** evaluate_coref.py prints log statements, which are saved in coref/asp/faa_nohup.out. These logs include 3 print statements for each entry, coref/asp/analyze_output.ipynb scans the output for predicted coreferences. Since currently ASP is finding no coreferences, there is no code to save them in tool_results\

---

### coref_mt5:

**Input:** Raw text from FAA data. coref_mt5 takes in a list of titles and a list of inputs, where the titles correspond to each input.\
The input may contain multiple sentences, which should be seperated by newline characters.

coref_mt5 sees each record separately and may create coreferences across multiple sentences in record.

**Output:** outputs predicted clusters by word index (start index of reference, end index of reference) like so:\
predicted clusters with word indexes [[(0, 8), (26, 26), (40, 41), (58, 58), (90, 90), (93, 93), (114, 116), (136, 136), (140, 140)], [(24, 24), (82, 84), (102, 102)], [(111, 112), (127, 128)], [(22, 24), (160, 160)]]\
Also outputs coreference-resolved sentence like so:\
[1 The Eiffel Tower ( French : tour Eiffel ) ] is a wrought - iron lattice tower on the Champ de Mars in [4 Paris , [2 France ]] . [1 It ] is named after the engineer Gustave Eiffel , whose company designed and built [1 the tower ] . Locally nicknamed " La dame de fer " ( French for " Iron Lady "), [1 it ] was constructed from 1887 to 1889 as the centerpiece of the 1889 World ' s Fair . Although initially criticised by some of [2 France ' s ] leading artists and intellectuals for [1 its ] design , [1 it ] has since become a global cultural icon of [2 France ] and one of the most recognisable structures in [3 the world ] . [1 The Eiffel Tower ] is the most visited monument with an entrance fee in [3 the world ] : 6 . 91 million people ascended [1 it ] in 2015 . [1 It ] was designated a monument historique in 1964 , and was named part of a UNESCO World Heritage Site (" [4 Paris ] , Banks of the Seine ") in 1991 .\
Note that the number attached to each coreference in the resolved sentence corresponds to the index in the list of word indexes above (minus one).\

---

### s2e-coref:

**Input:** CoNLL-12 formatted data. See our process for transforming and annotating the FAA data to follow CoNLL-12 format [here](../OMIn_dataset/data/conll_12_format_processing), and the final faa.conll file [here](../OMIn_dataset/data/FAA_data/faa.conll)\
Like ASP, s2e-coref also has a minimize.py script which transforms the CoNLL-12 formatted data to jsonlines. See [s2e-coref/data](s2e-coref/data) for both formats of data. 

s2e-coref sees each record separately and may create coreferences across multiple sentences in a record.

**Output:** A jsonl document with 2 dictionaries:
- A list of predictions for each doc: ({"faa/401_19800721061969I_0": [], "faa/2498_20030328006589I_0": [], "faa/295_19790808027309A_0": [], "faa/2575_20041108029389I_0": [[[16, 17], [25, 25]]], ...)
- A list of subtoken_maps for each doc: {"faa/401_19800721061969I_0": [0, 0, 0, 0, 0, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14], "faa/2498_20030328006589I_0": [0, 0, 0, 0, 0, 0, 1, 1, 2, 3, 4, 5, 5, 6, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 21, 22, 23], ...\
The subtoken maps can be used to map the numbers in the lists of predictions to the corresponding spans in the sentence. See s2e-coref/interpret_predictions.ipynb for how.

---

### neuralcoref:

**Input:** A document, as a string

**Output:** Coreferences in the form: [NOSE GEAR: [NOSE GEAR, NOSE GEAR], ...]
