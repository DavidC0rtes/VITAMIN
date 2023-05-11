from utilities.functions import *
from logics.ATLF.pre_ATLF import *
from binarytree import Node
from utilities.parser.ATL import *


def get_tuple_list_prop(prop):  # returns a list of tuples (state, value) where the value depends on the input proposition
    i = get_atom_index(prop)
    if i is None:
        return None
    states = read_input.get_states()
    list = []
    matrix = read_input.get_matrix_proposition()

    for index, source in enumerate(matrix):
        tuple = (states[index], float(source[i]))
        list.append(tuple)
    return list


def build_tree(tpl):
    if isinstance(tpl, tuple):
        root = Node(tpl[0])
        if len(tpl) > 1:
            root.left = build_tree(tpl[1])
            if len(tpl) > 2:
                root.right = build_tree(tpl[2])
    else:
        couples = get_tuple_list_prop(tpl)
        if couples is None:
            return None
        root = Node(str(couples))

    return root


def string_to_tuple_list(string):  # converts a string in a list of tuple (state, value)
    list = string.strip("[]").split(", ")
    new_list = []
    for i in range(0, len(list), 2):
        state = list[i].strip("('")
        value = float(list[i + 1].strip(")"))
        new_tuple = (state, value)
        new_list.append(new_tuple)
    return new_list


def intersection_values(param, states):  # min
    list = []
    for i in range(0, len(param)):
        value = min(param[i][1], states[i][1])
        tuple = (param[i][0], value)
        list.append(tuple)
    return list


def set_value_tuple_list(value):  # assign a value to all elements in the list
    list = []
    states = read_input.get_states()
    for i in range(0, len(states)):
        tuple = (states[i], value)
        list.append(tuple)
    return list


def first_included_in_second(p, t):  # return if p is in t
    # p and t are list of tuples
    for i in range(0, len(p)):
        value_p = p[i][1]
        value_t = t[i][1]
        if value_p > value_t:
            return False
    return True


def update_values(p, t):  # if value_t > value_p updates
    list = []
    for i in range(0, len(p)):
        value_p = p[i][1]
        value_t = t[i][1]
        if value_t > value_p:
            tuple = (p[i][0], value_t)
        else:
            tuple = (p[i][0], value_p)
        list.append(tuple)
    return list


def difference_values(param, states):
    list = []
    for i in range(0, len(param)):
        value = param[i][1] - states[i][1]
        tuple = (param[i][0], value)
        list.append(tuple)
    return list


def union_values(states1, states2):  # max
    list = []
    for i in range(0, len(states1)):
        value = max(states1[i][1], states2[i][1])
        tuple = (states1[i][0], value)
        list.append(tuple)
    return list


def solve_tree(node):
    if node.left is not None:
        solve_tree(node.left)
    if node.right is not None:
        solve_tree(node.right)

    if node.right is None:  # UNARY

        # ¬φ := 1−φ
        if verify('NOT', node.value):
            states = string_to_tuple_list(node.left.value)
            ris = difference_values(set_value_tuple_list(1), states)
            node.value = str(ris)

        if verify('COALITION', node.value) and verify('GLOBALLY', node.value):
            coalition = int(node.value[1])
            states = string_to_tuple_list(node.left.value)
            p = set_value_tuple_list(1)  # true
            t = states
            while not first_included_in_second(p, t):  # p not in t
                p = t
                t = intersection_values(eval(pre(coalition, p)), states)
            node.value = str(p)

        elif verify('COALITION', node.value) and verify('NEXT', node.value):
            coalition = int(node.value[1])
            ris = pre(coalition, eval(node.left.value))
            node.value = str(ris)

        elif verify('COALITION', node.value) and verify('EVENTUALLY', node.value):
            coalition = int(node.value[1])
            states1 = set_value_tuple_list(1)
            states2 = string_to_tuple_list(node.left.value)
            p = set_value_tuple_list(0)
            t = states2
            while not first_included_in_second(t, p):  # t not in p
                p = update_values(p, t)
                t = intersection_values(eval(pre(coalition, p)), states1)
            node.value = str(p)

    if node.left is not None and node.right is not None:  # BINARY
        if verify('OR', node.value):
            states1 = string_to_tuple_list(node.left.value)
            states2 = string_to_tuple_list(node.right.value)
            res = []
            for i in range(0, len(states1)):
                state = states1[i][0]
                value = max(states1[i][1], states2[i][1])
                tuple = (state, value)
                res.append(tuple)
            node.value = str(res)

        elif verify('AND', node.value):
            states1 = string_to_tuple_list(node.left.value)
            states2 = string_to_tuple_list(node.right.value)
            res = []
            for i in range(0, len(states1)):
                state = states1[i][0]
                value = min(states1[i][1], states2[i][1])
                tuple = (state, value)
                res.append(tuple)
            node.value = str(res)

        elif verify('COALITION', node.value) and verify('UNTIL', node.value):
            coalition = int(node.value[1])
            states1 = string_to_tuple_list(node.left.value)
            states2 = string_to_tuple_list(node.right.value)
            p = set_value_tuple_list(0)
            t = states2
            while not first_included_in_second(t, p):  # t not in p
                p = update_values(p, t)
                t = intersection_values(eval(pre(coalition, p)), states1)
            node.value = str(p)

        elif verify('IMPLIES', node.value):
            # p -> q ≡ ¬p ∨ q
            states1 = string_to_tuple_list(node.left.value)
            states2 = string_to_tuple_list(node.right.value)
            not_states1 = difference_values(set_value_tuple_list(1), states1)
            ris = union_values(not_states1, states2)
            node.value = str(ris)


def get_value_initial_state(initial_state, string):
    list_tuple = eval(string)
    for element in list_tuple:
        if element[0] == initial_state:
            return element[1]


def model_checking(formula, filename):
    if not formula.strip():
        result = {'res': 'Error: formula not entered', 'initial_state': ''}
        return result

    read_input.read_file(filename)

    # parsing
    res_parsing = do_parsing(formula, read_input.get_number_of_agents())
    if res_parsing is None:
        result = {'res': "Syntax Error", 'initial_state': ''}
        return result

    root = build_tree(res_parsing)
    if root is None:
        result = {'res': "Syntax Error: the atom does not exist", 'initial_state': ''}
        return result

    solve_tree(root)

    initial_state = read_input.get_initial_state()
    value_initial_state = get_value_initial_state(initial_state, root.value)

    result = {'res': 'Result: ' + str(root.value), 'initial_state': 'Initial state ' + str(initial_state) + ": " + str(value_initial_state)}
    return result

