import pandas as pd
import re

### CONLL-12 Format

#CONLL-12 format is like so:

#1. Document ID: This is a variation on the document filename
#2. Part number: Some files are divided into multiple parts numbered as 000, 001, 002, ... etc.
#3. Word number
#4. Word itself: This is the token as segmented/tokenized in the Treebank. Initially the *_skel file contain the placeholder [WORD] which gets replaced by the actual token from the Treebank which is part of the OntoNotes release.
#5. Part-of-Speech
#6. Parse bit: This is the bracketed structure broken before the first open parenthesis in the parse, and the word/part-of-speech leaf replaced with a *. The full parse can be created by substituting the asterix with the "([pos] [word])" string (or leaf) and concatenating the items in the rows of that column.
#7. Predicate lemma: The predicate lemma is mentioned for the rows for which we have semantic role information. All other rows are marked with a "-"
#8. Predicate Frameset ID: This is the PropBank frameset ID of the predicate in Column 7.
#9. Word sense: This is the word sense of the word in Column 3.
#10. Speaker/Author: This is the speaker or author name where available. Mostly in Broadcast Conversation and Web Log data.
#11. Named Entities: These columns identifies the spans representing various named entities.
#12 - N Predicate Arguments: There is one column each of predicate argument structure information for the predicate mentioned in Column 7.
#N. Coreference:oreference chain information encoded in a parenthesis structure.

##### However, ASP does not actually use columns 4-n, so we can simply create placeholders.

text = list(pd.read_csv("../../data/FAA_data/Maintenance_Text_data_nona.csv")["c119"])

def tokenize(sentence):
    # Define the special characters to be treated as separate tokens
    special_characters = [".", ",", '"', "(", ")", "[", "]", "{", "}"] # minus apostrophe, which has to be handled separately

    # Split the sentence using whitespace characters
    words = re.split(r'\s+', sentence)

    # Initialize an empty list to store the final tokens
    tokens = []

    # Iterate through each word and further split based on special characters
    for word in words:
        word = word.lower()

        # Split the word based on special characters
        split_word = re.split(f'([{re.escape("".join(special_characters))}])', word)

        # Check for apostrophe:
        for wd in split_word:
            # Check if the word contains an apostrophe followed by an 's'
            if "'s" in wd:
                # Split the word into two tokens: the word without "'s" and "'s"
                tokens.extend(re.split(r"('s)", wd))
            elif "n't" in wd:
                tokens.extend(re.split(r"(n't)", wd))
            elif "'ll" in wd:
                tokens.extend(re.split(r"('ll)", wd))
            elif "'re" in wd:
                tokens.extend(re.split(r"('re)", wd))
            elif "'m" in wd:
                tokens.extend(re.split(r"('m)", wd))
            elif "'d" in wd:
                tokens.extend(re.split(r"('d)", wd))
            elif "'ve" in wd:
                tokens.extend(re.split(r"('ve)", wd))
            elif "'" in wd:
                tokens.extend(re.split(r"'", wd))
            else:
                tokens.append(wd)

    # Filter out empty strings from the tokens list
    tokens = list(filter(None, tokens))

    return tokens

# Tokenize text
split_text = []
for entry in text:
    if '.' in entry:
        sentences = []
        for sentence in entry.split('.'):
            if not sentence.isspace() and len(sentence) > 0:
                tokens = tokenize(sentence + '.')
                sentences.append(tokens)
        split_text.append(sentences)
    else:
        tokens = tokenize(entry)
        split_text.append([tokens])

# Reformat it
formatted = ''

for idoc, doc in enumerate(split_text):
    doc_id = f"faa_{idoc}"
    formatted = formatted + f"#begin document ({doc_id}); part 000\n"
    for sent in doc:
        for iword, word in enumerate(sent):
            if word == '.':
                word = r'\.'
            formatted = formatted + "{:10} {:>5} {:>5} {:>20}\t-\t-\t-\t-\t-\t-\t-\t-\n".format(doc_id, 0, iword, word)
        formatted = formatted + '\n'
    formatted = formatted + "#end document\n"

# Save
with open("./ASP/data/faa_conll/dev.english.v4_gold_conll", "w") as f:
    f.write(formatted)
with open("./ASP/data/faa_conll/test.english.v4_gold_conll", "w") as f:
    f.write(formatted)
with open("./ASP/data/faa_conll/train.english.v4_gold_conll", "w") as f:
    f.write(formatted)