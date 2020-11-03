from os import listdir
from modules import Trie
from modules.TrieDS import merge
from modules import InvertedIndex


_data_path = "./data/"


if __name__ == "__main__":
    """
    """
    engine = InvertedIndex()
    if "posting_list.json" not in listdir("engine/") or \
        "pos2doc.json" not in listdir("engine/"):
        paths = sorted([_data_path+i for i in listdir(_data_path)])

        for i_path in range(len(paths)):
            engine.from_csv(paths[i_path], i_path)
        engine.save("engine/")

    else:
        engine.load("engine/")

    search_term = "un*ed"
    ans = engine.search(search_term)
    for i in ans.keys():
        print(i, " : ", ans[i], "\n\n\n")
    