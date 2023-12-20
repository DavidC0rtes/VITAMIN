from logics.NatATL.modelCheckingCTL import model_checking, process_modelCheckingCTL
from utilities.read_input import read_file,get_graph, get_actions, get_states, get_number_of_agents, write_updated_file
from utilities.functions import create_label_matrix
from utilities.parser.NatATL.matrixParser import matrixParser

#path destination for new updated input file
output_file = 'C:\\Users\\lmfao\\Desktop\\Tesi\\TESTING\\output.txt'

def modify_matrix(graph, label_matrix, states, action, agent_index, agents):
    #print(f"states:{states}")
    new_graph = [row.copy() for row in graph]
    rows_modified = [False] * len(new_graph)
    for i, row in enumerate(new_graph):
        row_modified = False
        for j, elem in enumerate(row):
            if label_matrix[i][j] in states:
                if isinstance(elem, str) and elem != '*':
                    elem_parts = elem.split(',')
                    new_elem_parts = []
                    for part in elem_parts:
                        part_list = list(part)
                        agent_matches = False
                        if part_list[agents[agent_index-1]-1] == 'I' or part_list[agents[agent_index-1]-1] == action:
                            agent_matches = True
                        if agent_matches:
                            new_elem_parts.append(part)
                    new_elem = ','.join(new_elem_parts)
                    new_graph[i][j] = new_elem if new_elem else 0
                    row_modified = True
        rows_modified[i] = row_modified
    return new_graph

def process_transition_matrix_data(model, agents,  *strategies):
    read_file(model)

    graph = get_graph()
    label_matrix = create_label_matrix(graph)
    print(f"initial transition matrix: {graph}")
    #print(f"associated labelling matrix:{label_matrix}")
    actions_per_agent = get_actions(graph, agents)
    agent_actions = {}
    for i, agent_key in enumerate(actions_per_agent.keys()):
        agent_actions[f"actions_{agent_key}"] = actions_per_agent[agent_key]

    for agent_key in agent_actions:
        print(agent_key)
        print(agent_actions[agent_key])

    for strategy_index, strategy in enumerate(strategies, start=1):
        state_sets = set()
        temp = set()
        for iteration, (condition, action) in enumerate(strategy['condition_action_pairs']):
            #print(f"condition {condition}")
            states = model_checking(condition, model)
            #print(f" result: m_checking{states}, statesres {states['res']}")
            state_set = eval(states['res'].split(': ')[1])

            if iteration > 0:
                if (state_set):
                    temp = state_sets
                    state_sets = state_set - temp
                else:
                    state_sets = set(get_states())
                    action = "I"
                #print(f"state_set: {state_sets} con iteration {iteration} action {action}")
                graph = modify_matrix(graph, label_matrix, state_sets, action, strategy_index, agents)
                #print(f"second iteration modify_matrix for agent {strategy_index}")
                print(f'new transition matrix: {graph} modified by agent {strategy_index}')
            else:
                if (state_set):
                    state_sets = state_set
                else:
                    state_sets = set(get_states())
                    action = "I"
                #print(f"state_set: {state_sets}, iteration {iteration} action {action}")
                graph = modify_matrix(graph, label_matrix, state_sets, action, strategy_index, agents)
                #print(f"First iteration of modify_matrix for agent {strategy_index}")
                print(f'new transition matrix: {graph} modified by agent {strategy_index}')

    return graph

def pruning(model, agents, formula, current_agents):
    modified_graph = process_transition_matrix_data(model, agents,  *current_agents)
    matrixParser(modified_graph, get_number_of_agents())
    write_updated_file(model, modified_graph, output_file)
    result = process_modelCheckingCTL(output_file, formula)

    if (result['initial_state'] == 'Initial state s0: True'):
        #print(result)
        return True