
class IrregularStringLength(Exception):
    """
        Raised when string length is different from expected
    """
    def __init__(self, string, message="String length is 0"):
        self.string = string
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f'{self.string} -> {self.message}'



def _dict_merge(a,b):
    """
    """
    d = {}
    for i in a.keys():
        d[i] = a[i]
    for i in b.keys():
        if i in d.keys():
            d[i] += b[i]
        else:
            d[i] = b[i]
    return d




class Trie:
    """
    docstring
    """
    def __init__(self):
        self.__data_node = dict()
        
    def add_string(self, first_char, string, doc_id, row, pos):
        """
            Add index to the data structure
        """
        if len(first_char) != 1:
            raise IrregularStringLength(string=first_char, message="first_char length is not 1")

        if first_char in self.__data_node.keys():
            if doc_id in self.__data_node[first_char][1].keys():
                self.__data_node[first_char][1][doc_id].append([row, pos])
            else:
                self.__data_node[first_char][1][doc_id] = [[row, pos]]
            if len(string) > 0:
                self.__data_node[first_char][0].add_string(string[0], string[1:], doc_id, row, pos)
            elif first_char != "*":
                self.__data_node[first_char][0].add_string("*", "", doc_id, row, pos)
        else:
            self.__data_node[first_char] = (Trie(), {doc_id: [[row, pos]]})
            if len(string) > 0:
                self.__data_node[first_char][0].add_string(string[0], string[1:], doc_id, row, pos)
            elif first_char != "*":
                self.__data_node[first_char][0].add_string("*", "", doc_id, row, pos)
        
        if first_char != "*":
            if '*' in self.__data_node.keys():
                if doc_id in self.__data_node['*'][1].keys():
                    self.__data_node['*'][1][doc_id].append([row, pos])
                else:
                    self.__data_node['*'][1][doc_id] = [[row, pos]]
                if len(string) > 0:
                    self.__data_node['*'][0].add_string(string[0], string[1:], doc_id, row, pos)
                
            else:
                self.__data_node['*'] = (Trie(), {doc_id: [[row, pos]]})
                if len(string) > 0:
                    self.__data_node['*'][0].add_string(string[0], string[1:], doc_id, row, pos)

    def getdn(self):
        return self.__data_node

    

    def search(self, string):
        """
        """
        if len(string) < 1 :
            raise IrregularStringLength(string)
        
        _first_char = string[0]
        if len(string) == 1:
            if _first_char in self.__data_node.keys():
                if _first_char != '*':
                    pos = self.__data_node[_first_char][1]
                    extra = {}
                    if '*' in self.__data_node['*'][0].__data_node.keys():
                        extra = self.__data_node['*'][0].__data_node['*'][1]
                    for i in extra.keys():
                        if i in pos.keys():
                            pos.pop(i)
                    return pos
                return self.__data_node[_first_char][1]
        else:
            if _first_char in self.__data_node.keys():
                if _first_char == '*':
                    pos_star = self.__data_node[_first_char][0].search(string)
                    pos_char1 = self.search(string[1:])
                    pos_char2 = self.__data_node[_first_char][0].search(string[1:])
                    return _dict_merge(pos_star, _dict_merge(pos_char1, pos_char2))
                else:
                    return self.__data_node[_first_char][0].search(string[1:])
        
        return {}

