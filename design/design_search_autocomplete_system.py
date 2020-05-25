import collections

class Node:
    __slots__ = ["children", "sentences"]
    def __init__(self):
        self.children = dict()
        self.sentences = set()

    def add(self, sentence):
        node = self
        for letter in sentence:
            child = node.children.get(letter)
            if child is None:
                child = Node()
                node.children[letter] = child
            node = child
            child.sentences.add(sentence)

class AutocompleteSystem:

    def __init__(self, sentences, times):
        self.__trie = Node()
        self._session_trie = None
        self.times = collections.defaultdict(int)
        self.history = ""
        for s, t in zip(sentences, times):
            self.times[s] = t
            self.__trie.add(s)
        self._session_trie = self.__trie
                
    def input(self, c: str):
        ret = []
        if c != '#':
            self.history += c
            if self._session_trie:
                node = self._session_trie.children.get(c)
                if node:
                    ret = sorted(node.sentences, key=lambda x: (-self.times[x], x))[:3]
                self._session_trie = node
        else:
            self.__trie.add(self.history)
            self.times[self.history] += 1
            self.history = ""
            self._session_trie = self.__trie
        return ret

    
if __name__ == "__main__":
    solution = AutocompleteSystem(["i love you","island","iroman","i love leetcode"],[5,3,2,2])
    assert solution.input("i") ==  ["i love you", "island","i love leetcode"]
    assert solution.input(" ") == ["i love you","i love leetcode"]
    assert solution.input("a") == []
    assert solution.input("#") == []
    print("---------")
    assert solution.input("i") ==  ["i love you", "island","i love leetcode"]
    assert solution.input(" ") == ['i love you', 'i love leetcode', 'i a']
    assert solution.input("a") == ["i a"]
    assert solution.input("#") == []
    print("---------")
    assert solution.input("i") ==  ["i love you", "island","i a"]
    assert solution.input(" ") == ['i love you', 'i a', 'i love leetcode']
    assert solution.input("a") == ["i a"]
    assert solution.input("#") == []
    solution = AutocompleteSystem(["abc","abbc","a"],[3,3,3])
    assert solution.input("b") == []
    assert solution.input("c") == []
    assert solution.input("#") == []
    assert solution.input("b") == ["bc"]
    assert solution.input("c") == ["bc"]
    assert solution.input("#") == []
    assert solution.input("a") == ["a","abbc","abc"]
    assert solution.input("b") == ['abbc', 'abc']
    assert solution.input("c") == ["abc"]
    assert solution.input("#") == []
    assert solution.input("a") == ['abc', 'a', 'abbc']
    assert solution.input("b") == ['abc', 'abbc']
    assert solution.input("c") == ["abc"]
    assert solution.input("#") == []