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
    docstring
    """
    def __init__(self):
        self._trie = Trie()
        self._tokenizer = RegexpTokenizer(r'[^\W_]+')
        self._stemmer = PorterStemmer()
        self._lemmatizer = WordNetLemmatizer()
        self._post2doc_mapper = [0]
        self._docs = [-1]


    def from_csv(self, path, doc_id):
        """
            Creates per column
        """
        try:
            csv = read_csv(path)
        except Exception as e:
            print(e)
            return
        # with ProcessPoolExecutor(max_workers=32) as worker:
        #     workers = {
        #                 worker.submit(self._tokenizer.tokenize, 
        #                 csv['Snippet'][i_row]):i_row
        #                     for i_row in range(len(csv['Snippet']))
        #               }
            
        #     with ThreadPoolExecutor(max_workers=8) as worker2:
        #         for tokenize_res in as_completed(workers):
        #             row_col = workers[tokenize_res]
        #             tokens = tokenize_res.result()
        #             if doc_id == 1 and row_col == 94:
        #                 print([self._stemmer.stem(self._lemmatizer.lemmatize(token)) for token in tokens])
        #             for token in tokens:
        #                 term = self._stemmer.stem(self._lemmatizer.lemmatize(token))
        #                 worker2.submit(self._trie.add_string, term[0], term[1:], doc_id, row_col)
        
        self._post2doc_mapper.append(self._post2doc_mapper[-1] + len(csv['Snippet']))
        self._docs.append(doc_id)

        for i_row in range(len(csv['Snippet'])):
            tokens = self._tokenizer.tokenize(csv['Snippet'][i_row])
            for token in tokens:
                term = self._stemmer.stem(self._lemmatizer.lemmatize(token))
                self._trie.add_string(term, self._post2doc_mapper[-2]+i_row)

    def search(self, string):
        """
        """
        poss = self._trie.search(string)
        print(self._post2doc_mapper)
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
        """
        f = open(filepath+"posting_list.json", 'w')
        f.write(dumps(self._trie.to_dict()))
        f.close()
        f = open(filepath+"pos2doc.json", 'w')
        f.write(dumps({i:j for i, j in zip(self._docs, self._post2doc_mapper)}))
        f.close()

    def load(self, filepath):
        """
        """
        f = open(filepath+"posting_list.json", 'r')
        self._trie.from_dict(loads(f.read()))
        f.close()
        f = open(filepath+"pos2doc.json", 'r')
        mapper = loads(f.read())
        f.close()
        posndoc = sorted([(i, mapper[i]) for i in mapper.keys()])
        self._post2doc_mapper = [int(i[1]) for i in posndoc]
        self._docs = [i[0] for i in posndoc]




