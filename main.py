from trie import *
from tkinter import *
from levenshtein import *
import pickle
from create_final_fst import *
from fst_lib2 import *

fst_file_read = open('fullfst.obj', 'rb')
t = pickle.load(fst_file_read)

#trie_file_read = open('fulltrie.obj', 'rb')
#t = pickle.load(trie_file_read)

dict_file_read = open('dict.obj', 'rb')
dict = pickle.load(dict_file_read)

#dict = ["add","added", "addeds", "adder"]
#output_list = [x for x in range(len(dict))]
#t = create_FST(dict, output_list)

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
