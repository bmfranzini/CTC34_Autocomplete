from trie import *
import pickle

dict = []
with open("/usr/share/dict/american-english", "r") as file:
    for line in file:
        for word in line.split():
            dict.append(word)

trie = Trie()
trie.formTrie(dict)

file_trie = open('fulltrie.obj', 'wb')
pickle.dump(trie, file_trie)
