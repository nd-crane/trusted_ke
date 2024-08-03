import pandas as pd
import re
import nltk
nltk.download('averaged_perceptron_tagger')
from bllipparser import RerankingParser
import spacy

rrp = RerankingParser.fetch_and_load('WSJ-PTB3', verbose=True)

nlp = spacy.load("en_core_web_sm") # Must run "python -m spacy download en" prior
ner = nlp.get_pipe("ner")

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

# s2e uses the following: doc_key (1), word (3), parse bit (6), speaker (10), ner (11), and coref (N)
# Speaker can be '-' if no speaker info
# Coref can == '-' to get skipped in minimize.py

def parse_bllip_output(parse_output, words):
    """ Input
            parse_output: string type output of the RerankingParser from https://github.com/BLLIP/bllip-parser/tree/master (Charniak parser)
            words: [string] list of words in a sentence which was inputted to the RerankingParser in order to obtain its output

        Output
            returns the parse tree split into a list of string "parse bits" -- how the parse tree is divided per word in CONLL-12 format
            The first parse bit contains the parse_output up to and including the first word : "(S1... (POS_TAG word)"
            Except (POS_TAG word) is replaced by a *, since both the POS_TAG and the word are contained in other columns of CONLL-12
            If the word ends a parenthesis phrase, the closing paranthesis is included in the parse bit
            
    """
    parse_output = re.sub('S1','TOP', parse_output) # CONLL-12 refers to the top layer as top
    parse_bits = []
    for word in words:
        if word == "(":
            word = "-LRB-"
        elif word == ")":
            word = "-RRB-"
        elif word == "?":
            word = r'\?'

        word = word.replace("^", "\^")
        
        try:
            mo = re.match(r'(.*?)(\([A-Z#.:,$-`]+ '+word+r'\))(.*)', parse_output)
        except:
            print(parse_output, words)
        if not mo:
            parse_bits.append("")
            continue
        
        groups = mo.groups()
    
        parse_bit = groups[0]+"*"
        rem = groups[-1].strip()
    
        paran_mo = re.match(r'(\)+)(.*)', rem)
        if paran_mo:
            paran_groups = paran_mo.groups()
            rem = paran_groups[-1]
            parse_bit = parse_bit + paran_groups[0]
    
        parse_bit = re.sub('\s','', parse_bit)
        parse_bits.append(parse_bit)
    
        # split output
        parse_output = rem
        
    return parse_bits

def get_ner_labels(words):

    """ Input: words: [string] tokenized sentence
        Output:
            ner_labels: [string] label corresponding to each word in words. Words with no NER tag are labeled with an "*", words an NER tag are labeled with "(LABEL)".
            If a label spans multiple words, the first word is labeled with "(LABEL*", the following with "*", and the last with "*)"
            This is according to CONLL-12 format
    """

    ner_labels = ["*" for word in words]

    doc = spacy.tokens.Doc(nlp.vocab, words=words)
    
    for ent in ner(doc).ents:
        ent_label = ent.label_
        if ent.end - ent.start > 1:
            ner_labels[ent.start]  = f"({ent_label}*"
            ner_labels[ent.end - 1] = "*)"
        else:
            ner_labels[ent.start] = f"({ent_label})"
    
    return ner_labels

def main(docs, doc_ids):

    """ Input:
            docs: [[string]] list of documents, which are lists of document parts. Ex: [["This is Doc 0 part 0", "This is Doc 0 part 1"], ... ["This is Doc N part 0", ... "This is Doc N part M"]]
            doc_ids: [string] list of document ids corresponding to each document in docs
    """

    # Lower:
    docs = [[part.lower() for part in doc] for doc in docs]
    
    formatted = ""
    
    for idoc, doc in enumerate(docs):
        for ipart, part in enumerate(doc):

            # build string for final output
            formatted = formatted + f"#begin document ({doc_ids[idoc]}); part {ipart:03d}\n"
        
            # Tokenize entry doc into sentences
            sentences = nltk.sent_tokenize(part)
            for sentence in sentences:

                # if a string is only made up of punctuation characters, simple_parse will throw an error. We check the string for non-punct characters and continue if it does not find any
                is_punct = True
                for char in sentence.strip():
                    if char not in '!"#(),-.:;?`{}': # all the characters that will cause simple_parse to error out
                        is_punct = False
                if is_punct:
                    continue
        
                # Then tokenize sentence into words
                words = nltk.word_tokenize(sentence)

                # Process POS-tag:
                pos_tags = [tag[1] for tag in nltk.pos_tag(words)]
        
                # Process parse tree:
                try:
                    parse_output = rrp.simple_parse(words)
                    parse_bits = parse_bllip_output(parse_output, words)
                except:
                    print(f"ERROR on doc {idoc} part {ipart}, sentence '{sentence}'. words = ", words)
                    parse_bits = ["*" for word in words]
        
                # Tag NER:
                ner_labels = get_ner_labels(words)
        
                # Add line for each word to conll formatted text
                for iword, word in enumerate(words):
                    if word == '.' or word == '?':
                        word = '/' + word
                    formatted = formatted + f"{doc_ids[idoc]:10} {ipart:>5} {iword:>5} {word:>20} {pos_tags[iword]:>10} {parse_bits[iword]:>25}\t-\t-\t-\t speaker1 \t{ner_labels[iword]:15}\t-\n"
                formatted = formatted + '\n'
            formatted = formatted + "#end document\n"

    return formatted

if __name__=="__main__":

    import argparse
    import json

    parser = argparse.ArgumentParser()
    parser.add_argument("input_file", help="Input JSON file. Format [{document id: [parts of document]}, ...]")
    parser.add_argument("output_directory", help="Path to output directory to save formatted data")
    parser.add_argument("--parts", default = None, help="How many parts of the input file to process (cumulative over multiple docs if applicable)")
    args = parser.parse_args()
    
    with open(args.input_file, 'r') as json_file:
        data = json.load(json_file)
    
    doc_ids = list(data.keys())
    docs = list(data.values())

    if args.parts is not None:
        Nparts = int(args.parts)
        new_doc_ids = []
        new_docs = []
        nparts = 0
        for doc in docs:
            new_doc = []
            for part in doc:
                nparts = nparts + 1

                if nparts > Nparts:
                    break
                else:
                    new_doc.append(part)
                    
            if nparts > Nparts:
                break
            else:
                new_docs.append(new_doc)
    
    formatted = main(docs, doc_ids)

    # Save
    print(f"Saving formatted data to {args.output_directory}")
    parts = ""
    if args.parts is not None:
        parts = f"_{args.parts}"
    with open(args.output_directory + f"/formatted{parts}.conll", "w") as f:
        f.write(formatted)