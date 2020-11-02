from utils import csv_to_list
from nltk.tokenize import RegexpTokenizer
from .TrieDS import Trie
from concurrent.futures import ThreadPoolExecutor, as_completed, ProcessPoolExecutor
from json import dumps
from pandas import read_csv
_tokenizer = RegexpTokenizer(r'[^\W_]+')


class InvertedIndex(object):
    """
    docstring
    """
    def __init__(self):
        self.trie = Trie()
        self._tokenizer = RegexpTokenizer(r'[^\W_]+')


    def from_csv(self, path, doc_id):
        """
            Creates per column
        """

        csv = read_csv(path)
        with ProcessPoolExecutor(max_workers=32) as worker:
            workers = {
                        worker.submit(self._tokenizer.tokenize, 
                        csv[csv.columns[i_col]][i_row]):[i_row, i_col] 
                        for i_col in range(len(csv.columns)) 
                            for i_row in range(len(csv[csv.columns[i_col]]))
                      }
            
            with ThreadPoolExecutor(max_workers=8) as worker2:
                for tokenize_res in as_completed(workers):
                    row_col = workers[tokenize_res]
                    tokens = tokenize_res.result()
                    for i_token in range(len(tokens)):
                        worker2.submit(self.trie.add_string, tokens[i_token][0], tokens[i_token][1:], doc_id, row_col, i_token)

                        

    def save(self, filepath):
        """
        """
        f = open(filepath, 'w')
        f.write(dumps(self.trie.to_dict()))
        f.close()




