from src import Trie
from nltk import tokenize

def print_trie(t,c):
    dd = t.getdn()
    for i in dd.keys():
        print(" "*c, i, dd[i][1])
        print_trie(dd[i][0], c+1)


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




def main():
    a = Trie()
    s = """There was something in the tree. 
    It was difficult to tell from the ground, but Rachael could see movement. 
    She squinted her eyes and peered in the direction of the movement, 
    trying to decipher exactly what she had spied. The more she peered, however, 
    the more she thought it might be a figment of her imagination. Nothing seemed 
    to move until the moment she began to take her eyes off the tree. Then in the corner of her eye, 
    she would see the movement again and begin the process of staring again."""
    # s = "trree trrees trreesss tre tre"
    b = tokenize.word_tokenize(s)
    t = "*i*c*t*n"
    print(len(b))
    for i in range(len(b)):
        if b[i].count("ground")> 0:
            print(i, b[i])
        a.add_string(b[i][0], b[i][1:], i, i, i)
    # print_trie(a, 0)
    # print(a.getdn()['*'])
    ans = a.search(t)
    print(list(ans.keys()))




if __name__ == "__main__":
    main()

