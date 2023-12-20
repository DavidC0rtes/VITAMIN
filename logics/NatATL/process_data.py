from logics.NatATL.strategies import initialize, generate_strategies
from logics.NatATL.pruning import pruning
import time

def process_data(structure, formula):
    # Start timer
    start_time = time.time()
    found_solution = False
    # initializes conditions and actions for involved agents
    cartesian_products, k, model, CTLformula, agents = initialize(structure, formula)
    # generates the initial strategies
    strategies_generator = generate_strategies(cartesian_products, k, agents, found_solution)
    # check for each strategy if there's a solution via pruning & model checking
    for current_strategy in strategies_generator:  # Iterate over the generator object
        found_solution = pruning(model, agents, CTLformula, current_strategy)  # Call pruning here
        if found_solution:
            print("Solution found!")
            # Write to file
            #returns the boolean satisfiability result, the current complexity bound, and the winning strategy for each agent
            return found_solution, k, current_strategy

    print(f"False, no states satisfying {CTLformula} have been found!")
    return found_solution, k, None

