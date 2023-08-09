#!/usr/bin/env python3

import crosslingual_coreference
import spacy
import pandas as pd

def resolve():

    DEVICE = 0 # Number of the GPU, -1 if want to use CPU

    #Disabled pipes will be loaded but they won’t be run unless you explicitly enable them
    #using en_core_web_trf instead of en_core_web_sm for increased accuracy
    coref = spacy.load('en_core_web_trf', disable=['ner', 'tagger', 'parser', 'attribute_ruler', 'lemmatizer'])

    # Add coreference resolution model as shown in documentation
    #https://spacy.io/universe/project/crosslingualcoreference
    coref.add_pipe("xx_coref", config={"chunk_size": 2500, "chunk_overlap": 2, "device": DEVICE})


    # apply to MaintNet on text cols
    df = pd.read_csv('MaintNet_data/Aircraft_Annotation_DataFile.csv')
    #textcols = ['problemDescription','csmpNarrativeSummary','recommendSolution']
    textcols = ['problemDescription']

    corefdict = {textcol : [] for textcol in textcols}
    for irow in range(len(df)):
        for textcol in textcols:
            if type(df[textcol].iat[irow]) == str:
                if len(df[textcol].iat[irow].split()) > 2:
                    try:
                        corefdict[textcol].append(coref(df[textcol].iat[irow])._.resolved_text)
                    except:
                        print(textcol, irow)
                        print(df[textcol].iat[irow])
                        print(coref(df[textcol].iat[irow]))
                        print(coref(df[textcol].iat[irow])._.resolved_text)
                        print(corefdict[textcol])
                    
                else:
                    corefdict[textcol].append(df[textcol].iat[irow])
                    
            else:
                corefdict[textcol].append('')
                
    pd.DataFrame.from_dict(corefdict).to_csv('MaintNet_data/Aircraft_Annotation_DataFile.csv', index=False)
    
    return

    
if __name__ == '__main__':
    resolve()