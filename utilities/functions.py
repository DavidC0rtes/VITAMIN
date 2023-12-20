from utilities.read_input import *


# returns the index of the given atom, in the array of atomic propositions
def get_atom_index(element):
    array = get_atomic_prop()
    try:
        index = np.where(array == element)[0][0]
        return index
    except IndexError:
        print("Element not found in array.")
        return None


# returns the index, given a state name
def get_index_by_state_name(state):
    state_list = get_states()
    index = np.where(state_list == state)[0][0]
    return index


# returns the state, given an index
def get_state_name_by_index(index):
    states = get_states()
    return states[index]


# converts action_string into a list
def build_list(action_string):
    ris = ''
    if action_string == '*':
        for i in range(0, get_number_of_agents()):
            ris += '*'
        action_string = ris
    action_list = action_string.split(',')
    return action_list


# returns a set of agents given a coalition (e.g. 1,2,3)
def get_agents_from_coalition(coalition):
    agents = coalition.split(",")
    return set(agents)


# sort and remove 0 from agents
def format_agents(agents):
    agents = sorted(agents)
    if 0 in agents:
        agents.remove(0)
    agents = {int(x) - 1 for x in agents}
    return agents


# returns coalition's actions
def get_coalition_action(actions, agents):
    coalition_moves = set()
    result = ''
    agents = format_agents(agents)
    if len(agents) == 0:
        for i in range(0, get_number_of_agents()):
            result += '-'
    else:
        for x in actions:
            for i, letter in enumerate(x):
                if i in agents:
                    result += letter
                else:
                    result += '-'

            coalition_moves.add(result)
    return coalition_moves


def get_base_action(action, agents):
    return get_coalition_action(set([action]), agents).pop()

# returns all moves except for those of the considered coalition
def get_opponent_moves(actions, agents):
    other_moves = set()
    agents = format_agents(agents)
    for x in actions:
        result = ""
        for i, letter in enumerate(x):
            if i not in agents:
                result += letter
            else:
                result += '-'

        other_moves.add(result)
    return other_moves

#added NatATL functions below

def get_label(index):
    return f's{index}'

def create_label_matrix(graph):
    label_matrix = []
    for i, row in enumerate(graph):
        label_row = [get_label(i) if isinstance(elem, str) and elem != '*' else None for elem in row]
        label_matrix.append(label_row)
    return label_matrix