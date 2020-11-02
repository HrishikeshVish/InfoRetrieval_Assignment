################################################################### NOT TO BE USED ###################################################################
def generate_corpus():
    # Import required modules
    import os
    import pandas as pd
    
    # Get list of files in dataset
    dataset_path = './TelevisionNews'
    dataset_files_list = os.listdir(dataset_path)

    # Create a corpus dafaframe to store the combined corpus
    column_headers = set(['URL', 'MatchDateTime', 'Station', 'Show', 'IAShowID', 'IAPreviewThumb', 'Snippet'])
    corpus = pd.DataFrame({'URL' : [], 'MatchDateTime' : [], 'Station' : [], 'Show' : [], 'IAShowID' : [], 'IAPreviewThumb' : [], 'Snippet' : []})

    # Iterate through each file in the dataset and create a combined corpus
    for file_id in range(len(dataset_files_list)):
        try:
            # Read contents of each file in the dataset and check if comforms to the required format
            partial_corpus = pd.read_csv('./TelevisionNews/' + dataset_files_list[file_id])
            if not partial_corpus.empty and (set(partial_corpus.columns.values) == column_headers):
                # Append the contents of the file to the combines corpus dataframe
                corpus = corpus.append(partial_corpus, ignore_index=True)
        except pd.errors.EmptyDataError:
            continue
    
    # Save the combined corpus dataframe to one csv file
    corpus.to_csv('./corpus.csv', index=False)

def generate_snl_corpus():
    # Import required modules
    import pandas as pd
    from nltk.stem import PorterStemmer
    from nltk.stem import WordNetLemmatizer
    from nltk.tokenize import RegexpTokenizer

    # Dowload the wordnet corpus for nltk
    import nltk
    nltk.download('wordnet')

    # Read the combined corpus into a dataframe
    corpus = pd.read_csv('./corpus.csv')

    # Empty list to store the stemmed and lemmatized corpus
    snl_snippets = []

    # Declare the Stemmer, Lemmatizer and Tokenizer
    stemmer = PorterStemmer()
    lemmatizer = WordNetLemmatizer()
    tokenizer = RegexpTokenizer(r'\w+')

    # Generate the stemmed and lemmatized corpus
    for snippet in corpus['Snippet']:
        snl_snippet = []
        # Stem and Lemmatize each token in the snippet
        for word in tokenizer.tokenize(snippet.lower()):
            snl_snippet.append(stemmer.stem(lemmatizer.lemmatize(word)))
        snl_snippets.append(snl_snippet)
    
    # Combine the data stemmed and lemmatized corpus to the whole original corpus
    snl_corpus = corpus
    snl_corpus['S&LSnippet'] = snl_snippets

    # Save the full stemmed and lemmatized corpus to one csv file
    snl_corpus.to_csv('./snl_corpus.csv', index=False)

######################################################################################################################################################

################################################################### TO BE USED #######################################################################

def generate_intermediate_corpus():
    # Import required modules
    import os
    import pandas as pd
    from nltk.stem import PorterStemmer
    from nltk.stem import WordNetLemmatizer
    from nltk.tokenize import RegexpTokenizer

    # Dowload the wordnet corpus for nltk
    import nltk
    nltk.download('wordnet')

    # Declare the Stemmer, Lemmatizer and Tokenizer
    stemmer = PorterStemmer()
    lemmatizer = WordNetLemmatizer()
    tokenizer = RegexpTokenizer(r'\w+')

    # Get list of files in dataset
    corpus_path = './TelevisionNews'
    corpus_files_list = os.listdir(corpus_path)

    # Initialize intermediate corpus data
    snl_snippets = []
    row_numbers = []
    file_names = []

    # Iterate through each file in the dataset and create a combined corpus
    for file_name in corpus_files_list:
        try:
            # Read contents of each file in the dataset and check if comforms to the required format
            partial_corpus = pd.read_csv('./TelevisionNews/' + file_name)
            if 'Snippet' in partial_corpus.columns:
                for row_number in range(len(partial_corpus['Snippet'])):
                    snl_snippet = []
                    snippet = partial_corpus['Snippet'][row_number]
                    # Stem and Lemmatize each token in the snippet
                    for word in tokenizer.tokenize(snippet.lower()):
                        snl_snippet.append(stemmer.stem(lemmatizer.lemmatize(word)))
                    # Append to the intermediate corpus data
                    snl_snippets.append(snl_snippet)
                    row_numbers.append(row_number)
                    file_names.append(file_name)
        except pd.errors.EmptyDataError:
            continue
    
    # Save the full intermediate corpus to one csv file
    intermediate_corpus = pd.DataFrame({'snl_snippets' : snl_snippets, 'row_numbers' : row_numbers, 'file_names' : file_names})
    intermediate_corpus.to_csv('./intermediate_corpus.csv', index=False)

######################################################################################################################################################

generate_intermediate_corpus()