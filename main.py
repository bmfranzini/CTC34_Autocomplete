from trie import *
from tkinter import *
from levenshtein import *
import pickle
from create_final_fst import *
from fst_lib2 import *

trie_file_read = open('fullfst.obj', 'rb')
t = pickle.load(trie_file_read)

dict = []
with open("/usr/share/dict/american-english", "r") as file:
    for line in file:
        for word in line.split():
            dict.append(word)
# dict = ["mon", "thurs", "tues", "tye"]
# output_list = [x for x in range(len(dict))]
# t = create_FST(dict, output_list)

# for state in t.states:
#     print("------------------inicio do estado------------------")
#     if state.type == FINAL_STATE:
#         print("ESTADO FINAL")
#     for edge in state.outgoing_edges:
#         print(edge.on_symbol)
#     print("------------------final do estado--------------------")
#t = Trie()
#t.formTrie(["b", "hel", "hell", "hello", "help", "a"])
#print(t.root.children[0].children[0].children[0].children[0].children[0].last)

window = Tk()
window.geometry("300x200+10+10")
lbl = Label(window, text="Digite uma palavra", font=("Arial", 16))
lbl.place(x=60, y=10)
v = StringVar()
entry = Entry(window, font = ('Arial', 10), textvariable=v)
entry.place(x=80, y=50)

global lev
lev = False

words_lev = []
word = ""

def get_word(*args):
    labels = [None] * (10)
    for i in range(0, 10):
        labels[i] = Label(window, text="                     ", font=("Arial", 10))
        labels[i].place(x=80, y=75 + 20 * i)

    palavra = v.get()
    word = palavra
    sugestions = []
    sugestions = t.findSuggestions(palavra, dict)
    words_lev = sugestions

    matches = []
    sparse = SparseLevenshteinAutomaton(word, 1)

    for query in words_lev:
        s_sparse = sparse.start()
        for c in query:
            s_sparse = sparse.step(s_sparse, c)
            if not sparse.can_match(s_sparse):
                break
        if sparse.is_match(s_sparse):
            matches.append(query)


    num_sugest = 10
    if len(sugestions) < num_sugest:
        num_sugest = len(sugestions)

    for i in range(0,num_sugest):
        if sugestions[i] != palavra and (sugestions[i] in matches):
            labels[i].config(text=sugestions[i] + "               ", fg='red')
        else:
            labels[i].config(text=sugestions[i] + "               ", fg='black')


v.trace('w', get_word)
window.mainloop()
