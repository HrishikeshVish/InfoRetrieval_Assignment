from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer
import numpy as np
import numpy.linalg as LA
import math
import os
import json
import nltk
import pandas as pd
from tqdm import tqdm
from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import RegexpTokenizer
from os import path
import sys
import time
from preprocess import generateArtifacts
from searchOps import patternMatch, minimumEditDistance, getWildCardMatches, getNormalMatches

def termFrequency(term, document):
    document = document.lower()
    nD = document.split()
    tF = nD.count(term.lower())/float(len(nD))
    return tF
    
def inverseDocumentFrequency(term, documents):
    count = 0
    for doc in documents:
        if term.lower() in doc.lower().split():
            count += 1
    if count > 0:
        return 1.0 + math.log(float(len(documents))/count)
    else:
        return 1.0
def tf_idf(term, document, documents):
    tf = termFrequency(term, document)
    idf = inverseDocumentFrequency(term, documents)
    return tf*idf
    
def generateVectors(query, documents):
    tf_idf_matrix = np.zeros((len(query.split()), len(documents)))
    for i, s in enumerate(query.lower().split()):
        idf = inverseDocumentFrequency(s, documents)
        for j,doc in enumerate(documents):
            tf_idf_matrix[i][j] = idf * termFrequency(s, doc)
    return tf_idf_matrix

def wordCount(s):
    counts = dict()
    words = s.lower().split()
    for word in words:
        if word in counts:
            counts[word] += 1
        else:
            counts[word] = 1
    return counts
def buildQueryVector(query, documents):
    count = wordCount(query)
    vector = np.zeros((len(count),1))
    for i, word in enumerate(query.lower().split()):
        vector[i] = float(count[word])/len(count) * inverseDocumentFrequency(word, documents)
    return vector
def cosineSimilarity(v1, v2):
    return np.dot(v1,v2)/float(LA.norm(v1)*LA.norm(v2))

def computeRelevance(query, documents, tf_idf_matrix, query_vector):
    ranked_docs = []
    for i, doc in enumerate(documents):
        similarity = cosineSimilarity(tf_idf_matrix[:,i].reshape(1, len(tf_idf_matrix)), query_vector)
        ranked_docs.append([doc, float(similarity[0])])
        #print("query document {}, similarity {}".format(i, float(similarity[0])))
    return ranked_docs

def rankByFreq(document_list):
    # Get the number of satisfied query terms for each document
    query_term_match_count = dict()
    for document in document_list:
        if document in query_term_match_count.keys():
            query_term_match_count[document] = query_term_match_count[document] + 1
        else:
            query_term_match_count[document] = 1
    
    # Rank documents in order of number of query terms matched
    ranked_order_of_docs = []
    for document in query_term_match_count.keys():
        ranked_order_of_docs.append([query_term_match_count[document], document])
    ranked_order_of_docs = sorted(ranked_order_of_docs, reverse=True)
    return ranked_order_of_docs

def rankByTFIDF(ranked_order_of_docs, num_docs, query):
    text = []
    for document in ranked_order_of_docs:
        file,offset = document[1].split(" ")
        offset = int(offset)
        corpus = pd.read_csv('./TelevisionNews/'+file)
        snippet = corpus['Snippet'][offset]
        text.append(snippet)

    #count_vect = CountVectorizer()
    #X_train_counts = count_vect.fit_transform(text)
    #tfidf_transformer = TfidfTransformer()
    #tf_idf = tfidf_transformer.fit_transform(X_train_counts)
    tf_idf_matrix = generateVectors(query, text)
    query_vector = buildQueryVector(query, text)
    ranked_docs = computeRelevance(query, text, tf_idf_matrix, query_vector)
    ranked_docs = sorted(ranked_docs, key=lambda x:x[1], reverse=True)
    for i in range(num_docs):
        print(ranked_docs[i][0])
        print("Similarity = ", ranked_docs[i][1])
        
