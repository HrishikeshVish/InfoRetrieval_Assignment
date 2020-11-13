#from elastic import elasticSearch
from search import search
import json
import pandas as pd
from pageRanking import rankByFreq, rankByTFIDF
with open('test.json') as f:
    data = json.load(f)

"""
out = elasticSearch(data)

elasticURLS = []
counter = 0
for item in out:
    elems = []
    output = item['hits']['hits']
    for x in output:
        
        elems.append(x['_source']['\ufeffURL'])
    with open("./Expected/"+str(counter)+".json", "w") as outfile:
        json.dump(elems, outfile)
    counter+=1
    elasticURLS.append(elems)
#print(elasticURLS)
"""
normsearchURLS = []
counter = 0
for ele in data:
    document_list = search(ele)
    print("HERE1")
    ranked_order_of_docs = rankByFreq(document_list)
    
    
    print("HERE2")
    if(len(ranked_order_of_docs)>1000):
        ranked_docs = rankByTFIDF(ranked_order_of_docs[0:1000], 5, ele)
    else:
        ranked_docs = rankByTFIDF(ranked_order_of_docs, 5, ele)
    fin_out = []
    print("HERE")
    for i in range(15):
        file, offset = ranked_docs[i][2].split(" ")
        corpus = pd.read_csv('./TelevisionNews/'+file)
        offset = int(offset)
        snippet = corpus['Snippet'][offset]
        url = corpus['URL'][offset]
        fin_out.append(url)
    with open("./Actual/"+str(counter)+".json", "w") as outfile:
        json.dump(fin_out, outfile)
    normsearchURLS.append(fin_out)
    counter+=1
#print(normsearchURLS)
        

