from create_final_fst import create_FST
import pickle

dict = []
with open("/usr/share/dict/american-english", "r") as file:
    for line in file:
        for word in line.split():
            dict.append(word)

output_list = [x for x in range(len(dict))]
t = create_FST(dict, output_list)

file_fst = open('fullfst.obj', 'wb')
pickle.dump(t, file_fst)