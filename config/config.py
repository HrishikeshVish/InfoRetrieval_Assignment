"""
    Loads config file
"""
from json import loads


# f_config = open("./config.json", "r")

# SEARCH_ENGINE_CONFIG = loads(f_config.read())

# f_config.close()

REQUIRED_FILE_FOR_ENGINE = ["posting_list.json", "pos2doc.json", "vocab.json", "tf_idf_vector.json", "bigrams.json"]

DATA_PATH = "/root/Documents/Project/archive/TelevisionNews/"

ENGINE_PATH = "./engine/"

LOG_FILE = "./log/log.logs"
