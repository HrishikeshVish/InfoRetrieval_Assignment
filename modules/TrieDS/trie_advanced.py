import copy


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


class InvalidDataNodeStructure(Exception):
    """
        Raised when string length is different from expected
    """

    def __init__(self, dn, message="Invalid Structure try something else or use your brain"):
        self.dn = dn
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f'{self.dn} -> {self.message}'


def _list_diff(li1, li2):
    s1 = set(li1)
    s2 = set(li2)
    li_dif = []
    for i in s1:
        if i not in s2:
            li_dif.append(i)
    return li_dif


def _dict_merge(a, b):
    """
    """
    d = copy.deepcopy(a)
    for i in b.keys():
        if i in d.keys():
            for j in b[i]:
                if j not in d[i]:
                    d[i].append(copy.deepcopy(j))
        else:
            d[i] = copy.deepcopy(b[i])
    return d


class Trie:
    """
    docstring
    """

    def __init__(self):
        self.__data_node = dict()

    @staticmethod
    def __is_valid_dn(dn):
        if type(dn) != dict:
            return False

        for i in dn.keys():
            if type(i) != str:
                return False
            if type(dn[i][0]) != Trie:
                return False
        return True

    @property
    def data_node(self):
        return self.__data_node.copy()

    @data_node.setter
    def data_node(self, dn):
        if self.__is_valid_dn(dn):
            self.__data_node = dn
        else:
            raise InvalidDataNodeStructure(dn)

    def add_string(self, string, doc):
        """
            Add index to the data structure
        """

        if len(string) < 1:
            raise IrregularStringLength(string=string)
        _first_char = string[0]
        if _first_char in self.__data_node.keys():
            self.__data_node[_first_char][1].append(doc)
            if len(string) > 1:
                self.__data_node[_first_char][0].add_string(string[1:], doc)
        else:
            self.__data_node[_first_char] = [Trie(), [doc]]
            if len(string) > 1:
                self.__data_node[_first_char][0].add_string(string[1:], doc)

    def search(self, string):
        """
        """
        if len(string) < 1:
            raise IrregularStringLength(string)

        _first_char = string[0]
        # print(string)
        if len(string) == 1:
            if _first_char in self.__data_node.keys():
                pos = copy.deepcopy(self.__data_node[_first_char][1])
                tmp = self.__data_node[_first_char][0].__data_node
                for i in pos:
                    for j in tmp.keys():
                        if i in tmp[j][1]:
                            pos.remove(i)
                return pos
            if _first_char == '*':
                res = []
                # print("lol")
                for i in self.__data_node.keys():
                    res = list(set(res+self.__data_node[i][1]))
                return copy.deepcopy(res)
        elif len(string) == 2 and string[-1] == "*":
            if _first_char in self.__data_node.keys():
                return copy.deepcopy(self.__data_node[_first_char][1])
        else:
            if _first_char == '*':
                res = self.search(string[1:])
                for i in self.__data_node.keys():
                    res = list(set(res+self.__data_node[i][0].search(string)))
                return copy.deepcopy(res)
            if _first_char in self.__data_node.keys():
                return self.__data_node[_first_char][0].search(string[1:])
        return []

    def merge(self, trie):
        """
        """
        assert(type(trie) == Trie)
        dn = trie.data_node
        for i in dn.keys():
            if i in self.__data_node.keys():
                self.__data_node[i][1] = list(
                    set(self.__data_node[i][1] + dn[i][1]))
                self.__data_node[i][0].merge(dn[i][0])
            else:
                self.__data_node[i] = copy.deepcopy(dn[i])

    def to_dict(self):
        """
        """
        if not self.__data_node:
            return {}
        req_dict = {}
        for i in self.__data_node.keys():
            req_dict[i] = [self.__data_node[i]
                           [0].to_dict(), copy.deepcopy(self.__data_node[i][1])]
        return req_dict

    def from_dict(self, trie_dict):
        """
        """
        if not trie_dict:
            self.__data_node = {}
            return

        for i in trie_dict.keys():
            new_trie = Trie()
            new_trie.from_dict(trie_dict[i][0])
            self.__data_node[i] = [new_trie, [int(jj) for jj in trie_dict[i][1]]]




def merge(a, b):
    """
        Merge two trie
    """
    assert(type(a) == Trie and type(b) == Trie)
    dn_1 = a.data_node
    dn_2 = b.data_node
    dn_3 = {}

    # copy
    dn_3 = copy.deepcopy(dn_1)

    for i in dn_2.keys():
        if i in dn_3.keys():
            dn_3[i][1] = list(set(dn_3[i][1] + dn_2[i][1]))
            dn_3[i][0] = merge(dn_3[i][0], dn_2[i][0])
        else:
            dn_3[i] = copy.deepcopy(dn_2[i])
    c = Trie()
    c.data_node = dn_3
    return c
