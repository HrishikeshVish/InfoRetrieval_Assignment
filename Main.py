from search import search
from pageRanking import rankByFreq, rankByTFIDF
query = input("Enter the search term")
document_list = search(query)
ranked_order_of_docs = rankByFreq(document_list)
rankByTFIDF(ranked_order_of_docs, 5, query)

