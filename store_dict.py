import pickle

dict = []
with open("/usr/share/dict/american-english", "r") as file:
    for line in file:
        for word in line.split():
            dict.append(word)

file_dict = open('dict.obj', 'wb')
pickle.dump(dict, file_dict)