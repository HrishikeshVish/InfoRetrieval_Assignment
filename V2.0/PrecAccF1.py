import json
import pandas as pd
import os
from tqdm import tqdm
corpus_path = './TelevisionNews'
corpus_files_list = os.listdir(corpus_path)
totalSize = 0
for file_name in tqdm(corpus_files_list):
    try:
        partial_corpus = pd.read_csv('./TelevisionNews/' + file_name)
        if 'URL' in partial_corpus.columns:
            totalSize += len(partial_corpus['URL'])
    except:
        pd.errors.EmptyDataError

print(totalSize)
metricsFull = []
for i in range(10):
    with open('./actual/'+str(i)+'.json') as f:
        actual = json.load(f)
    with open('./expected/'+str(i)+'.json') as f:
        expected = json.load(f)
    metrics = {}
    metrics['tp'] = len(list(set(actual) & set(expected)))
    metrics['fp'] = len(list(set(actual).difference(set(expected))))
    metrics['tn'] = totalSize - len(list(set(actual).union(set(expected))))
    metrics['fn'] = len(list(set(expected).difference(set(actual))))
    metrics['acc'] = metrics['tp'] + metrics['tn']
    metrics['acc'] = metrics['acc']/(metrics['tp'] + metrics['tn'] + metrics['fp'] + metrics['fn'])
    metrics['rec'] = metrics['tp']/(metrics['tp'] + metrics['fn'])
    metrics['prec'] = metrics['tp']/(metrics['tp'] + metrics['fp'])
    metrics['f1'] = metrics['prec'] *metrics['rec']*2 / (metrics['prec'] + metrics['rec'])
                                                                                            
                                                                        
    metricsFull.append(metrics)
    print(metrics)
prec = 0
rec = 0
f1 = 0
acc = 0

for i in range(10):
    prec += metricsFull[i]['prec']
    rec += metricsFull[i]['rec']
    acc += metricsFull[i]['acc']
    f1  += metricsFull[i]['f1']
print("prec = ",prec/10.0)
print("rec = ", rec/10.0)
print("acc = ", acc/10.0)
print("f1 = ", f1/10.0)

    
