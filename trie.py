import time
import tracemalloc


class TrieNode():
    def __init__(self):
        self.children = []
        self.last = False
        self.idx = -1
        self.char = ''
        self.parent = None


class Trie():
    def __init__(self):
        self.root = TrieNode()
        self.contador = 0

    def formTrie(self, keys):
        for i in range(len(keys)):
            self.insert(keys[i], i)

    def insert(self, key, index):
        node = self.root

        for a in key:
            filho = None
            aux = False
            for children in node.children:
                if children.char == a:
                    aux = True
                    filho = children
                    break
            if not aux:
                filho = TrieNode()
                filho.char = a
                filho.parent = node
                node.children.append(filho)

            node = filho
        node.last = True
        node.idx = index


    def findSuggestions(self, key, dict):
        node = self.root
        for a in key:
            aux = False
            for children in node.children:
                if children.char == a:
                    aux = True
                    node = children
                    break

            if not aux:
                print("A palavra nao é prefixo de nada no dicionário")
                return []

        if not node.children:
            return []

        return self.bfs(node, dict)

    def bfs(self, node, dict):
        vertice_fonte = node
        fila = []
        fila.extend(vertice_fonte.children)
        sugestions = []
        while fila:
            vertice = fila.pop(0)
            if vertice.last:
                sugestions.append(dict[vertice.idx])
            fila.extend(vertice.children)
        return sugestions


"""
keys = ["aula", "auuii", "auuiiiii", "auxt", "a"]
key = "aul"
sugestions = []

start = time.perf_counter()
tracemalloc.start()
t = Trie()
t.formTrie(keys)
comp = t.printAutoSuggestions(key, sugestions)

end = time.perf_counter()

if comp == -1:
    print("No other strings found with this prefix\n")
elif comp == 0:
    print("No string found with this prefix\n")

print("sugestions=", sugestions)
print("Tempo de execução = ", end - start)
print("Memória usada = ", tracemalloc.get_traced_memory())
tracemalloc.stop()
"""