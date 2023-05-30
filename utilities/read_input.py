import numpy as np

graph = []
states = []
atomic_propositions = []
matrix_prop = []
initial_state = ''
number_of_agents = ''


# The function is used to read the content of the input file representing the model.
# It is designed in such a way that it can recognize the different parts of the text based
# on their title and appropriately divide it into sections.
# The different elements are then inserted into appropriate data structures.
def read_file(filename):
    global graph, states, atomic_propositions, matrix_prop, initial_state, number_of_agents

    with open(filename, 'r') as f:
        lines = f.readlines()

    # reset
    graph = []
    states = []
    atomic_propositions = []
    matrix_prop = []
    initial_state = ''
    number_of_agents = ''

    current_section = None
    transition_content = ''
    unknown_transition_content = ''
    name_state_content = ''
    atomic_propositions_content = ''
    labelling_content = ''
    rows_graph = []
    rows_prop = []

    for line in lines:
        line = line.strip()
        if line == 'Transition':
            current_section = 'Transition'
        elif line == 'Unkown_Transition_by':
            current_section = 'Unknown_Transition_by'
        elif line == 'Name_State':
            current_section = 'Name_State'
        elif line == 'Initial_State':
            current_section = 'Initial_State'
        elif line == 'Atomic_propositions':
            current_section = 'Atomic_propositions'
        elif line == 'Labelling':
            current_section = 'Labelling'
        elif line == 'Number_of_agents':
            current_section = 'Number_of_agents'
        elif current_section == 'Transition':
            transition_content += line + '\n'
            values = line.strip().split()
            rows_graph.append(values)
        elif current_section == 'Unknown_Transition_by':
            unknown_transition_content += line + '\n'
        elif current_section == 'Name_State':
            name_state_content += line + '\n'
            values = line.strip().split()
            states = np.array(values)
        elif current_section == 'Initial_State':
            initial_state = line
        elif current_section == 'Atomic_propositions':
            atomic_propositions_content += line + '\n'
            values = line.strip().split()
            atomic_propositions = np.array(values)
        elif current_section == 'Labelling':
            labelling_content += line + '\n'
            values = line.strip().split()
            rows_prop.append(values)
        elif current_section == 'Number_of_agents':
            number_of_agents = line

    grafo_prov = np.array(rows_graph)
    for row in grafo_prov:
        new_row = []
        for item in row:
            if item == '0':
                new_row.append(0)
            else:
                new_row.append(str(item))
        graph.append(new_row)

    # row = state, column = atom
    matrix_prop_prov = np.array(rows_prop)
    for row in matrix_prop_prov:
        new_row = []
        for item in row:
            if item == '0':
                new_row.append(0)
            elif item == '1':
                new_row.append(1)
            else:
                new_row.append(str(item))
        matrix_prop.append(new_row)


# It represents the model.
# Transitions are indicated through the actions performed by the agents from the source state (row) to the destination state (column).
def get_graph():
    return graph

# It returns the name of the states.
def get_states():
    return states

# returns the name of the atomic propositions
def get_atomic_prop():
    return atomic_propositions

# It returns a matrix that represents the atom labeling function.
# The rows represent the states, and the columns represent the atoms.
# The matrix indicates the values (between 0 and 1) of the atoms in each state.
def get_matrix_proposition():
    return matrix_prop


# returns the initial state
def get_initial_state():
    return initial_state


# returns the number of agents
def get_number_of_agents():
    return int(number_of_agents)
