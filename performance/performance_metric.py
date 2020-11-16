
from search import search
import json
import pandas as pd
from pageRanking import rankByFreq, rankByTFIDF

with open('./performance/expectedList1.json') as f:
    data = json.load(f)
expected = data
queries = list(data.keys())

normsearchURLS = []
counter = 0
actualOutput = {}
count = 0
for ele in queries:
    if(count == 4):
        count+=1
        continue
    count+=1
    document_list = search(ele)
    
    ranked_order_of_docs = rankByFreq(document_list)
    actualOutput[ele] = []
    
    
    if(len(ranked_order_of_docs)>1000):
        ranked_docs = rankByTFIDF(ranked_order_of_docs, 5, ele)
    else:
        ranked_docs = rankByTFIDF(ranked_order_of_docs, 5, ele)
    fin_out = []
    size = len(ranked_docs)
    if(size>10):
        size = 10
        
    for i in range(size):
        file, offset = ranked_docs[i][2].split(" ")
        corpus = pd.read_csv('./TelevisionNews/'+file)
        offset = int(offset)
        snippet = corpus['Snippet'][offset]
        url = corpus['URL'][offset]
        fin_out.append(url)
        actualOutput[ele].append(url)
    with open("./performance/Actual/"+str(counter)+".json", "w") as outfile:
        json.dump(fin_out, outfile)
    normsearchURLS.append(fin_out)
    counter+=1
with open("./performance/actualList.json", "w") as out:
    json.dump(actualOutput, out)
print(actualOutput)

actual = {}
for i in range(10):
    with open("./performance/Actual/"+str(i)+".json") as f:
        data = json.load(f)
        actual[queries[i]] = data
#print(actual)
print(actual.keys())

for i in list(actual.keys()):
    
    #print(len(actual[i]))
    #print(len(expected[i]))
    print(len(list(set(actual[i]) & set(expected[i]))))
    

