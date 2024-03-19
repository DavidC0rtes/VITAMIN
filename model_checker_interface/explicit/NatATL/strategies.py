"""Checked: This approach generates all possible strategies having complexity equal to a default k value, using two
main functions:
    - create_strategies(): generates all possible condition-action pairs combinations between agents (it uses
    the condition_action pairs given in input as cartesian product between all the possible actions/conditions for each agent)
    - generate_compound_strategies(): generates all the remaining strategies (i.e. less than k strategies) """
import itertools
import random
from models.CGS.CGS import *
import os
from logics.NatATL.NatATLtoCTL import get_agents_from_natatl, natatl_to_ctl, get_k_value
from logics.NatATL.stringParser import parse_string
from logics.NatATL.matrixParser import matrixParser

found_solution = False

#this function returns one strategy at time using "yield" keyword
def generate_conditions(P, C, max_k):
    condition_set = set()

    def generate_condition(k, condition):
        if k == 0:
            condition_tuple = tuple(condition)
            if condition_tuple not in condition_set:
                yield condition
                condition_set.add(condition_tuple)
        else:
            for p in P:
                if p not in condition:
                    new_condition = condition + [p]
                    if len(new_condition) == 1:
                        yield from generate_condition(k - 1, new_condition)
                    elif len(new_condition) > 1:
                        new_condition.sort()
                        new_condition_str = new_condition[0] + " " + random.choice(C) + " "
                        for i in range(1, len(new_condition) - 1):
                            new_condition_str += new_condition[i] + " " + random.choice(C) + " "
                        new_condition_str += new_condition[-1]
                        complexity = len(new_condition_str.split())
                        if complexity <= max_k:
                            yield from generate_condition(k - 1, [new_condition_str])

    for k in range(1, max_k + 1):
        yield from generate_condition(k, [])

# returns all the conditions (plus the negated ones only if max_k is big enough to do it)
def generate_negated(input_list, max_k):
    for input_str in input_list:
        atomic_props = input_str
        if isinstance(input_str, str):
            atomic_props = input_str.split(' && ')
        # Replace 'not' with '!' in the itertools.product line
        for combo in itertools.product(['', '!'], repeat=len(atomic_props)):
            # Include the atomic proposition in the negated condition
            negated_props = [f'{combo[i]}{atomic_props[i]}' if combo[i] != '' else atomic_props[i] for i in range(len(atomic_props))]
            new_str = ' && '.join(negated_props)
            complexity = len(new_str.split())
            if "!" in new_str:
                complexity+=1
            #print(f"complexity {complexity}")
            if (complexity == max_k):
                yield new_str


def generate_strategies(cartesian_products, k, agents, found_solution):
    strategies = [list() for _ in range(len(agents))]  # strategies are dictionaries

    def search_solution(strategies, current_strategy, depth):
        if depth == len(agents):
            yield current_strategy
        else:
            for agent in strategies[depth]:
                current_strategy.append(agent)
                yield from search_solution(strategies, current_strategy, depth + 1)
                current_strategy.pop()

    if not found_solution:
        for index, agent_key in enumerate(cartesian_products):
            cartesian_product = cartesian_products[agent_key]
            combinations = itertools.combinations(cartesian_product, 1)
            filtered_combinations = [combination for combination in combinations
                                     if len(set(action for _, action in combination)) == 1 and
                                     len(set(condition for condition, _ in combination)) == 1
                                     ]
            for combination in filtered_combinations:
                total_complexity = sum(len(condition.split()) + (1 if "!" in condition else 0) for condition, _ in combination)
                if total_complexity == k:
                    new_strategy = {"condition_action_pairs": list(combination)}
                    if not is_duplicate(strategies[index], new_strategy):
                        strategies[index].append(new_strategy)
                        yield from search_solution(strategies, [], 0)

    return strategies


def generate_compound_strategies(strategies, actions, k, agents):
    global found_solution
    new_combinations = []
    print("Im HERE")
    def search_solution(strategies, current_strategy, depth):
        if depth == len(agents):
            print(f"Current Strategy: {current_strategy}")
            yield current_strategy  # Yield current_strategy instead of calling pruning to call pruning from main
        else:
            for dictionary in strategies[depth]:
                for condition, action in dictionary['condition_action_pairs']:
                    new_strategy = {'condition_action_pairs': current_strategy[depth].get('condition_action_pairs', []) + [(condition, action)]}
                    total_complexity = sum(len(condition.split()) + (1 if "!" in condition else 0) for condition, _ in new_strategy['condition_action_pairs'])
                    if total_complexity == k and not is_duplicate(new_combinations, new_strategy) and len(new_strategy['condition_action_pairs']) <= len(actions[depth]):
                        current_strategy[depth]['condition_action_pairs'] = new_strategy['condition_action_pairs']
                        yield from search_solution(strategies, current_strategy,depth + 1)  # Use yield from to propagate the generator
                        current_strategy[depth]['condition_action_pairs'] = current_strategy[depth].get('condition_action_pairs', [])[:-1]

    return search_solution(strategies, [{'condition_action_pairs': []} for _ in range(len(agents))], 0)  # Return the generator object


def is_duplicate(existing_dictionaries, new_dictionary):
    for existing_dictionary in existing_dictionaries:
        if existing_dictionary['condition_action_pairs'] == new_dictionary['condition_action_pairs']:
            return True
    return False


class BreakLoop(Exception):
    pass

def agent_combinations(new_combinations):
    for agent1 in new_combinations:
        for agent2 in new_combinations:
                yield agent1, agent2

def initialize(model_path, formula):
    filename = os.path.abspath(model_path)

    if not os.path.isfile(filename):
        raise FileNotFoundError(f"No such file or directory: {filename}")
    cgs = CGS()
    cgs.read_file(filename)
    #print(formula)


    graph = cgs.get_graph()
    #check if input model is correct
    matrixParser(graph, cgs.get_number_of_agents())
    #transform natATL formula into CTL formula
    CTLformula = natatl_to_ctl(formula)
    print(formula)
    print(CTLformula)
    k = get_k_value(formula)
    #modificala per ritornare una lista di agenti se ho formule complesse
    agents = get_agents_from_natatl(formula)
    print(f"Envolved agents: {agents}")
    actions_per_agent = cgs.get_actions(graph, agents)
    print(f"actions picked by each agent:{actions_per_agent}")
    agent_actions = {}
    for i, agent_key in enumerate(actions_per_agent.keys()):
        agent_actions[f"actions_{agent_key}"] = actions_per_agent[agent_key]
    #print(f"Obtained actions: {agent_actions}")
    actions_list = [actions for actions in agent_actions.values()]
    atomic_propositions = cgs.get_atomic_prop()
    print(atomic_propositions)

    C = ['and', 'or']
    #print(f"k: {max_k}, CTL formula: {formula_CTL}, n: {len(agents)}, agents: {agents}")
    count = 0
    conditions = generate_conditions(atomic_propositions, C, k)

    try:
        cartesian_products = {}
        for agent_key in agent_actions.keys():
            for n in range(1, len(agent_actions[agent_key]) + 1):
                for combo in itertools.combinations(conditions, n):
                    for condition in combo:
                        negated_conditions = generate_negated([condition], k)
                        for variant in negated_conditions:
                            new_cartesian_products = generate_cartesian_products(actions_list, parse_string(variant))
                            for key, value in new_cartesian_products.items():
                                if key not in cartesian_products:
                                    cartesian_products[key] = []
                                cartesian_products[key].extend(value)
        #print(cartesian_products) #to see all possible condition action pairs for each agent
        #print(len(cartesian_products)) #to see if the number of cartesian products is equal to the envolved agents
        #print(type(cartesian_products))
        return cartesian_products, k, filename, CTLformula, agents

    except BreakLoop:
        pass

def generate_cartesian_products(actions_list, condition):
    cartesian_products = {}
    for i, actions in enumerate(actions_list, start=1):
        agent_key = f"actions_agent{i}"
        agent_cartesian_product = list(itertools.product([condition], actions))
        if agent_key not in cartesian_products:
            cartesian_products[agent_key] = []
        cartesian_products[agent_key].extend(agent_cartesian_product)
    return cartesian_products

