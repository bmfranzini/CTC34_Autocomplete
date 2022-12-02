import fst_lib2 as fst

# defino as variáveis globais
t = fst.FST()

def find_minimized(state):
    # retorna um estado equivalente do dicionário. Se não estiver presente, insere uma cópia
    # do parâmetro no dicionário e o retorna
    global t
    for state_index in range(len(t.states)):
        if t.states[state_index].is_equivalent(state):
            print("Achei equivalente")
            return state_index
    new_state = fst.State(fst.NORMAL_STATE)
    new_state.copy_state(state) # acho que não precisa, já está sendo uma cópia
    print("Novo minimo")
    for edge in new_state.outgoing_edges:
        print(f'{edge.dest}  {edge.on_symbol}')
    t.states.append(new_state)
    #t.add_state(state.type, state.outgoing_edges)

    return len(t.states) - 1


def exists_transition(state, c): #equivale a função transition do pseudocódigo, mas retornando true ou false
    for edge in state.outgoing_edges:
        if edge.on_symbol == c:
            return True
    return False

def create_FST(input_list, output_list):
    temp_states = [] # lista com estados, do tamanho da maior palavra do dicionário
    for i in range(46):
        temp_states.append(fst.State(fst.NORMAL_STATE))
    previous_word = ''
    current_output = ''
    temp_states[0].clear_state()
    for i in range(len(input_list)):
        current_word = input_list[i]
        current_output = output_list[i]
        j = 0 # checar se é zero ou um
        # calculo tamanho do máximo prefixo comum entre current_word e previous_word
        while(j < len(current_word) and j < len(previous_word) and current_word[j] == previous_word[j]):
            j += 1
        prefix_len = j  # número máximo de letras do prefixo comum
        print(prefix_len)
        # minimizamos os estados do sufixo da última palavra
        for j in range(len(previous_word), prefix_len, -1):
            output = temp_states[j-1].output_to_state(temp_states[j])
            temp_states[j-1].del_edge(temp_states[j])
            temp_states[j-1].create_edge(t.states[find_minimized(temp_states[j])], previous_word[j-1], output)
            #new_edge = fst.Edge(temp_states[j-1], t.states[find_minimized(temp_states[j])], previous_word[j-1])
            temp_states[j].clear_state()
        
        for j in range((prefix_len)+1, len(current_word)):
            temp_states[j].clear_state()

        # inicializamos os estados do vetor para a palavra atual (considero apenas o sufixo, pois o resto já está inicializado)
        for j in range((prefix_len), len(current_word)):
            #clearstate
            #temp_states[j].clear_state()
            #new_edge = fst.Edge(temp_states[j], temp_states[j+1], current_word[j])
            temp_states[j].create_edge(temp_states[j+1], current_word[j], 0)
            #print("CRIANDO A EDGE QUE VAI DE ", temp_states[j], " para ", temp_states[j+1])
        # temp_states[len(current_word)].clear_state()
        if current_word != previous_word:
            temp_states[len(current_word)].type = fst.FINAL_STATE
        #j = 0
        #for state in temp_states[:len(current_word)+1]:
            #print("***************Estado de número ", i, "*****************")
            #for edge in state.outgoing_edges:
                #print("Símbolo: ", edge.on_symbol, "Indo de ", edge.src, " para ", edge.dest)
            #j += 1
        
        # encontramos o output da bifurcação
        prefix_output = 0
        for j in range(prefix_len):
            prefix_output += temp_states[j].output(current_word[j])
            print("PrefixOutput: ",prefix_output)
        new_output = current_output - prefix_output
        print('NewOutput', new_output)
        temp_states[prefix_len].set_output(current_word[prefix_len], new_output)
        
        previous_word = current_word
    
    # minimizamos os estados da última palavra
    for i in range(len(current_word), 0, -1):
        output = temp_states[i-1].output_to_state(temp_states[i])
        temp_states[i-1].del_edge(temp_states[i])
        temp_states[i-1].create_edge(t.states[find_minimized(temp_states[i])], current_word[i-1], output)
        #new_edge = fst.Edge(temp_states[i-1], t.states[find_minimized(temp_states[i])], current_word[i-1])
        temp_states[i].clear_state()
    minimized_state_index3 = find_minimized(temp_states[0])
    print(t.states[minimized_state_index3].outgoing_edges)
    t.define_initial(t.states[minimized_state_index3])
    
    return t




    

