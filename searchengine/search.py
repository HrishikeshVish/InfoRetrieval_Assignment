# Import required modules
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
from searchengine.preprocess import generateArtifacts
from searchengine.searchOps import patternMatch, minimumEditDistance, getWildCardMatches, getNormalMatches


        
def search(query):


    # Dowload the wordnet corpus for nltk
    nltk.download("punkt")
    nltk.download("wordnet")

    # Declare the Stemmer, Lemmatizer and Tokenizer
    stemmer = PorterStemmer()
    lemmatizer = WordNetLemmatizer()
    term_tokenizer = RegexpTokenizer(r'[a|b|c|d|e|f|g|h|i|k|l|m|n|o|p|q|r|s|t|u|v|w|x|y|z|?|\*]+')
    wildcard_tokenizer = RegexpTokenizer(r'[a|b|c|d|e|f|g|h|i|k|l|m|n|o|p|q|r|s|t|u|v|w|x|y|z]+')
    stemmer.stem(lemmatizer.lemmatize("sample done"))

    # Obtain the posting list and bigram index
    posting_list, bigram_index, permuterm_index = generateArtifacts()


    # Take input query
    #query = input("Please enter the query string: ")
    #query = "united environmental agency"
    
    start = time.time()

    # Get the desired documents list
    document_list = []
    for query_term in term_tokenizer.tokenize(query.lower()):
        # If query term is a wildcard query
        if "*" in query_term or "?" in query_term:
            document_list = getWildCardMatches(query_term, permuterm_index, document_list, wildcard_tokenizer, posting_list)
            
        # If query term is a normal query
        else:
            document_list = getNormalMatches(stemmer, lemmatizer, query_term, document_list, posting_list, bigram_index)
            
            
    
    

    end = time.time()
    
    


    
    #print("Documents that are relevant to the search are:\n", ranked_order_of_docs, "\n")
    print("--- %0.5f seconds ---" % (end - start))
    return document_list
#search(5)
