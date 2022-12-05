INTITIAL_STATE = 1
FINAL_STATE = 2
NORMAL_STATE = 3
INITIAL_AND_FINAL_STATE = 4
EPSILON = 5


class Edge(object):
    def __init__(self, src, destination, on_symbol, output = 0):
        self.src = src
        self.dest = destination
        self.on_symbol = on_symbol
        self.op = output

    
    def transit(self, ip):
        return (self.dest, self.op) if self.on_symbol == ip else None

    def __eq__(self, oth):
        if isinstance(oth, Edge):
            return (self.on_symbol == oth.on_symbol) and (self.op == oth.op) and (self.src == oth.src) and (self.dest == oth.dest)
        return False


class State(object):
    def __init__(self, type, outgoing_edges = []):
        self.type = type
        self.outgoing_edges = outgoing_edges

    def clear_state(self):
        self.type = NORMAL_STATE
        self.outgoing_edges = []

    def copy_state(self, state):
        self.type = state.type
        self.outgoing_edges = []
        for edge in state.outgoing_edges:
            self.create_edge(edge.dest, edge.on_symbol, edge.op)
            
    def create_edge(self, state, on_symbol, output):
        new_edge = Edge(self, state, on_symbol, output)
        self.outgoing_edges.append(new_edge)

    def set_output(self, state, num):
        for edge in self.outgoing_edges:
            if edge.dest == state:
                edge.op = num
    
    def output(self, c):
        aux_edge = None
        max_op = 0
        for edge in self.outgoing_edges:
            if edge.on_symbol == c and edge.op >= max_op:
                aux_edge = edge
        return aux_edge.op

    def add_outgoing_edge(self, edge):
        assert isinstance(edge, Edge), 'Outgoing Edge must be an instance of Edge.'
        self.outgoing_edges.append(edge)
    
    def del_edge(self, state): # revisar para checar tbm transicao
        for edge in self.outgoing_edges:
            if edge.dest == state:
                self.outgoing_edges.remove(edge)
    def output_to_state(self, state): # revisar para checar tbm transicao
        for edge in self.outgoing_edges:
            if edge.dest == state:
                return edge.op
        return 0

    
    def is_final_state(self):
        return self.type == FINAL_STATE

    def is_equivalent(self, state):
        if (self.type != state.type):
            return False
        if (len(self.outgoing_edges) != len(state.outgoing_edges)):
            return False
        for state_edge in state.outgoing_edges:
            temp = False
            for edge in self.outgoing_edges:
                if (edge.on_symbol == state_edge.on_symbol) and (edge.dest == state_edge.dest) and (edge.op == state_edge.op) :
                    temp = True
            if not temp:
                return False
        return True

class FST(object):
    def __init__(self):
        self.states = []
        self.init_state = None
    
    def add_state(self, state_type = NORMAL_STATE, outgoing_edges = []):
        new_state = State(state_type, outgoing_edges)
        if new_state in self.states:
            raise ValueError('State already defined.')
        if state_type in (INTITIAL_STATE, INITIAL_AND_FINAL_STATE):
            if self.init_state is not None:
                raise ValueError('FST Cannot have more than one INITIAL_STATE.')
            self.init_state = new_state
        self.states.append(new_state)

    def define_initial(self, state):
        if state not in self.states:
            self.add_state(state)
        if self.init_state != None:
            self.states[self.states.index(self.init_state)].type = NORMAL_STATE
        self.states[self.states.index(state)].type = INTITIAL_STATE
        self.init_state = state

    def findSuggestions(self, key, dict):
        node = self.init_state
        idx_word = 0

        for i in range(len(key)):
            a = key[i]
            aux = False
            final = False
            for edge in node.outgoing_edges:
                if edge.on_symbol == a:
                    aux = True
                    if edge.dest.type == FINAL_STATE and i == len(key) - 1:
                        #final = True
                        #sugestions.append(key)
                        pass
                    if edge.dest.type != FINAL_STATE:
                        node = edge.dest
                        idx_word += edge.op
                    #break

            if not aux:
                print("A palavra nao é prefixo de nada no dicionário")
                return []

        if not node.outgoing_edges:
            return []
        sugestions = []
        #if final:
            #for edge in node.outgoing_edges:
                #if edge.on_symbol == key[-1]:
                    #sugestions.extend(self.bfs(edge.dest, idx_word, dict))
        #else:
        sugestions.extend(self.bfs(node, idx_word, dict))

        return sugestions

    def bfs(self, node, idx, dict):
        sugestions = []
        vertice_fonte = node
        fila = []

        for edge in vertice_fonte.outgoing_edges:
            fila.append((edge.dest, edge.op+idx))
        
        while fila:
            vertice = fila.pop(0)
            if vertice[0].type == FINAL_STATE:
                sugestions.append(dict[vertice[1]])
            for edge in vertice[0].outgoing_edges:
                fila.append((edge.dest, edge.op+vertice[1]))
        return sugestions