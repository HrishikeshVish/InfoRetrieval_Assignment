from modules import Trie
from modules.TrieDS import merge
from modules import InvertedIndex
from nltk import tokenize
from nltk.tokenize import RegexpTokenizer
_tokenizer = RegexpTokenizer(r'[^\W_]+')

def print_trie(t,c):
    dd = t.getdn()
    for i in dd.keys():
        print(" "*c, i, dd[i][1])
        print_trie(dd[i][0], c+1)



############### ADD TOKEN TEST ###############

# def main():
#     a = Trie()
#     s = """There was something in the tree. 
#     It was difficult to tell from the ground, but Rachael could see movement. 
#     She squinted her eyes and peered in the direction of the movement, 
#     trying to decipher exactly what she had spied. The more she peered, however, 
#     the more she thought it might be a figment of her imagination. Nothing seemed 
#     to move until the moment she began to take her eyes off the tree. Then in the corner of her eye, 
#     she would see the movement again and begin the process of staring again."""
#     b = tokenize.word_tokenize(s)
#     for i in range(len(b)):
#         a.add_string(b[i][0], b[i][1:], i, i, i)
#     print_trie(a, 0)

###############################################






############### SEARCH TEST ###############

# def main():
#     from json import dumps
#     a = Trie()
#     s = """There was something in the tree. 
#     It was difficult to tell from the ground, but Rachael could see movement. 
#     She squinted her eyes and peered in the direction of the movement, 
#     trying to decipher exactly what she had spied. The more she peered, however, 
#     the more she thought it might be a figment of her imagination. Nothing seemed 
#     to move until the moment she began to take her eyes off the tree. Then in the corner of her eye, 
#     she would see the movement again and begin the process of staring again."""
#     # s = "trree trrees trreesss tre tre"
#     # s = "BBC News BBC Newsroom"
#     # s = "staring she"
#     b = tokenize.word_tokenize(s)
#     print(b)
#     t = "*re*"
#     print(len(b))
#     for i in range(len(b)):
#         # if b[i].count("re")> 0:
#         #     print(i, b[i])
#         a.add_string(b[i], i)
#     f = open("lol.json", "w")
#     f.write(dumps(a.to_dict()))
#     f.close()
#     # print_trie(a, 0)
#     # print(a.getdn()['*'])
#     ans = a.search(t)
#     print(ans)
#     for i in ans:
#         print(b[i])
#     # for i in ans.keys():
#     #     for j in ans[i]:
#     #         print(b[j], j)

##########################################






############### MERGE TEST ###############

# def main():
#     a1 = Trie()
#     a2 = Trie()
#     s1 = """There was something in the tree. 
#     It was difficult to tell from the ground, but Rachael could see movement. 
#     She squinted her eyes and peered in the direction of the movement, 
#     trying to decipher exactly what she had spied. The more she peered, however, 
#     the more she thought it might be a figment of her imagination. Nothing seemed 
#     to move until the moment she began to take her eyes off the tree. Then in the corner of her eye, 
#     she would see the movement again and begin the process of staring again."""
#     s2 = "trree trrees trreesss tre tre"
#     b = tokenize.word_tokenize(s1)
#     c = tokenize.word_tokenize(s2)
#     t = "*re*"
#     print(len(b))
#     for i in range(len(b)):
#         if b[i].count("re")> 0:
#             print(i, b[i])
#         if i % 2 == 0:
#             a1.add_string(b[i][0], b[i][1:], 0, i, i)
#         else:
#             a2.add_string(b[i][0], b[i][1:], 0, i, i)
#     for i in range(len(c)):
#         if c[i].count("re")> 0:
#             print(i, c[i])
#         if i % 2 == 0:
#             a1.add_string(c[i][0], c[i][1:], 1, i, i)
#         else:
#             a2.add_string(c[i][0], c[i][1:], 1, i, i)
#     ans1 = a1.search(t)
#     ans2 = a2.search(t)
#     a3 = merge(a1, a2)
#     ans3 = a3.search(t)
#     print(ans1)
#     print(ans2)
#     print(ans3)

###########################################






############### CLASS METHOD MERGE TEST ###############

# def main():
#     a1 = Trie()
#     a2 = Trie()
#     s1 = """There was something in the tree. 
#     It was difficult to tell from the ground, but Rachael could see movement. 
#     She squinted her eyes and peered in the direction of the movement, 
#     trying to decipher exactly what she had spied. The more she peered, however, 
#     the more she thought it might be a figment of her imagination. Nothing seemed 
#     to move until the moment she began to take her eyes off the tree. Then in the corner of her eye, 
#     she would see the movement again and begin the process of staring again."""
#     s2 = "trree trrees trreesss tre tre"
#     b = tokenize.word_tokenize(s1)
#     c = tokenize.word_tokenize(s2)
#     t = "*re*"
#     print(len(b))
#     for i in range(len(b)):
#         if b[i].count("re")> 0:
#             print(i, b[i])
#         if i % 2 == 0:
#             a1.add_string(b[i][0], b[i][1:], 0, i, i)
#         else:
#             a2.add_string(b[i][0], b[i][1:], 0, i, i)
#     for i in range(len(c)):
#         if c[i].count("re")> 0:
#             print(i, c[i])
#         if i % 2 == 0:
#             a1.add_string(c[i][0], c[i][1:], 1, i, i)
#         else:
#             a2.add_string(c[i][0], c[i][1:], 1, i, i)
#     ans1 = a1.search(t)
#     ans2 = a2.search(t)
#     a3 = merge(a1, a2)
#     ans3 = a3.search(t)
#     a1.merge(a2)
#     ans4 = a1.search(t)
#     print(ans1)
#     print(ans2)
#     print(ans3)
#     print(ans4)

###########################################################


# import pandas

# c = pandas.read_csv("/root/Documents/Project/archive/TelevisionNews/BBCNEWS.201701.csv")

# c.columns
# for i in c.columns:
#     print(c[i].to_list())


############### NON Lematized INVERTED INDEX ###############

# def main():
#     import datetime
#     from json import dumps
#     import time
#     import os
#     import gc
#     data_path = "/root/Documents/Project/archive/TelevisionNews/"
#     paths = [data_path+i 
#                 for i in os.listdir(data_path)]
#     # path = "data/lol.csv"
#     paths = sorted(paths)
#     a = datetime.datetime.now()
#     tt = InvertedIndex()
#     for i_path in range(len(paths)):
#         print(paths[i_path])
#         tt.from_csv(paths[i_path], i_path)
#         gc.collect()
#     # trie_s = create_inverted_index_on_csv(path, 0)
#     # print(tt.trie)
#     print(datetime.datetime.now()-a)
#     # time.sleep(600)
#     # f = open("lol.json", "w")
#     # f.write(dumps(test_trie.to_dict()))
#     # f.close()
#     tt.save("./")
#     # print(tt.trie.data_node)
#     a = datetime.datetime.now()
#     ans = tt.search("un*ed")
#     print(datetime.datetime.now()-a)
#     for i in ans.keys():
#         print(i, " : ", ans[i], "\n\n\n")

###########################################################


############### LOAD INVERTED INDEX ###############

def main():
    import datetime
    from json import dumps
    import time
    import os
    import gc

    # path = "data/lol.csv"
    # paths = sorted(paths)
    a = datetime.datetime.now()
    tt = InvertedIndex()
    tt.load("./")
    # trie_s = create_inverted_index_on_csv(path, 0)
    # print(tt.trie)
    print(datetime.datetime.now()-a)
    # time.sleep(600)
    # f = open("lol.json", "w")
    # f.write(dumps(test_trie.to_dict()))
    # f.close()
    # tt.save("./")
    # print(tt.trie.data_node)
    a = datetime.datetime.now()
    ans = tt.search("un*ed")
    print(datetime.datetime.now()-a)
    for i in ans.keys():
        print(i, " : ", ans[i], "\n\n\n")

########################################################



if __name__ == "__main__":
    main()

