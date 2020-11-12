import requests
from elasticsearch import Elasticsearch
import json
import csv
import sys
import os
from tqdm import tqdm
from elasticsearch import helpers, Elasticsearch
import csv

es = Elasticsearch()


def CSV2JSON(csvFile): 
    data = dict()
    with open(csvFile, encoding='utf-8') as csvf: 
        csvReader = csv.DictReader(csvf)
        for rows in csvReader: 
            key = rows['\ufeffURL'] 
            data[key] = rows 
    return data
          
# change this
path = '../TelevisionNews/'
paths = sorted([path+i for i in os.listdir(path)])
es = Elasticsearch([{'Host':'localhost','port':9200}])
r = requests.get('http://127.0.0.1:9200')
# if 200 all is good
print(r.status_code)
# index all the data points
i = 0
for file_i in paths:
    # es.index(index=str(i), body=CSV2JSON(file_i))
    with open(file_i) as f:
        reader = csv.DictReader(f)
	# if this not work use es.index()
        # es.index(index='my-index', doc_type='my-type', id=i, body=JSONthing)
        helpers.bulk(es, reader, index='my-index', doc_type='my-type')
    i += 1

## Do this multiple times on dat json file
import time
now = time.time()
a = es.search(index="my-index", body={'query':{"match": {"Snippet":"germany suffers"}}})
print("Time for search:",time.time() - now)
