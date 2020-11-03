from utils import csv_to_list
from nltk.tokenize import RegexpTokenizer
from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer
from .TrieDS import Trie
from concurrent.futures import ThreadPoolExecutor, as_completed, ProcessPoolExecutor
from json import dumps, loads
from pandas import read_csv



class InvertedIndex(object):
    """
        Inverted Index using trie as data-structure
    """
    def __init__(self):
        """
            Constructor to initialize trie, tokenizer and lemmatizer
        """
        self._trie = Trie()
        self._tokenizer = RegexpTokenizer(r'[^\W_]+')
        self._stemmer = PorterStemmer()
        self._lemmatizer = WordNetLemmatizer()
        self._post2doc_mapper = [0]
        self._docs = [-1]


    def from_csv(self, path, doc_id):
        """
            read CSV and created inverted index for 'Snippet' column
        """
        try:
            csv = read_csv(path)
        except Exception as e:
            print(e)
            return
        
        self._post2doc_mapper.append(self._post2doc_mapper[-1] + len(csv['Snippet']))
        self._docs.append(doc_id)

        for i_row in range(len(csv['Snippet'])):
            tokens = self._tokenizer.tokenize(csv['Snippet'][i_row])
            for token in tokens:
                term = self._stemmer.stem(self._lemmatizer.lemmatize(token))
                self._trie.add_string(term, self._post2doc_mapper[-2]+i_row)

    def search(self, string):
        """
            Search string in trie
            map the hashed row-doc_id number returned from trie search as {doc_id: [rows]}
            return resultant {doc_id: [rows]}

        """
        if '*' not in string:
            string = self._stemmer.stem(self._lemmatizer.lemmatize(string))
        poss = self._trie.search(string)
        res = {}
        for pos in poss:
            for i_doc in range(len(self._post2doc_mapper)):
                if pos < self._post2doc_mapper[i_doc]:
                    if self._docs[i_doc] in res.keys():
                        res[self._docs[i_doc]].append(pos - self._post2doc_mapper[i_doc-1])
                        break
                    else:
                        res[self._docs[i_doc]] = [pos - self._post2doc_mapper[i_doc-1]]
                        break

        return res


    def save(self, filepath):
        """
            Save Inverted Index - Posting List as posting_list.json
            and hashed row-doc_id as pos2doc.json
        """
        f = open(filepath+"posting_list.json", 'w')
        f.write(dumps(self._trie.to_dict()))
        f.close()
        f = open(filepath+"pos2doc.json", 'w')
        f.write(dumps({i:j for i, j in zip(self._docs, self._post2doc_mapper)}))
        f.close()

    def load(self, filepath):
        """
            Load data from saved posting list and hashed row-doc_id mapper
        """
        f = open(filepath+"posting_list.json", 'r')
        self._trie.from_dict(loads(f.read()))
        f.close()
        f = open(filepath+"pos2doc.json", 'r')
        mapper = loads(f.read())
        f.close()
        posndoc = sorted([(int(mapper[i]),i) for i in mapper.keys()])
        self._post2doc_mapper = [i[0] for i in posndoc]
        self._docs = [i[1] for i in posndoc]




