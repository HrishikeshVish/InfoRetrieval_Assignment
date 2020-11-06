import pandas as pd
from SuffixSearch import buildIndex, generateBiWordIndex
def buildPostingList():
    intermediate_corpus = pd.read_csv('intermediate_corpus.csv')
    documents = intermediate_corpus['snl_snippets']
    print(len(documents))
    invIndex = buildIndex(documents)
    postingList = pd.DataFrame({'word':list(invIndex.keys()), 'List':list(invIndex.values())})
    postingList.to_csv('postingList.csv', index=False)
    return invIndex
print(buildPostingList())


    
    
    
