# Import required modules
import os
import json
import nltk
import pandas as pd
from tqdm import tqdm
from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import RegexpTokenizer
from os import path
import sys
import time

def patternMatch(p, s):
    p = " " + p
    s = " " + s
    p_len = len(p)
    s_len = len(s)
    dp = [[False for j in range(p_len)] for i in range(s_len)]
    dp[0][0] = True
    for i in range(1, p_len):
        if p[i] == '*':
            dp[0][i] = dp[0][i-1]
    for i in range(1, s_len):
        for j in range(1, p_len):
            if s[i] == p[j] or p[j] == '?':
                dp[i][j] = dp[i-1][j-1]
            elif p[j] == '*':
                dp[i][j] = (dp[i-1][j] or dp[i][j-1])
    return dp[s_len-1][p_len-1]

def minimumEditDistance(s1, s2):
    if len(s1) == 0:
        return len(s2)
    if len(s2) == 0:
        return len(s1)
    m = len(s1)
    n = len(s2)
    dp = [[0 for j in range(n+1)] for i in range(m+1)]
    for i in range(m+1):
        for j in range(n+1):
            if i == 0:
                dp[i][j] = j
            elif j == 0:
                dp[i][j] = i
            elif s1[i-1] == s2[j-1]:
                dp[i][j] = dp[i-1][j-1]
            else:
                dp[i][j] = 1 + min(dp[i][j-1], dp[i-1][j], dp[i-1][j-1])
    return dp[m][n]



def getWildCardMatches(query_term, permuterm_index, document_list, wildcard_tokenizer, posting_list):
    # Get all the segments of the wildcard query term
    wildcard_segments = wildcard_tokenizer.tokenize(query_term)
    # Get all the terms that have the wildcard segment as a substring
    possible_snl_matches = []
    for wildcard_segment in wildcard_segments:
        if wildcard_segment in permuterm_index.keys():
            possible_snl_matches.extend(permuterm_index[wildcard_segment])

    # Get the matches that have all the wildcard segments as a substring
    possible_snl_matches_count = dict()
    for possible_snl_match in possible_snl_matches:
        if possible_snl_match in possible_snl_matches_count.keys():
            possible_snl_matches_count[possible_snl_match] = possible_snl_matches_count[possible_snl_match] + 1
        else:
            possible_snl_matches_count[possible_snl_match] = 1
    best_possible_snl_matches = []
    for possible_snl_match in possible_snl_matches_count.keys():
        if possible_snl_matches_count[possible_snl_match] == len(wildcard_segments):
            best_possible_snl_matches.append(possible_snl_match)

    # Get the exact matches to the wildcard query
    exact_snl_matches = []
    for best_possible_snl_match in best_possible_snl_matches:
        if patternMatch(query_term, best_possible_snl_match):
            exact_snl_matches.append(best_possible_snl_match)

    print("\nSearching", exact_snl_matches, "instead of", query_term, "\n")
    for snl_word in exact_snl_matches:
        document_list.extend(posting_list[snl_word])
    return document_list
    
def getNormalMatches(stemmer, lemmatizer, query_term, document_list, posting_list, bigram_index):
    snl_query_term = stemmer.stem(lemmatizer.lemmatize(query_term))
    # If the query term exists in the vocabulary
    if snl_query_term in posting_list.keys():
        document_list.extend(posting_list[snl_query_term])
    # If the query is not in the vocabulary, look for closest alternatives
    else:
        # Get bigrams of the query term
        bigrams = [''.join(bigram) for bigram in nltk.bigrams(snl_query_term)]
        # Get all possible alternatives terms with atleast one matching bigram
        alt_terms = set()
        for bigram in bigrams:
            if bigram in bigram_index.keys():
                for alt_term in bigram_index[bigram]:
                    alt_terms.add(alt_term)
        # Get best alternative terms based on minimum edit distance
        best_alt_terms = []
        min_edit_dist = 100
        for alt_term in alt_terms:
            edit_dist = minimumEditDistance(alt_term, snl_query_term)
            if edit_dist == min_edit_dist:
                best_alt_terms.append(alt_term)
            elif edit_dist < min_edit_dist:
                min_edit_dist = edit_dist
                best_alt_terms = [alt_term]
        print("\nSearching", best_alt_terms, "instead of", snl_query_term, "\n")
        # Query documents using the best alternatives
        for alt_term in best_alt_terms:
            document_list.extend(posting_list[alt_term])
    return document_list
