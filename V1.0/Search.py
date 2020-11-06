import pandas as pd
from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import RegexpTokenizer
from nltk import bigrams
stemmer = PorterStemmer()
lemmatizer = WordNetLemmatizer()
tokenizer = RegexpTokenizer(r'\w+')
def search(queryString):
    corpus = pd.read_csv('postingList.csv')
    print(corpus['word'])
    queryWords = []
    for word in tokenizer.tokenize(queryString.lower()):
        queryWords.append(stemmer.stem(lemmatizer.lemmatize(word)))
    print(queryWords)
    lists = []
    print(corpus['word'][0])
    words = list(corpus['word'])
    for word in queryWords:
        
        if word in words:
            documents = eval(corpus['List'][words.index(word)])
            if(len(lists) == 0):
                lists = documents
            else:
                intersection = list(set(lists).intersection(documents))
                if(len(intersection) != 0):
                    lists = intersection
                else:
                    if(len(documents)>len(lists)):
                        lists = documents
    if(len(lists) == 0):
        for word in queryWords:
            wordBigram = list(bigrams(word))
            wordBigram = list(map(''.join, wordBigram))
            print(wordBigram)
 
                    
    
        
        
    
search("bobo goober poopoo")
