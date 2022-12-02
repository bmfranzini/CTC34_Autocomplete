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
        #self.src.add_outgoing_edge(self)
    
    def transit(self, ip):
        return (self.dest, self.op) if self.on_symbol == ip else None
    #def __repr__(self):
        #return (self.src, self.dest, self.on_symbol, self.op).__repr__()
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
            #new_edge = Edge(self, edge.dest, edge.on_symbol, edge.op)
            
    def create_edge(self, state, on_symbol, output):
        new_edge = Edge(self, state, on_symbol, output)
        self.outgoing_edges.append(new_edge)

    def set_output(self, c, num):
        for edge in self.outgoing_edges:
            if edge.on_symbol == c:
                edge.op = num
    
    def output(self, c):
        for edge in self.outgoing_edges:
            if edge.on_symbol == c:
                return edge.op
        return None
    """
    def word_set(self):
        state_set = set()
        for edge in self.outgoing_edges:
            for word in edge.dest.word_set():
                #if word != '':
                state_set = state_set.union({edge.on_symbol + word})
                #else:
                    #state_set = {edge.on_symbol}
            if edge.dest.word_set() == set():
                state_set = {edge.on_symbol}
        print(state_set)
        return state_set
    """
    def add_outgoing_edge(self, edge):
        assert isinstance(edge, Edge), 'Outgoing Edge must be an instance of Edge.'
        self.outgoing_edges.append(edge)
    
    def del_edge(self, state): # revisar para checar tbm transicao
        for edge in self.outgoing_edges:
            if edge.dest == state:
                #print(f"Tirando aresta de char {edge.on_symbol}")
                self.outgoing_edges.remove(edge)
    def output_to_state(self, state): # revisar para checar tbm transicao
        for edge in self.outgoing_edges:
            if edge.dest == state:
                return edge.op
        return 0
    #def transit(self, ip_char):
        #return [oe.transit(ip_char) for oe in self.outgoing_edges]
    
    def is_final_state(self):
        return self.type == FINAL_STATE
    
    """
    def __eq__(self, oth):
        #if isinstance(oth, str):
            #return oth == self.name
        #return self.name == oth.name
        #checar se o numero de arestas é igual
        if isinstance(oth, State):
            #print(self.word_set())
            return (self.type == oth.type) and (len(self.outgoing_edges) == len(oth.outgoing_edges)) and (self.word_set() == oth.word_set())
        return False
    """
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
            #if state_edge not in self.outgoing_edges:
                #return False
            
            #if not (state_edge.dest in [edge.dest for edge in self.outgoing_edges]):
                #return False
        return True
    #def __hash__(self):
        #return self.name.__hash__()


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