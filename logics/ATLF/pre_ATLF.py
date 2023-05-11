from utilities import functions, read_input
from anytree import Node, RenderTree


graph = read_input.get_graph()


def get_coalition_tree(action_coalition, trees):
    for t in trees:
        if t.name == action_coalition:
            return t
    return None


def print_tree(tree):
    for pre, fill, node in RenderTree(tree):
        print(f"{pre}{node.name}")


def build_node(strategy, state, parent):
    node = [state, parent + strategy]
    return node


def get_atom_value(atom_values, state):
    for elem in atom_values:
        if elem[0] == state:
            return elem[1]


def create_next_move_trees(coalition, state):
    destination = 0
    graph = read_input.get_graph()
    # transitions from a state
    index_state = functions.get_index_by_state_name(state)
    trees = []

    for action in graph[index_state]:
        if action != 0:
            action = functions.build_list(action)

            for move in action:
                coalition_move = move[coalition - 1]

                # create a tree for each action
                t = get_coalition_tree(coalition_move, trees)
                opponent_move = move[:coalition - 1] + move[coalition:]

                if t is None:
                    tree = Node(coalition_move)
                    node = build_node(opponent_move, destination, coalition_move)
                    Node(node, parent=tree)
                    trees.append(tree)

                else:
                    node = build_node(opponent_move, destination, t.name)
                    Node(node, parent=t)

            # ---- end for move ----
        destination = destination + 1
    # ---- end for action ----
    return trees


def evaluate_max_strategy(coalition, state, atom_values):  # returns max(min(t1, t2, t3...))

    # builds the strategy tree and then calculates the minimum value
    min_values_tree = []
    trees = create_next_move_trees(coalition, state)

    for el in trees:
        children = el.children
        values_tree = []
        for node in children:
            state = functions.get_state_name_by_index(node.name[0])
            values_tree.append(get_atom_value(atom_values, state))

        minimum = min(values_tree)
        min_values_tree.append(minimum)

    return max(min_values_tree)


def pre(coalition, atom_values):
    # pre for each state
    states = read_input.get_states()
    result = []
    for state in states:
        # coalition strategy from state
        max_value = evaluate_max_strategy(coalition, state, atom_values)
        # put value in the state tuple
        tuple = (state, max_value)
        result.append(tuple)

    # ------ end for state ---------
    result = str(result)
    return result
