from os import listdir
from modules import Trie
from modules.TrieDS import merge
from modules import InvertedIndex
from pandas import read_csv
import sys

_data_path = "/root/Documents/Project/archive/TelevisionNews/"



def pos_in_csv(pos):
    """
    """
    paths = sorted([_data_path+i for i in listdir(_data_path)])
    for i_doc in pos.keys():
        print(paths[int(i_doc)-1], "\n\n")
        csv = read_csv(paths[int(i_doc)])
        for i_row in pos[i_doc]:
            for col in csv.columns:
                print("\t", col, " : ", csv[col][i_row])
            print("\n\n")
        print("\n\n")




if __name__ == "__main__":
    """
    """
    search_term = "un*ed"
    if len(sys.argv) == 2:
        search_term = sys.argv[1]

    engine = InvertedIndex()
    if not ("posting_list.json" in listdir("engine/") and "pos2doc.json" in listdir("engine/")):
        paths = sorted([_data_path+i for i in listdir(_data_path)])

        for i_path in range(len(paths)):
            engine.from_csv(paths[i_path], i_path)
        engine.save("engine/")

    else:
        engine.load("engine/")

    ans = engine.search(search_term)
    print("START")
    pos_in_csv(ans)
    print("END")
    