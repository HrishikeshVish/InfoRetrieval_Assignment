import requests
from elasticsearch import Elasticsearch
import json
import csv
import sys
import os
from tqdm import tqdm
from elasticsearch import helpers, Elasticsearch
import csv
import pandas as pd
es = Elasticsearch()


def CSV2JSON(csvFile): 
    with open(csvFile, encoding='utf8') as csvf: 
        csvReader = csv.DictReader(csvf)
        data = {}
        for rows in csvReader:
            key = rows['\ufeffURL'] 
            data[key] = rows 
    return json.dumps(data)

def elasticSearch(query):         
    # change this
    path = './TelevisionNews/'
    paths = sorted([path+i for i in os.listdir(path)])
    es = Elasticsearch([{'Host':'localhost','port':9200,"index.mapping.total_fields.limit": 2000}])
    r = requests.get('http://127.0.0.1:9200')
    # if 200 all is good
    print(r.status_code)
    # index all the data points
    i = 1
    for file_i in paths:
        #es.index(index=str(i), body=CSV2JSON(file_i))
        with open(file_i, encoding='utf8') as f:
            reader = csv.DictReader(f)
            #es.index(index='my-index', id=i, body=CSV2JSON(file_i))
            # if this not work use es.index()
            helpers.bulk(es, reader, index='my-index', doc_type='my-type')
            #print(i)
    
        i += 1

    ## Do this multiple times on dat json file
    import time
    now = time.time()
    out = []
    for item in query:
        a = es.search(index="my-index", size = 10000, body={'size':10, 'query':{"match":{"Snippet":{"query":item, "fuzziness":"AUTO","auto_generate_synonyms_phrase_query" : "false"}}}})
        item1 = a['hits']['hits']
        for hit in a['hits']['hits']:
            snippet = hit['_source']['Snippet']
            URL = hit['_source']['\ufeffURL']
            out.append(URL)
    out = list(set(out))
    print(len(out))
        


    print("Time for search:",time.time() - now)
    return out
t = elasticSearch(['united states'])
