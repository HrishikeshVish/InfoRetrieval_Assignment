from searchengine.search import search
from searchengine.pageRanking import rankByFreq, rankByTFIDF
import pandas as pd
import time
cond = 'Y'
while cond == 'Y' or cond == 'y':
    print("Enter the search Term")
    query = input()
    start = time.time()
    document_list = search(query)
    #print(document_list)
    ranked_order_of_docs = rankByFreq(document_list)
    if "*" in query or "?" in query:
        ranked_docs = ranked_order_of_docs[0:10]
        for doc in ranked_docs:
            f, o = doc[1].split(" ")
            corpus = pd.read_csv('./TelevisionNews/'+f)
            url = corpus['URL'][int(o)]
            snippet = corpus['Snippet'][int(o)]
            print(url)
            print(snippet)
            print()
        end = time.time()
        print(len(ranked_docs) , " results fetched in ", end-start, "s")
    else:
        if(len(ranked_order_of_docs)>1500):
            ranked_docs = rankByTFIDF(ranked_order_of_docs[0:1500], 5, query)[0:10]
        else:
            ranked_docs = rankByTFIDF(ranked_order_of_docs, 5, query)[0:10]
    #print(ranked_docs)
        for doc in ranked_docs:
        
            snippet = doc[0]
            similarity = doc[1]
            file = doc[2]
            f, o = file.split(" ")
            corpus = pd.read_csv('./TelevisionNews/'+f)
            url = corpus['URL'][int(o)]
            print(url)
            print(snippet)
            print(similarity)
            print()
        end = time.time()
        print(len(ranked_docs) , " results fetched in ", end-start,"s")
    
    
    print("do you wish to add a new query? Y or N")
    cond = input()
    


