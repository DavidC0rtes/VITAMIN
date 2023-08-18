from functions import *
from utilities.read_input import *
from classes import *


########################################################
# returns les actions de s1 à s2 que agent ne peut distinguer 
# donne les actions entre deux états ou agent joue le même rôle (fait la même action) que dans action
def indistinguishable_action(state1, state2, action, agent):
    action_indisting = []
    graph = get_graph()
    index1 = get_index_by_state_name(state1)
    index2 = get_index_by_state_name(state2)
    if index1 ==None or index2 == None :
        print("index faux")
        return None

    
    actions_s1tos2 = graph[index1][index2]
    if str(action) not in str(actions_s1tos2):
        return None 
    # si l'action précisée ne peut faire la transition de state1 à state2
    # if agent not in actions_s1tos2 :
    #     return None
    # si l'agent ne peut effectuer l'action précisée pour passer de state1 à state 2
    liste_actions1tos2 = build_list(actions_s1tos2)
    for act in liste_actions1tos2 : 
        if act[int(agent)-1]==action[int(agent)-1] :
            action_indisting.append(act)
        ## actions qui permettent d'aller de s1 à s2 et où action de l'agent a est la même que action
    return action_indisting #retourne aussi l'action entrée



def function_F_for_succ(q1, q2, alpha, agent_a):
    possible_action = indistinguishable_action(q1, q2, alpha, agent_a)
    agents = list(range(1,get_number_of_agents()+1))

    if possible_action == None :
        return None

    possible_set_capacities = []
    resultat = []
    for act in possible_action :
        possible_cap = []
        possible_cap = get_capacities_from_actionvector(act, agents)
        print(get_capacities_from_actionvector(act, agents))
        possible_set_capacities += possible_cap
    for value in possible_set_capacities : 
        resultat.append(list(value))
    return resultat

