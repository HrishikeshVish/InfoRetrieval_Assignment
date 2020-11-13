from search import search
from pageRanking import rankByFreq, rankByTFIDF
query = input("Enter the search term")
document_list = search(query)
print(document_list)
ranked_order_of_docs = rankByFreq(document_list)
if "*" in query or "?" in query:
    ranked_docs = ranked_order_of_docs[0:10]
else:
    ranked_docs = rankByTFIDF(ranked_order_of_docs, 5, query)[0:10]


