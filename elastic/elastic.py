# -*- coding: utf-8 -*-
"""
Created on Sat Nov 14 12:20:21 2020

@author: 91948
"""
from elasticsearch import Elasticsearch,helpers
from tqdm import tqdm
import requests
import time
import json
import csv
import os

# change if data already indexed
index = True
res = requests.get("http://127.0.0.1:9200")
if res.status_code !=200:
    print("Shit")
    
    
path = './TelevisionNews/'
paths = sorted(list(map(lambda x:path+x,os.listdir(path))))
es = Elasticsearch([{'host': 'localhost', 'port': 9200}])

if index:
    for file in tqdm(paths):
        try:
            with open(file) as f:
                reader = csv.DictReader(f)
                for rows in reader:
                     es.index(index='test',body=rows)   
        except:
            pass

# test the queries
with open('queries.txt') as f:
    queries = json.loads(f.read().strip(''))

data = dict()
for query in queries:
    data[query] =dict()
    start = time.time()
    response = es.search(index="test", body={"query": {"match": {'Snippet':query}}})
    data[query]['time'] = time.time() - start
    data[query]['result'] = response['hits']['hits'][:3] #change this if needed
    
# generate GT    
with open('groudTruth.txt', 'w') as outfile:
    json.dump(data, outfile)
