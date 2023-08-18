import numpy as np

graph = []
states = []
atomic_propositions = []
matrix_prop = []
initial_state = ''
number_of_agents = ''
capacities_assignment = []
actions = []
action_capacities = []
capacities = []


def read_file(filename):
    global graph, states, atomic_propositions, matrix_prop, initial_state, number_of_agents, capacities_assignment, action_capacities, actions, capacities

    with open(filename, 'r') as f:
        lines = f.readlines()

    graph = []
    states = []
    atomic_propositions = []
    matrix_prop = []
    initial_state = ''
    number_of_agents = ''
    capacities_assignment = []
    action_capacities = []
    capacities = []

    current_section = None
    transition_content = ''
    unknown_transition_content = ''
    name_state_content = ''
    atomic_propositions_content = ''
    labelling_content = ''
    rows_graph = []
    rows_prop = []
    capacities_assignment_content = ''
    action_assign_content = ''
    capacities_content = ''

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
        elif line == 'Capacities' :
            current_section = 'Capacities'
        elif line == 'Capacities_assignment':
            current_section = 'Capacities_assignment'
        elif line == 'Actions_for_capacities':
            current_section = 'Actions_for_capacities'


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
        elif current_section == 'Capacities' :
            capacities_content += line + '\n'
            values = line.strip().split()
            capacities = np.array(values)
        elif current_section == 'Capacities_assignment':
            capacities_assignment_content += line + '\n'
            values = line.strip().split()
            capacities_assignment.append(values)
        elif current_section == 'Actions_for_capacities':
            action_assign_content += line + '\n'
            values = line.strip().split()
            action_capacities.append(values)
            
    actions =[]
    a = 0
    grafo_prov = np.array(rows_graph)
    for row in grafo_prov:
        new_row = []
        for item in row:
            if item == '0':
                new_row.append(0)
            else:
                new_row.append(str(item))
            a= item.split(",")
            for elem in a :
                actions.append(elem)
        graph.append(new_row)   

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
    return int(number_of_agents)

def get_actions():
    return actions

def get_capacities_assignment2():
    return capacities_assignment

def get_capacities_assignment() :
    cap_ass = get_capacities_assignment2()
    result = []
    for i in range (1, get_number_of_agents()+1) :
        interm = [str(i)]
        cap_ag = cap_ass[i-1]
        for count, value in enumerate(cap_ag) :
            if value == '1' :
                interm.append(get_capacities()[count])
        result.append(interm)

    return result


def get_action_capacities():
    return action_capacities

def get_capacities(): 
    result = []
    for elem in capacities :
        result.append(elem)
    return result



