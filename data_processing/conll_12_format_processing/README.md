# Processing json files to CoNLL-12 format

Here, we annotate and transform the FAA to follow the CoNLL-2012 convention, which we refer to as the CoNLL-12 format.

**The CoNLL-2012 Dataset**
To see a sample of CoNLL-12 data, download their trial data at https://conll.cemantix.org/2012/data.html. Or, follow instructions there and at https://catalog.ldc.upenn.edu/LDC2013T19 to obtain the full dataset.

The CoNLL-12 Shared Task describes their column structure in the table below, available at https://conll.cemantix.org/2012/data.html

| Col # | Col Name | Description|
|-------|----------|------------|
| 1 | Document ID | This is a variation on the document filename|
| 2 | Part number | Some files are divided into multiple parts numbered as 000, 001, 002, ... etc.|
| 3 | Word number |  |
| 4 | Word itself | This is the token as segmented/tokenized in the Treebank. Initially the *_skel file contain the placeholder [WORD] which gets replaced by the actual token from the Treebank which is part of the OntoNotes release. |
| 5 |Part-of-Speech |  |
| 6 | Parse bit | This is the bracketed structure broken before the first open parenthesis in the parse, and the word/part-of-speech leaf replaced with a *. The full parse can be created by substituting the asterix with the "([pos] [word])" string (or leaf) and concatenating the items in the rows of that column.|
| 7 | Predicate lemma | The predicate lemma is mentioned for the rows for which we have semantic role information. All other rows are marked with a "-"|
| 8 | Predicate Frameset ID | This is the PropBank frameset ID of the predicate in Column 7.|
| 9 | Word sense | This is the word sense of the word in Column 3.|
| 10 | Speaker/Author | This is the speaker or author name where available. Mostly in Broadcast Conversation and Web Log data.|
| 11 | Named Entities | These columns identifies the spans representing various named entities.|
| 12:N | Predicate Arguments | There is one column each of predicate argument structure information for the predicate mentioned in Column 7.|
| N | Coreference| Coreference chain information encoded in a parenthesis structure. |

**Our Methodology**
First, we note that the FAA data contains many cases where sentences are seperated by periods, without as space after them, such that it appears: "SENTENCE ONE.SENTENCE TWO." This caused many errors when we attempted to feed the data directly to our format_conll.py, so we instead created an additional preprocessing script, create_faa_json.py, which adds spaces after sentences and lowercases the data, saving it in faa.json.

Then, we use format_conll.py to transform faa.json to faa.conll.

Our goal for faa.conll was specifically to input it to s2e-coref and ASP. Therefore, we found through experiment that both these tools ignore columns 7-9, and 12:N, so we simply add a '-' in those columns.

For the remaining columns, we use:
* All FAA incident entries (rows in the csv) are treated as a one-part document
* Words and sentences are tokenized with NLTK
* POS-tagging is done with NLTK
* The parse bit is derived from a parse tree. We follow the developers of CoNLL-2012 in using a Charniak parser, specifically the RerankingParser from BLLIP.
* The speaker is always "speaker1"
* The CoNLL-2012 developers used the Identifinder<sup>TM</sup> tool from BBN for NER; however, we used spaCy since it was much easier to implement and more up-to-date
* The coreference column we leave empty (as hyphens) since we are only interested in what coreferences the tested tools can generate without outside influence.


**File-by-file explanation:**

format_conll.py: script which takes json data as input, puts the data into conll-12 format, and saves an output file called formatted.conll\
*Ex:* python format_conll.py faa.json .

*Experiment using obtained conll-2012 data:*\
*We input OntoNotes data to format_conll.py to test how well it can recreate what appeared in CoNLL-2012*\
msnbc_0004.conll: data from the trial release of conll-12, also located in data/conll-2012/trial/data/english/annotations/bc/msnbc/msnbc_0004.conll\
create_conll_raw.py: transforms msnbc_0004.conll to conll_raw.json, which takes out the formatting, parsing, and labeling elements of conll-12 data and stores the original, natural text in a json format\
conll_raw.json: original msnbc data formatted as a json file by create_conll_raw.py\
msnbc_formatted.conll: output of format_conll.py when run on conll_raw.json\
check_format_conll_acc.ipynb: notebook which compares the original msnbc_0004.conll data with the data created by format_conll.py to test accuracy of script

*FAA data formatting*
create_faa_json.py: transforms the faa data to a json file in the format expected by format_conll.py\
faa.json: output of create_faa_json.py\
faa.conll: output of format_conll.py when run on faa.json

faa.json and faa.conll also copied and saved in data/FAA_data
