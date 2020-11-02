import os
import nltk
from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer
import nltk


def LCS(strA, strB):
    revA = strA[::-1]
    revB = strB[::-1]
    reversed_lcs = os.path.commonprefix([revA, revB])
    lcsa = reversed_lcs[::-1]
    return lcsa

def buildArray(inStr):
    Len = len(inStr)
    suffixArray = {}
    for i in range(Len):
        suffixArray[i] = inStr[i:]
    sA = {k: v for k, v in sorted(suffixArray.items(), key=lambda item: item[1])}

    return sA, list(sA.keys())
def find(search, inputStr, suford, Len):
    patLen = len(search)
    foundIndices = []
    left = 0
    right = Len - 1
    for i in range(Len):
        if(suford[i] + patLen <=Len):
            result = 0
            for j in range(patLen):
                if(inputStr[suford[i]+j] != search[j]):
                    result = -1
                    break
            result = inputStr[suford[i]:].startswith(search)
            if(result == 1):
                foundIndices.append(suford[i])
    return foundIndices
def findLCS(sub, s, suford, Len):
    patLen = len(sub)
    foundIndices = []
    left = 0
    right = Len - 1
    for i in range(Len):
        if(suford[i] + patLen <=Len):
            result = 0
            for j in range(patLen):
                if(s[suford[i]+j] != sub[j]):
                    result = -1
                    break
            result = s[suford[i]:].startswith(sub)
            if(result == 1):
                foundIndices.append(suford[i])
    if(len(foundIndices) == 0):
        return -1
    foundIndices = sorted(foundIndices)
    return foundIndices

    
def findDoc(documents, search):
    invertedIndex = {}
    partialIndex = {}
    suford = []
    n = len(documents)
    LCSArray = []
    out1 = []
    for i in range(n):
        suffixArray, suford = buildArray(documents[i]) 
        inout = -1
        in1 = documents[i]
        found = find(search, in1, suford, len(in1)) # Number of full matches
        if(len(found) !=0):
            found = sorted(found)
            invertedIndex[i] = found
            out1.append(found)
        else:
            # Partial Matches
            s1_offset = i
            patLen = len(search)
            stemp = document[i]
            longest = LCS(stemp, search)
            if(len(longest) == 0):
                s1_start = []
                s1_len = 0
            else:
                sp = longest
                inout = findLCS(sp, documents[i], suford, len(documents[i]))
                s1_len = len(longest)
                s1_start = inout
            
            if(len(LCSArray) == 0 and len(longest)>0):
                LCSArray.append(longest)
            if(len(LCSArray) !=0 and len(LCSArray[0])< len(longest)):
                LCSArray[0] = longest
            partialIndex[i] = longest
                
            
    if(len(LCSArray) == 0 and len(out1) == 0):
        invertedIndex = {}
        invertedIndex[-1] = -1
        return invertedIndex
    if(len(out1) !=0):
        return invertedIndex
    else:
        return partialIndex
def buildIndex(documents):
    invertedIndex = {}
    for i in range(len(documents)):
        print(i)
        words = documents[i].split(" ")
        for j in words:
            if j not in invertedIndex:
                invertedIndex[j] = []
            if i not in invertedIndex[j]:
                invertedIndex[j].append(i)
    return invertedIndex

def preProcess(documents):
    porter = PorterStemmer()
    lemmatizer = WordNetLemmatizer()
    for i in range(len(documents)):
        stemmed = []
        words = documents[i].split(" ")
        for j in words:
            stemmed.append(porter.stem(lemmatizer.lemmatize(j)))
        print(stemmed)

def generateBiWordIndex(searchTerm):
    bigrm = list(nltk.bigrams(searchTerm.split()))
    print(*map(' '.join, bigrm), sep=", ")
    
        
#print(findDoc(["""He is still unconscious following his ordeal, but he will awaken soon and retake control of the Fowl finances""", """However, there is time for one last job. Something that my mother would not approve of. I don't think the fairy folk would like it much either. So I shall not"""], "is"))
                
#print(preProcess(["""He is still unconscious following his ordeal, but he will awaken soon and retake control of the Fowl finances""", """However, there is time for one last job. Something that my mother would not approve of. I don't think the fairy folk would like it much either. So I shall not"""]))         
            
#generateBiWordIndex("Could you be there cause I'm the one who waits for you, or are you unforgiven too")  
#print(LCS("Hweorjweorjoiabcde", "dowjdowedjwiedoAAcde"))
