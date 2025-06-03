import sys

import graphviz

from vitamin_model_checker.models.CGS.CGS import *
from vitamin_model_checker.models.costCGS.costCGS import *
from vitamin_model_checker.models.timedCGS.timedCGS import *

"""
Generates a visualization of the CGS file in CGM (Concurrent Game Model) form.
Takes a path to the CGS file as argument.
"""
def read_cgs(filepath: str):
    concurrent_game_struct = timedCGS()
    concurrent_game_struct.read_file(filepath)

    dot = graphviz.Digraph(comment=filepath, graph_attr={'rankdir': 'LR'}, strict = True)
    states = concurrent_game_struct.get_states()
    graph_matrix = concurrent_game_struct.get_graph()
    atomic_props = concurrent_game_struct.get_atomic_prop()
    matrix_prop = concurrent_game_struct.get_matrix_proposition()
    initial_state_name = concurrent_game_struct.get_initial_state()
    clock_constraints = concurrent_game_struct.get_clock_constraints()
    invariants = concurrent_game_struct.get_invariants()
    print(initial_state_name)
    for i,state_name in enumerate(states):
        true_props = []
        if invariants[i]:
            true_props.append(invariants[i])
        if i < len(matrix_prop):  # Ensure index is within bounds for labelling matrix
            prop_row = matrix_prop[i]
            for j, val in enumerate(prop_row):
                if j < len(atomic_props) and str(val) == '1':  # Ensure index is within bounds for atomic_props
                    true_props.append(atomic_props[j])

        node_label = f"{state_name}"
        if true_props:
            node_label += f"\\n({', '.join(true_props)})" # Use \n for newline in Graphviz labels

        if state_name == initial_state_name:
            dot.node(state_name, label=node_label, style='filled', fillcolor='lightblue', shape='doublecircle')
        else:
            dot.node(state_name, label=node_label)
    
    # Add edges
    for i, row in enumerate(graph_matrix):
        source_state = states[i]
        for j, cell_value in enumerate(row):
            # Clock constraints on unlabelled edges are ignored
            if cell_value != 0:
                destination_state = states[j]
                constraint = clock_constraints[i*len(states) + j]
                # The cell_value can be a single action string or a comma-separated list
                if constraint != None:
                    edge_label = f"{constraint}, " + str(cell_value).replace(',', ', ') 
                else:
                    edge_label = str(cell_value).replace(',', ', ')
                dot.edge(source_state, destination_state, label=edge_label)

    dot.render('diagram-output', view=True)


if __name__ == "__main__":
    cgs_filename = sys.argv[1]
    read_cgs(cgs_filename)
