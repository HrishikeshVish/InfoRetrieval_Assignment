def pattern_match(p, s):
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

def minimum_edit_distance(s1, s2):
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

def generate_artifacts():
    # Import required modules
    import os
    import json
    import nltk
    import pandas as pd
    from tqdm import tqdm
    from nltk.stem import PorterStemmer
    from nltk.stem import WordNetLemmatizer
    from nltk.tokenize import RegexpTokenizer

    # Dowload the wordnet corpus for nltk
    nltk.download('punkt')
    nltk.download('wordnet')

    # Declare the Stemmer, Lemmatizer and Tokenizer
    stemmer = PorterStemmer()
    lemmatizer = WordNetLemmatizer()
    tokenizer = RegexpTokenizer(r'[a|b|c|d|e|f|g|h|i|k|l|m|n|o|p|q|r|s|t|u|v|w|x|y|z]+')

    # Get list of files in dataset
    corpus_path = './TelevisionNews'
    corpus_files_list = os.listdir(corpus_path)

    print("Generating the Posting List")

    # Initialize Posting List as an empty Dictionary
    posting_list = dict()

    # Iterate through each file in the dataset and create a combined corpus
    for file_name in tqdm(corpus_files_list):
        try:
            # Read contents of each file in the dataset and check if comforms to the required format
            partial_corpus = pd.read_csv('./TelevisionNews/' + file_name)
            if 'Snippet' in partial_corpus.columns:
                for row_number in range(len(partial_corpus['Snippet'])):
                    snippet = partial_corpus['Snippet'][row_number]
                    # Iterate through each token in the snippet and update the posting list
                    for word in tokenizer.tokenize(snippet.lower()):
                        snl_word = stemmer.stem(lemmatizer.lemmatize(word))
                        document_id = file_name + ' ' + str(row_number)
                        if(snl_word in posting_list.keys()):
                            if(posting_list[snl_word][-1] != document_id):
                                posting_list[snl_word].append(document_id)
                        else:
                            posting_list[snl_word] = [document_id]

        except pd.errors.EmptyDataError:
            continue
    
    # Save the full posting list as a json file
    posting_list_file = open('./posting_list.json', 'w+')
    json.dump(posting_list, posting_list_file, indent=4)
    posting_list_file.close()
    print('Posting List Generated')

    print("Generating the Posting List")

    # Initialize the bigram_index as an empty dictionary
    bigram_index = dict()

    # Iterate through the vocabulary and generate the bigram index
    for snl_word in tqdm(posting_list.keys()):
        bigrams = [''.join(bigram) for bigram in nltk.bigrams(snl_word)]
        for bigram in bigrams:
            if(bigram in bigram_index.keys()):
                bigram_index[bigram].append(snl_word)
            else:
                bigram_index[bigram] = [snl_word]
    
    # Save the full bigram_index as a json file
    bigram_index_file = open('./bigram_index.json', 'w+')
    json.dump(bigram_index, bigram_index_file, indent=4)
    bigram_index_file.close()
    print('Bigram Index Generated')

def search():
    import os
    import sys
    import time
    import json
    import nltk
    import pandas as pd
    from nltk.stem import PorterStemmer
    from nltk.stem import WordNetLemmatizer
    from nltk.tokenize import RegexpTokenizer

    # Dowload the wordnet corpus for nltk
    nltk.download("punkt")
    nltk.download("wordnet")

    # Declare the Stemmer, Lemmatizer and Tokenizer
    stemmer = PorterStemmer()
    lemmatizer = WordNetLemmatizer()
    tokenizer = RegexpTokenizer(r'[a|b|c|d|e|f|g|h|i|k|l|m|n|o|p|q|r|s|t|u|v|w|x|y|z|?|\*]+')
    stemmer.stem(lemmatizer.lemmatize("sample done"))

    # Obtain the posting list and bigram index
    directory_file_list = os.listdir(".")
    if ("posting_list.json" not in directory_file_list) or ("bigram_index.json" not in directory_file_list):
        generate_artifacts()
    posting_list_file = open("./posting_list.json", "r")
    posting_list = json.loads(posting_list_file.read())
    bigram_index_file = open("./bigram_index.json", "r")
    bigram_index = json.loads(bigram_index_file.read())

    # Take input query
    query = input("Please enter the query string: ")
    
    start = time.time()

    # Get the desired documents list
    document_list = []
    for query_term in tokenizer.tokenize(query.lower()):
        # If query term is a wildcard query
        if "*" in query_term or "?" in query_term:
            matching_snl_words = []
            for snl_word in posting_list.keys():
                if pattern_match(query_term, snl_word):
                    matching_snl_words.append(snl_word)
            print("\nSearching", matching_snl_words, "instead of", query_term, "\n")
            for snl_word in matching_snl_words:
                document_list.extend(posting_list[snl_word])
        # If query term is a normal query
        else:
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
                # Get best alternative terms based on minumum edit distance
                best_alt_terms = []
                min_edit_dist = 100
                for alt_term in alt_terms:
                    edit_dist = minimum_edit_distance(alt_term, snl_query_term)
                    if edit_dist == min_edit_dist:
                        best_alt_terms.append(alt_term)
                    elif edit_dist < min_edit_dist:
                        min_edit_dist = edit_dist
                        best_alt_terms = [alt_term]
                print("\nSearching", best_alt_terms, "instead of", snl_query_term, "\n")
                # Query documents using the best alternatives
                for alt_term in best_alt_terms:
                    document_list.extend(posting_list[alt_term])
    
    # Get the number of satisfied query terms for each document
    query_term_match_count = dict()
    for document in document_list:
        if document in query_term_match_count.keys():
            query_term_match_count[document] = query_term_match_count[document] + 1
        else:
            query_term_match_count[document] = 1
    
    # Rank documents in order of number of query terms matched
    ranked_order_of_docs = []
    for document in query_term_match_count.keys():
        ranked_order_of_docs.append([query_term_match_count[document], document])
    ranked_order_of_docs = sorted(ranked_order_of_docs, reverse=True)

    end = time.time()

    print("Documents that are relevant to the search are:\n", ranked_order_of_docs, "\n")
    print("--- %0.5f seconds ---" % (end - start))

search()