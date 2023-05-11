import numpy as np

graph = []
states = []
atomic_propositions = []
matrix_prop = []
initial_state = ''
number_of_agents = ''


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

    grafo_provv = np.array(rows_graph)
    for row in grafo_provv:
        new_row = []
        for item in row:
            if item == '0':
                new_row.append(0)
            else:
                new_row.append(str(item))
        graph.append(new_row)

    # row = state, column = atom
    matrix_prop_provv = np.array(rows_prop)
    for row in matrix_prop_provv:
        new_row = []
        for item in row:
            if item == '0':
                new_row.append(0)
            elif item == '1':
                new_row.append(1)
            else:
                new_row.append(str(item))
        matrix_prop.append(new_row)


def get_graph():
    return graph


def get_states():
    return states


def get_atomic_prop():
    return atomic_propositions


def get_matrix_proposition():
    return matrix_prop


def get_initial_state():
    return initial_state


def get_number_of_agents():
    return number_of_agents
