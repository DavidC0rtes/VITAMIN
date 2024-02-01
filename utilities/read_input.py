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
costs = []
cost_for_action = {}
usesCostsInsteadOfActions = False

def read_file(filename):
    global graph, states, atomic_propositions, matrix_prop, initial_state, number_of_agents, capacities_assignment, action_capacities, actions, capacities, cost_for_action

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
    cost_for_action = {}

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
    usesCostsInsteadOfActions = False

    for line in lines:
        line = line.strip()
        #Section "header"
        if line == 'Transition':
            current_section = 'Transition'
            useCostsInsteadOfActions = False
        elif line == 'Transition_With_Costs':
            current_section = 'Transition'
            usesCostsInsteadOfActions = True
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
        elif line == 'Costs_for_actions':
            current_section = 'Costs_for_actions'
        elif line == 'Costs_for_actions_split':
            current_section = 'Costs_for_actions_split'

        #If not header, then read contents based on what section we are in
        
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
        elif current_section == "Costs_for_actions":
            values = line.strip().split()
            action_name = values[0]
            state_and_cost_string = values[1].split(";")
            for couple in state_and_cost_string:
                state_and_cost = couple.split(",")
                cost_for_action.update({translate_action_and_state_to_key(action_name, state_and_cost[0]): int(state_and_cost[1])})
        elif current_section == "Costs_for_actions_split":
            values = line.strip().split()
            action_name = values[0]
            state_and_cost_string = values[1].split(";")
            for couple in state_and_cost_string:
                state_and_cost = couple.split(",")
                costs = [int(c) for c in state_and_cost[1:]]
                cost_for_action.update({translate_action_and_state_to_key(action_name, state_and_cost[0]): costs})
    
    actions =[]
    a = 0
    grafo_prov = np.array(rows_graph)
    for row in grafo_prov:
        new_row = []
        for item in row:
            if item == '0':
                new_row.append(0)
            else:
                if (usesCostsInsteadOfActions):
                    new_row.append(item)
                else:
                    new_row.append(str(item))
                    a = item.split(",")
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

def read_from_model_object(model):
    global graph, states, atomic_propositions, matrix_prop, initial_state, number_of_agents, capacities_assignment, action_capacities, actions, capacities
    graph = model.transition_matrix
    states = np.array(model.state_names)
    atomic_propositions = np.array(model.propositions)
    matrix_prop = model.labelling_function
    initial_state = model.initial_state
    number_of_agents = model.number_of_agents
    capacities_assignment = model.capacities_assignment
    actions_capacities = model.actions_for_capacities
    actions = model.actions
    capacities = np.array(model.capacities)
    cost_for_action = model.cost_for_action
    
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
    
def get_costs():
    return costs

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

def translate_action_and_state_to_key(action_string, state):
    return action_string + ";" + state
    
def get_cost_for_action(action, state):
    return cost_for_action[translate_action_and_state_to_key(action, state)]
    
def get_cost_for_action_all():
    return cost_for_action

#NatATL added functions below


def get_actions(graph, agents):
    # Convert the graph string to a list of lists
    graph_list = graph

    # Create a dictionary to store actions for each agent
    actions_per_agent = {f"agent{agent}": [] for agent in agents}

    for row in graph_list:
        for elem in row:
            if elem != 0 and elem != '*':
                actions = elem.split(',')
                for action in actions:
                    for i, agent in enumerate(agents):
                        if action[agent - 1] != 'I':  # idle condition
                            actions_per_agent[f"agent{agent}"].append(action[agent - 1])

    # Remove duplicates from each agent's action list
    for agent_key in actions_per_agent:
        actions_per_agent[agent_key] = list(set(actions_per_agent[agent_key]))

    return actions_per_agent

#return the number of actions extracted in get_actions()
def get_number_of_actions ():

    n = get_actions()
    return len(n)

def write_updated_file(input_filename, modified_graph, output_filename):
    if modified_graph is None:
        raise ValueError("modified_graph is None")
    with open(input_filename, 'r') as input_file, open(output_filename, 'w') as output_file:
        current_section = None
        matrix_row = 0
        for line in input_file:
            line = line.strip()

            if line == 'Transition':
                current_section = 'Transition'
                output_file.write(line + '\n')
            elif current_section == 'Transition' and matrix_row < len(modified_graph):
                output_file.write(' '.join([str(elem) for elem in modified_graph[matrix_row]]) + '\n')
                matrix_row += 1
            elif current_section == 'Transition' and matrix_row == len(modified_graph):
                current_section = None
                output_file.write('Unkown_Transition_by' + '\n')
            else:
                output_file.write(line + '\n')

#returns the edges of a graph
def get_edges():
    graph = get_graph()
    states = get_states()
    #duplicate edges (double transactions from "a" to "b") are ignored due to model checking
    edges = []
    for i, row in enumerate(graph):
        for j, element in enumerate(row):
            if element == '*':
                edges.append((states[i], states[i]))
            elif element != 0:
                edges.append((states[i], states[j]))
    return edges

def file_to_string(filename):
    with open(filename, 'r') as file:
        data = file.read()
    return data