import json
from search import search
from pageRanking import rankByFreq, rankByTFIDF
import pandas as pd

import os
from tqdm import tqdm
import matplotlib.pyplot as plt

corpus_path = './TelevisionNews'
corpus_files_list = os.listdir(corpus_path)
totalSize = 0
fileNames = {}

for file_name in tqdm(corpus_files_list):
    try:
        partial_corpus = pd.read_csv('./TelevisionNews/' + file_name)
        if 'URL' in partial_corpus.columns:
            for i in partial_corpus["URL"]:
                fileNames[i] = file_name
                
    except:
        pd.errors.EmptyDataError

#print(fileNames)
        
with open('groundTruth2.json', encoding='utf-8') as f:
    data = json.load(f)
URLs = {}
queries = list(data.keys())
snippets = {}
for ele in queries:
    retVal = data[ele]["result"]
    snippets[ele] = []
    elasticFiles = []
    URLs[ele] = []
    for i in retVal:
        URLs[ele].append(i["_source"]["ï»¿URL"])
        elasticFiles.append(fileNames[i["_source"]["ï»¿URL"]])
        
    similarity_scores = {}
    document_list = search(ele)
    ranked_order_of_docs = rankByFreq(document_list)
    if(len(ranked_order_of_docs)>1500):
        ranked_docs = rankByTFIDF(ranked_order_of_docs[0:1500], 5, ele)
    else:
        ranked_docs = rankByTFIDF(ranked_order_of_docs, 5, ele)
    for doc in ranked_docs:
        f,o = doc[2].split(" ")
        similarity = doc[1]
        similarity_scores[f] = similarity
    for ele in elasticFiles:
        if ele in similarity_scores.keys():
            print(similarity_scores[ele])
        else:
            print(0)
        
        
        
    

