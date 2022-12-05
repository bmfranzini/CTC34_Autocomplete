import fst_lib2 as fst
import pickle

# defino as variáveis globais
t = fst.FST()

def find_minimized(state):
    # retorna um estado equivalente do dicionário. Se não estiver presente, insere uma cópia
    # do parâmetro no dicionário e o retorna
    global t
    for state_index in range(len(t.states)):
        if t.states[state_index].is_equivalent(state):
            return state_index
    new_state = fst.State(fst.NORMAL_STATE)
    new_state.copy_state(state)
    t.node_counter += 1
    t.states.append(new_state)

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
        while(j < len(current_word) and j < len(previous_word) - 1 and current_word[j] == previous_word[j]):
            j += 1
        prefix_len = j  # número máximo de letras do prefixo comum
        # minimizamos os estados do sufixo da última palavra
        for j in range(len(previous_word), prefix_len, -1):
            output = temp_states[j-1].output_to_state(temp_states[j])
            temp_states[j-1].del_edge(temp_states[j])
            temp_states[j-1].create_edge(t.states[find_minimized(temp_states[j])], previous_word[j-1], output)
            temp_states[j].clear_state()
        
        for j in range((prefix_len)+1, len(current_word)):
            temp_states[j].clear_state()

        # inicializamos os estados do vetor para a palavra atual (considero apenas o sufixo, pois o resto já está inicializado)
        for j in range((prefix_len), len(current_word)):
            temp_states[j].create_edge(temp_states[j+1], current_word[j], 0)

        if current_word != previous_word:
            temp_states[len(current_word)].type = fst.FINAL_STATE
        
        # encontramos o output da bifurcação
        prefix_output = 0

        for j in range(prefix_len+1):
            prefix_output += temp_states[j].output(current_word[j])
        new_output = current_output - prefix_output
        
        if input_list[i] == "tuessd":
            print("prefix_len: ", prefix_len)
            print("current_output: ", current_output)
            print("prefix_output: ", prefix_output)

        temp_states[prefix_len].set_output(temp_states[prefix_len+1], new_output)
        
        previous_word = current_word
    
    # minimizamos os estados da última palavra
    for i in range(len(current_word), 0, -1):
        output = temp_states[i-1].output_to_state(temp_states[i])
        temp_states[i-1].del_edge(temp_states[i])
        temp_states[i-1].create_edge(t.states[find_minimized(temp_states[i])], current_word[i-1], output)
        temp_states[i].clear_state()
    minimized_state_index3 = find_minimized(temp_states[0])
    t.define_initial(t.states[minimized_state_index3])
    
    return t




    

