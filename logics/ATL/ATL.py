from utilities.functions import *
from binarytree import Node
from utilities.read_input import *
from utilities.parser.ATL import *

def get_states_prop_holds(set_prop):  # returns states where the proposition holds
    states = set()
    prop_matrix = get_matrix_proposition()
    for prop in set_prop:
        index = get_atom_index(prop)
        if index is None:
            return None
        for state, source in enumerate(prop_matrix):
            if source[int(index)] == 1:
                states.add(state)
    return states


def get_opponent_moves(actions, coalition):  # returns all moves except for those of the considered coalition
    other_moves = set()
    for x in actions:
        x = x[:coalition - 1] + x[coalition:]
        other_moves.add(x)
    return other_moves


def convert_state_set(state_set):  # set of states (e.g., s1, s2) as input and returns a set of indices to identify them
    states = set()
    for elem in state_set:
        position = get_index_by_state_name(elem)
        states.add(int(position))
    return states


def string_to_set(string):
    if string == 'set()':
        return set()
    set_list = string.strip("{}").split(", ")
    new_string = "{" + ", ".join(set_list) + "}"
    return eval(new_string)


def build_tree(tpl):
    if isinstance(tpl, tuple):
        root = Node(tpl[0])
        if len(tpl) > 1:
            root.left = build_tree(tpl[1])
            if len(tpl) > 2:
                root.right = build_tree(tpl[2])
    else:
        states = set()
        states_proposition = get_states_prop_holds(str(tpl))
        if states_proposition is None:
            return None # syntax error in atom
        else:
            for element in states_proposition:
                states.add(get_state_name_by_index(element))
            root = Node(str(states))

    return root


def pre(coalition, state_set):
    graph = get_graph()
    state_set = convert_state_set(state_set)  # returns a set of indeces
    pre_states = set()
    dict_state_action = dict()  # dictionary state-action
    for i, source in enumerate(graph):  # take states that have at least one transition to one of the states in the set
        for j in state_set:
            if graph[i][j] != 0:
                coordinates = str(i) + "," + str(j)
                dict_state_action.update({coordinates: build_list(graph[i][j])})

    # iterate over these states and check that my move is not present in any other state
    for key, value in dict_state_action.items():
        other_actions_in_row = dict()  # dictionary containing other moves of the row (excluding those saved in dict_state_action).
        all_actions_in_row = set()  # all elements in the row
        i = int(key.split(',')[0])
        j = int(key.split(',')[1])
        for index, element in enumerate(graph[i]):
            if element != 0:
                coordinates = str(i) + "," + str(index)
                all_actions_in_row.update(build_list(graph[i][index]))
                if index != j:
                    other_actions_in_row.update({coordinates: build_list(graph[i][index])})

        # check if there is a loop -> if yes, it is a pre
        if '**' in value:
            pre_states.add(str(i))
            break

        for action in value:
            move = action[coalition - 1]
            # checks whether a move is present in the others
            check_passed = True
            for k, v in other_actions_in_row.items():
                for el in v:
                    if el[coalition - 1] == move:
                        # check if it belongs to the set
                        column = int(k.split(',')[1])
                        if column not in state_set:
                            check_passed = False
                            break
                if not check_passed:
                    break
                if check_passed:
                    pre_states.add(i)

    # take the elements of the set and check if the moves towards the state contain all the possible opponent moves
    result = set()
    for i in pre_states:
        i = int(i)
        opponent_moves_in_state = set()
        opponent_moves_in_row = set()
        for j, column in enumerate(graph[int(i)]):
            if graph[i][j] != 0:
                opponent_moves_in_row.update(get_opponent_moves(build_list(graph[i][j]), coalition))
                if j in state_set:
                    # take the opponent's moves for actions towards the states in state_set
                    opponent_moves_in_state.update(get_opponent_moves(build_list(graph[i][j]), coalition))
        if opponent_moves_in_row == opponent_moves_in_state:
            # convert i into corresponding state
            result.add(get_state_name_by_index(i))
    return result


def solve_tree(node):
    if node.left is not None:
        solve_tree(node.left)
    if node.right is not None:
        solve_tree(node.right)

    if node.right is None:  # UNARY
        if verify('NOT', node.value):
            states = string_to_set(node.left.value)
            all_states = set(get_states())
            ris = all_states - states
            node.value = str(ris)

        elif verify('COALITION', node.value) and verify('GLOBALLY', node.value):
            coalition = int(node.value[1])
            states = string_to_set(node.left.value)
            p = set(get_states())
            t = states
            while p - t:  # p not in t
                p = t
                t = pre(coalition, p) & states
            node.value = str(p)

        elif verify('COALITION', node.value) and verify('NEXT', node.value):
            coalition = int(node.value[1])
            states = string_to_set(node.left.value)
            ris = pre(coalition, states)
            node.value = str(ris)

        elif verify('COALITION', node.value) and verify('EVENTUALLY', node.value):
            # trueUϕ.
            coalition = int(node.value[1])
            states1 = set(get_states())
            states2 = string_to_set(node.left.value)
            p = set()
            t = states2
            print(t)
            while t - p:  # t not in p
                p.update(t)
                t = pre(coalition, p) & states1
            node.value = str(p)

    if node.left is not None and node.right is not None:  # BINARY
        if verify('OR', node.value):
            states1 = string_to_set(node.left.value)
            states2 = string_to_set(node.right.value)
            ris = states1.union(states2)
            node.value = str(ris)

        elif verify('COALITION', node.value) and verify('UNTIL', node.value):
            coalition = int(node.value[1])
            states1 = string_to_set(node.left.value)
            states2 = string_to_set(node.right.value)
            p = set()
            t = states2
            while t - p:  # t not in p
                p.update(t)
                t = pre(coalition, p) & states1
            node.value = str(p)

        elif verify('AND', node.value):
            states1 = string_to_set(node.left.value)
            states2 = string_to_set(node.right.value)
            ris = states1.intersection(states2)
            node.value = str(ris)

        elif verify('IMPLIES', node.value):
            # p -> q ≡ ¬p ∨ q
            states1 = string_to_set(node.left.value)
            states2 = string_to_set(node.right.value)
            not_states1 = set(get_states()).difference(states1)
            ris = not_states1.union(states2)
            node.value = str(ris)


def verify_initial_state(initial_state, string):
    if initial_state in string:
        return True
    return False


def model_checking(formula, filename):
    if not formula.strip():
        result = {'res': 'Error: formula not entered', 'initial_state': ''}
        return result

    read_file(filename)

    # parsing
    res_parsing = do_parsing(formula, get_number_of_agents())
    if res_parsing is None:
        result = {'res': "Syntax Error", 'initial_state': ''}
        return result



    root = build_tree(res_parsing)
    if root is None:
        result = {'res': "Syntax Error: the atom does not exist", 'initial_state': ''}
        return result

    solve_tree(root)

    initial_state = get_initial_state()
    bool_res = verify_initial_state(initial_state, root.value)

    result = {'res': 'Result: ' + str(root.value), 'initial_state': 'Initial state '+ str(initial_state) + ": " + str(bool_res)}
    return result


