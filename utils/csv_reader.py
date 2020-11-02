import os


def csv_to_list(path):
    """
    """
    f = open(path, "r")
    lines = f.readlines()
    req_list = [line.split(",") for line in lines]
    return req_list


def csvs_from_directory(path):
    """
    """
    assert(os.path.isdir(path))
    csvs = os.listdir(path)
    if path[-1] != '/':
        path += '/'
    
    doc_token = {}
    for csv in csvs:
        doc_token[csv] = csv_to_list(csv)
    
    return doc_token