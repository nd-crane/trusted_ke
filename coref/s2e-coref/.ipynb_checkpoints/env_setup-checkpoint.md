### s2e-coref environment setup

Github: https://github.com/yuvalkirstain/s2e-coref

Step taken:
1. wget https://raw.githubusercontent.com/yuvalkirstain/s2e-coref/main/requirements.txt
2. Did not follow initial instruction to pip install requirements.txt, but created miniforge env called s2e0
Following commands:
* mamba install pytorch==1.4.0 # this installed python 3.8.18
* mamba install transformers==3.3.1
* mamba install tensorboard==2.3.0
    * It said that this finished executing but gave me this error in install_error.txt
* mamba install scipy==1.5.2
    * This updated pytorch to 2.0.1, and numpy from 1.19.2 to 1.22.3
    * Received the same error
* mamba install gitpython
3. Created format_data.ipynb to put the data in expected location and format (which made data directory)
4. wget https://raw.githubusercontent.com/yuvalkirstain/s2e-coref/main/minimze.py
5. export DATA_DIR=data
6. corrected name from minimze.py to minimize.py
7. python minimize.py $DATA_DIR
8. Received error: ModuleNotFoundError: No module named 'conll'
    * Tracked down conll- this github: https://github.com/YerevaNN/SciERC/tree/master
    * Since he only uses the get_doc_key function and BEGIN_DOCUMENT_REGEX, I just modified minimize.py by definining it at the top
    * got rid of conll. before BEGIN_DOCUMENT_REGEX and get_doc_key throughout minimize.py
9. Got error ModuleNotFoundError: No module named 'utils'
    * utils.flatten_list_of_lists only used once and pretty straightforward, just defined it at top under conll lines
10. After that, worked fine on conll data!