import time
import tracemalloc
from fst_lib2 import *
from create_final_fst import *
from trie import *

dict = []
with open("/usr/share/dict/american-english", "r") as file:
    for line in file:
        for word in line.split():
            dict.append(word)

def compare_autocomplete():
    fst_file_read = open('fullfst.obj', 'rb')
    fst = pickle.load(fst_file_read)

    trie_file_read = open('fulltrie.obj', 'rb')
    trie = pickle.load(trie_file_read)

    words_test = ["car", "house", "askakdc", "Monday", "avocado"]
    start = time.perf_counter()
    for word in words_test:
        fst.findSuggestions(word, dict)
    end = time.perf_counter()
    fst_time = (end - start)/5

    start = time.perf_counter()
    for word in words_test:
        trie.findSuggestions(word, dict)
    end = time.perf_counter()
    trie_time = (end - start) / 5

    print("Tempo da FST: ", fst_time)
    print("Tempo da Trie: ", trie_time)


def compare_memory():
    tracemalloc.start()
    output_list = [x for x in range(len(dict))]
    fst = create_FST(dict, output_list)
    fst_size = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    tracemalloc.start()
    trie = Trie()
    trie.formTrie(dict)
    trie_size = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    print("Memória usada pela FST: ", fst_size, " com ", fst.node_counter, " nós utilizados")
    print("Memória usada pela Trie: ", trie_size, " com ", trie.node_counter, " nós utilizados")


def compare_index():
    start = time.perf_counter()
    output_list = [x for x in range(len(dict))]
    fst = create_FST(dict, output_list)
    end = time.perf_counter()
    fst_time = end - start

    start = time.perf_counter()
    trie = Trie()
    trie.formTrie(dict)
    end = time.perf_counter()
    trie_time = end - start

    print("Tempo total de criação da FST: ", fst_time, " e tempo por índice: ", fst_time/len(dict))
    print("Tempo total de criação da Trie: ", trie_time, " e tempo por índice: ", trie_time/len(dict))

compare_index()
