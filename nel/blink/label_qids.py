import requests
import re
import pandas as pd
import sys
sys.path.append("./BLINK")
from main_dense import _load_candidates

def lookup(url, qiddict):
    
    qidp = re.compile(r'.*id="t-wikibase" class="mw-list-item"><a href="https://www.wikidata.org/wiki/Special:EntityPage/(Q\d*)".*')

    content = str(requests.get(url).content)
    mo = re.match(qidp, content)

    if mo:
        QID = mo.groups()[0]
    else:
        QID = url
        
    qiddict.update({url:QID})
            
    return QID, qiddict

if __name__=="__main__":
    
    # Get candidate dicts
    print("Loading candidate encoding")
    (
        candidate_encoding,
        title2id,
        id2title,
        id2text,
        wikipedia_id2local_id,
        faiss_indexer,
    ) = _load_candidates(
        "BLINK/models/entity.jsonl", 
        "BLINK/models/all_entities_large.t7", 
        faiss_index=None, 
        index_path=None,
        logger=None,
    )

    id2url = {
        v: "https://en.wikipedia.org/wiki?curid=%s" % k
        for k, v in wikipedia_id2local_id.items()
    }
    
    
    print("Reading results csv")
    results = pd.read_csv("../../data/results/blink_results.csv")
    results_dict = {"doc_idx":[], "sent_idx":[], "original_sentence":[], "input":[], "mention":[], "biencoder_predicted_entity":[], "bi_qid":['']*len(results), "bi_desc":['']*len(results), "crossencoder_predicted_entity":[], "cross_qid":['']*len(results), "cross_desc":['']*len(results)}
    
    for col in results.columns:
        if col in results_dict:
            results_dict[col] = list(results[col])
    
    print("Looking up QIDs and descriptions")
    url2qid = {}
    
    for irow in range(len(results)):
        
        # Biencoder:
        bi_entity = results["biencoder_predicted_entity"].iat[irow]
        bi_entity_id = title2id[bi_entity]
        url = id2url[bi_entity_id]
        desc = id2text[bi_entity_id]
        
        if url in url2qid:
            qid = url2qid[url]
        else:
            qid, url2qid = lookup(url, url2qid)

        results_dict["bi_qid"][irow] = qid
        results_dict["bi_desc"][irow] = desc
        
        # Crossencoder:
        cross_entity = results["crossencoder_predicted_entity"].iat[irow]
        cross_entity_id = title2id[cross_entity]
        url = id2url[cross_entity_id]
        desc = id2text[cross_entity_id]
        
        if url in url2qid:
            qid = url2qid[url]
        else:
            qid, url2qid = lookup(url, url2qid)
                                
        results_dict["cross_qid"][irow] = qid
        results_dict["cross_desc"][irow] = desc
        
        # print out status
        length = 50
        fill = "#"
        prefix = "Entries Processed:"
        suffix = ""
        percent = ("{0:.1f}").format(100 * (irow / float(len(results))))
        filled_length = int(length * irow // len(results))
        bar = fill * filled_length + '-' * (length - filled_length)
        sys.stdout.write(f'\r{prefix} |{bar}| {percent}% {suffix}', )
        sys.stdout.flush()
        
    pd.DataFrame(results_dict).to_csv("../../data/results/blink_results_labeled.csv", index=False)