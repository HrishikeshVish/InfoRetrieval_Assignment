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

def generatePostingList(stemmer, lemmatizer, tokenizer):
    # Get list of files in dataset
    corpus_path = './TelevisionNews'
    corpus_files_list = os.listdir(corpus_path)

    print("Generating the Posting List")

    # Initialize Posting List as an empty Dictionary
    posting_list = dict()

    # Iterate through each file in the dataset and create a combined corpus
    for file_name in tqdm(corpus_files_list):
        try:
            # Read contents of each file in the dataset and check if comforms to the required format
            partial_corpus = pd.read_csv('./TelevisionNews/' + file_name)
            if 'Snippet' in partial_corpus.columns:
                for row_number in range(len(partial_corpus['Snippet'])):
                    snippet = partial_corpus['Snippet'][row_number]
                    # Iterate through each token in the snippet and update the posting list
                    for word in tokenizer.tokenize(snippet.lower()):
                        snl_word = stemmer.stem(lemmatizer.lemmatize(word))
                        document_id = file_name + ' ' + str(row_number)
                        if(snl_word in posting_list.keys()):
                            if(posting_list[snl_word][-1] != document_id):
                                posting_list[snl_word].append(document_id)
                        else:
                            posting_list[snl_word] = [document_id]

        except pd.errors.EmptyDataError:
            continue
    for snl_word in posting_list.keys():
        posting_list[snl_word] = list(set(posting_list[snl_word]))
    
    # Save the full posting list as a json file
    posting_list_file = open('./searchengine/posting_list.json', 'w+')
    json.dump(posting_list, posting_list_file, indent=4)
    posting_list_file.close()
    print('Posting List Generated')
    return posting_list
    
def generateBigramIndex(posting_list):
    # Initialize the bigram_index as an empty dictionary
    bigram_index = dict()

    # Iterate through the vocabulary and generate the bigram index
    for snl_word in tqdm(posting_list.keys()):
        bigrams = [''.join(bigram) for bigram in nltk.bigrams(snl_word)]
        for bigram in bigrams:
            if(bigram in bigram_index.keys()):
                bigram_index[bigram].append(snl_word)
            else:
                bigram_index[bigram] = [snl_word]
    for bigram in bigram_index.keys():
        bigram_index[bigram] = list(set(bigram_index[bigram]))
    
    # Save the full bigram_index as a json file
    bigram_index_file = open('./searchengine/bigram_index.json', 'w+')
    json.dump(bigram_index, bigram_index_file, indent=4)
    bigram_index_file.close()
    print('Bigram Index Generated')
    return bigram_index

def generatePermutermIndex(posting_list):
    # Initialize the permuterm_index as an empty dictionary
    permuterm_index = dict()

    # Iterate through the vocabulary and generate the permuterm index
    for snl_word in tqdm(posting_list.keys()):
        for length in range(1, len(snl_word)+1):
            ngrams = [''.join(ngram) for ngram in nltk.ngrams(snl_word, length)]
            for ngram in ngrams:
                if(ngram in permuterm_index.keys()):
                    permuterm_index[ngram].append(snl_word)
                else:
                    permuterm_index[ngram] = [snl_word]
    for permuterm in permuterm_index.keys():
        permuterm_index[permuterm] = list(set(permuterm_index[permuterm]))
    
    # Save the full permuterm_index as a json file
    permuterm_index_file = open('./searchengine/permuterm_index.json', 'w+')
    json.dump(permuterm_index, permuterm_index_file, indent=4)
    permuterm_index_file.close()
    print('Permuterm Index Generated')
    return permuterm_index
    
def generateArtifacts():


    # Dowload the wordnet corpus for nltk
    nltk.download('punkt')
    nltk.download('wordnet')

    # Declare the Stemmer, Lemmatizer and Tokenizer
    stemmer = PorterStemmer()
    lemmatizer = WordNetLemmatizer()
    tokenizer = RegexpTokenizer(r'[a|b|c|d|e|f|g|h|i|k|l|m|n|o|p|q|r|s|t|u|v|w|x|y|z]+')
    if (path.exists('./searchengine/posting_list.json') == True):
        print("For the current corpus, Posting List already exists...")
        posting_list_file = open("./searchengine/posting_list.json", "r")
        posting_list = json.loads(posting_list_file.read())
    else:
        posting_list = generatePostingList(stemmer, lemmatizer, tokenizer)
        
    

    print("Generating the Bigram Index")
    if(path.exists('./searchengine/bigram_index.json') == True):
        print("Bigram Index exists for current vocabulary...")
        bigram_index_file = open("./searchengine/bigram_index.json", "r")
        bigram_index = json.loads(bigram_index_file.read())
    else:
        bigram_index = generateBigramIndex(posting_list)
        

    print("Generating Permuterm Index")
    if(path.exists('./searchengine/permuterm_index.json')==True):
        print("Permuterm Index already exists...")
        permuterm_index_file = open("./searchengine/permuterm_index.json", "r")
        permuterm_index = json.loads(permuterm_index_file.read())
    else:
        permuterm_index = generatePermutermIndex(posting_list)
        
    return posting_list, bigram_index, permuterm_index
