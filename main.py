"""
    Main method for search engine
"""

from os import listdir
from modules import InvertedIndex


loader = True
_data_path = "/root/Documents/Project/archive/TelevisionNews/"
_req_file = ["posting_list.json", "pos2doc.json", "vocab.json", "tf_idf_vector.json", "bigrams.json"]

if __name__ == "__main__":
    """
        Main
    """
    paths = sorted([_data_path+i for i in listdir(_data_path)])
    engine = InvertedIndex(paths)
    is_engine = True
    for file_i in _req_file:
        if file_i not in listdir("engine"):
            is_engine = False
            engine.initialize()
            engine.save("engine/")
            break

    if is_engine:
        engine.load("engine/")

    # query = input("Query = ")
    query = "mediteranean"
    ans = engine.run_query(query, ranking=True, ranking_algo='cos', top_n=10)
    for i in ans:
        try:
            print('Path : ', i['Path'])
        except:
            continue
        print('Row_no : ', i['Row_no'])
        try:
            print('rank_points : ', i['rank_points'])
        except:
            pass
        for j in i.keys():
            if j != 'Path' and j != 'Row_no' and j != 'rank_points':
                print(j, ":", i[j])
        print("\n\n")
