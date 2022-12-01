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
        self.contador = 1

    def formTrie(self, keys):
        for key in keys:
            self.insert(key)

    def insert(self, key):
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
        self.contador = self.contador + 1
        node.idx = self.contador

    def suggestionsRec(self, node, word, sugestions):
        if node.last:
            sugestions.append(word)

        for a, n in node.children:
            self.suggestionsRec(n, word + a, sugestions)

    def printAutoSuggestions(self, key, sugestions):
        node = self.root
        for a in key:
            aux = False
            for children in node.children:
                if children.char == a:
                    aux = True
                    node = children
                    break

            if not aux:
                return

        if not node.children:
            return -1

        self.bfs(node, sugestions)

    def bfs(self, node, sugestions):
        vertice_fonte = node
        fila = []
        fila.extend(vertice_fonte.children)
        while fila:
            vertice = fila.pop(0)
            if vertice.last:
                p = vertice
                palavra = ''
                while p.parent is not None:
                    palavra = p.char + palavra
                    p = p.parent
                sugestions.append(palavra)
            fila.extend(vertice.children)


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