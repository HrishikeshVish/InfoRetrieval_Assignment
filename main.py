"""
    Main method for search engine
"""

from os import listdir
from modules import InvertedIndex
from config import DATA_PATH, REQUIRED_FILE_FOR_ENGINE, ENGINE_PATH
from config import RANKING_ALGO, SHOW_DETAIL, TOTAL_N_RESULT, RANKING
from utils import logger
import sys


_IS_ENGINE = True

if __name__ == "__main__":
    """
        Main function that run search engine
    """
    paths = sorted([DATA_PATH+i for i in listdir(DATA_PATH)])
    engine = InvertedIndex(paths)
    for file_i in REQUIRED_FILE_FOR_ENGINE:
        if file_i not in listdir(ENGINE_PATH):
            _IS_ENGINE = False
            engine.initialize()
            engine.save(ENGINE_PATH)
            break

    if _IS_ENGINE:
        engine.load("engine/")

    while 1:
        try:
            query = input("[Note: Press Ctrl+C to abort]\nEnter Search Query : ")
        except Exception as exe:
            logger(exe)
            exit(0)
        ans = engine.run_query(query,
                              ranking=RANKING,
                              ranking_algo=RANKING_ALGO,
                              top_n=TOTAL_N_RESULT,
                              show_detail=SHOW_DETAIL)
        if ans:
            print("\n\nPrinting relevant results\n\n")
        for i in ans:
            try:
                print('Path : ', i['Path'])
            except Exception as exe:
                logger(exe)
                continue
            print('Row_no : ', i['Row_no'])
            try:
                print('rank_points : ', i['rank_points'])
            except Exception as exe:
                logger(exe)
            for j in i.keys():
                if j != 'Path' and j != 'Row_no' and j != 'rank_points':
                    print(j, ":", i[j])
            print("\n\n")

        _y_n = input("Want to continue?[y/N]")
        if not _y_n:
            break
        if _y_n.lower() == "n":
            break
        if _y_n.lower() == "y":
            sys.stderr.write("\x1b[2J\x1b[H")
            continue
        print("wrong input")
        sys.exit(1)
