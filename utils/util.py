import os
from numpy import dot, linalg, array, zeros



def string_vector(string, n):
    s_v = zeros(n)
    for i,j in enumerate(string):
        s_v[i] = ord(j)
    return s_v


def cosine_sim(a, b):
    cos_sim = dot(a, b)/(linalg.norm(a)*linalg.norm(b))
    return cos_sim

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

