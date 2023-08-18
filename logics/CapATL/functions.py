from utilities.read_input import *
import itertools
from itertools import combinations, permutations
from logics.CapATL.classes import *


##########################################################
# donne toutes le combinaisons de sous listes 
# i.e. [[1, 5], [4], [2,3]] donne [(1, 4, 2), (1, 4, 3), (5, 4, 2), (5, 4, 3)]
def trouver_combinaisons(listes):
    combinaisons = list(itertools.product(*listes))
    return combinaisons


# returns the states where the proposition holds
def get_states_prop_holds(prop):
    states = set()
    prop_matrix = get_matrix_proposition()

    index = get_atom_index(prop)
    if index is None:
        return None
    for state, source in enumerate(prop_matrix):
        if source[int(index)] == 1:
            states.add(state)
    return states


#returns the atomic propositions held in the state 
def get_prop_held_in_state(state):
    props = set()
    prop_matrix = get_matrix_proposition()

    index = get_index_by_state_name(state)
    if index is None : 
        return None
    state_atoms=prop_matrix[index] # row of the state
    for prop, source in enumerate(state_atoms):
        if source == 1 :
            props.add(prop)
    return props 


# returns the index of the given atom, in the array of atomic propositions
def get_atom_index(element):
    array = get_atomic_prop()
    try:
        index = np.where(array == element)[0][0]
        return index
    except IndexError:
        print("Element not found in array.")
        return None

# returns the index given a state name 
def get_index_by_state_name(state):
    if len(state) ==1 :
        state = state[0]
    else :
        interm = ''
        for elem in state : 
            interm = interm + elem
        state = str(interm)

    state_list = get_states()

    for count, st in enumerate(state_list) :
        if state == st :
            return count

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


# returns a set of agents given a coalition ("1,3,6") -> {'6','1','3'}
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


# returns possible capacities given an action A or B etc (not a vector)
def get_capacities_from_action(action):
    possible_capacities = []
    capacities = get_action_capacities() 
    for tupl in capacities:
        if action in tupl: 
            possible_capacities.append(tupl[0])
    return possible_capacities


def get_capacities_from_action2(action, agent) :
    result = []
    cap_ag = get_capacities_assignment()[int(agent)-1][1:]
    ens = get_action_capacities()
    if action == '*' :
        result = cap_ag
    for j in ens :
        if j[0] in cap_ag :
            if action in j :
                result.append(j[0])
    return result


def get_capacities_from_actionvector(action, agents):
    result1 = []
    for ag in agents :
        interm = []
        act = action[int(ag)-1]
        interm = get_capacities_from_action2(act, ag)
        result1.append(interm)
    result = trouver_combinaisons(result1)
    return result


# returns the set X_agt_cap
def X_agt_cap():
    cap_assgn = get_capacities_assignment()
    interm = []
    result = []
    for elem in cap_assgn :
        interm.append(elem[1:])
    interm = trouver_combinaisons(interm)
    for value in interm :
        result.append(list(value))

    return result

def X_agt_cap2() : 
    result = set()
    for elem in X_agt_cap():
        result.add(tuple(elem))
    return result


def generate_subsets(liste):
    subsets = []
    for r in range(1, len(liste) + 1):
        subsets.extend(tuple(tuple(subset) if len(subset) > 1 else subset[0] for subset in combinations(liste, r)))
    return subsets

def possible_knowledge() :
    result_f = []
    capacity_ass = X_agt_cap2()
    result_f = generate_subsets(capacity_ass)
    return result_f


def generer_sous_ensembles_ord_rep(ensemble, p):
    n = len(ensemble)
    resultats = []

    def generer_sous_ensemble_ord_rep_recursion(sous_ensemble):
        if len(sous_ensemble) == p:
            resultats.append(sous_ensemble)
        elif len(sous_ensemble) < p:
            for i in range(n):
                generer_sous_ensemble_ord_rep_recursion(sous_ensemble + [ensemble[i]])

    generer_sous_ensemble_ord_rep_recursion([])
    return resultats


def intersection_listes(listes):
    if not listes or len(listes) < 2:
        return []
    # Convertir la première liste en un ensemble de tuples
    ensemble_intersection = set(map(tuple, listes[0]))
    # Trouver l'intersection avec les autres listes
    for liste in listes[1:]:
        ensemble_intersection = ensemble_intersection.intersection(map(tuple, liste))
    # Convertir l'ensemble d'intersection en une liste de listes
    intersection = list(map(list, ensemble_intersection))
    
    return intersection


# returns coalition's actions from a given state 
def get_coalition_action_from_q(coalition, state_q) :

    agents = get_agents_from_coalition(coalition)
    agents = format_agents(agents)

    graph = get_graph()
    if get_index_by_state_name(state_q) is None : 
        return None
    possible_actions = graph[get_index_by_state_name(state_q)]
    result = []
    string = ""
    index = 0
    for act in possible_actions :
        if type(act) == str :
            for ag in agents :
                index = int(ag)
                string = string + act[index]
            result.append(string)
            string = ""
    return result   


def pointed_knowledge_set() : 
    P_cap = possible_knowledge()
    if [] in P_cap : 
        P_cap.remove([])
    for j in P_cap : 
        j = tuple(j)
    Pcap = generer_sous_ensembles_ord_rep(P_cap, get_number_of_agents())
    states = get_states()
    result = []
    agents = tuple(i for i in range(1,get_number_of_agents()+1))

    for st in states : 
        for value in Pcap :
            if intersection_listes(value) != [] :
                obj = p_knowledge(tuple(st), tuple(value), agents)
                result.append(obj)  
    return result


def Omega_Y(coal_Y) : #coal_Y string "1,3"
    result = []
    coalition = coal_Y
    pointed_knowl = pointed_knowledge_set()
    agents_tot = tuple(i for i in range (1, get_number_of_agents()+1))
    
    for elem in pointed_knowl :
        poss_action = get_coalition_action_from_q(coal_Y, getattr(elem, 'state'))
        if poss_action is not None :
            for act in poss_action :
                obj = p_knowledge_for_Y(0,[],0,[],[])
                obj.coalition = coalition
                obj.agents = agents_tot
                obj.state = getattr(elem, 'state') 
                obj.knowledge = getattr(elem, 'knowledge')
                obj.action = act
                result.append(obj)

    return result


# returns a list of possible actions for elem = [q, delta1...deltak] so that elem + action is in W
def action_in_W(elem, W) :
    action = []

    for value in W :

        if getattr(value, 'knowledge') == getattr(elem, 'knowledge') and getattr(value, 'state') == getattr(elem, 'state'):
            action.append(getattr(value, 'action'))
    return action


#function pi_theta needed in model checking
def pi_theta(W) :
    theta = pointed_knowledge_set()
    result = []
    for elem in theta :
        if len(action_in_W(elem, W)) :
            result.append(elem)
    return result 


# returns the actions that corresponds to the given capacity
def get_actions_from_capacity(capacity):
    result = 0
    corresp = get_action_capacities()
    for value in corresp : 
        if value[0]==capacity :
            result = value[1:]
    return result


# returns coalition's actions
def get_coalition_action(coalition):
    agents = get_agents_from_coalition(coalition)
    
    cap_ag = get_capacities_assignment()
    result = []
    act = []
    for ag in agents : 
        
        capacities = cap_ag[int(ag)-1][1:]
        for capac in capacities :
            act += get_actions_from_capacity(capac)
        result.append(act)   
        act = []
    return trouver_combinaisons(result)


# retruns the non null actions to reach q 
def get_actions_to_reach_q(state_q) :
    result = []
    graph = get_graph()
    nb_states = len(get_states())
    nb_agents = get_number_of_agents()
    index = get_index_by_state_name(state_q)

    for i in range(0, nb_states) :
        act = graph[i][index]
        if act != 0 :
            if len(act)>nb_agents :
                interm = act.split(',')
                for elem in interm :
                    result.append(elem)
            else : 
                result.append(act)
    return result


def intersection_n_listes(listes):

    ensembles = [set(lst) for lst in listes]
    intersection = set.intersection(*ensembles)
    return intersection


def possible_capacity(liste, taille ):
    sub_set = generer_sous_ensembles_ord_rep(liste, taille)
    result = []

    for elem in sub_set :
        if len(intersection_n_listes(elem)) != 0 :
            result.append(elem)
    return result


def pi_omega_Y(W, coalition_Y) :
    omega_Y = Omega_Y(coalition_Y)
    result = []
    dict_W = {}
    for obj in W : 
        key = (obj.state, obj.knowledge)
        dict_W[key] = obj
    for value in omega_Y :
        key = (value.state, value.knowledge)
        if key in dict_W :
            result.append(value)
    return result


# returns les actions de s1 à s2 que agent ne peut distinguer 
# donne les actions entre deux états ou agent joue le même rôle (fait la même action) que dans action
def indistinguishable_action(state1, state2, action, agent):
    action_indisting = []
    graph = get_graph()
    index1 = get_index_by_state_name(state1)
    index2 = get_index_by_state_name(state2)
    if index1 == None or index2 == None :
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
    for act in possible_action :
        possible_cap = []
        possible_cap = get_capacities_from_actionvector(act, agents)
            
        possible_set_capacities += possible_cap
    
    return possible_set_capacities


def succ(p_knowledge_for_Y):
    S = []

    coalition = getattr(p_knowledge_for_Y, 'coalition')
    agents_coal = get_agents_from_coalition(coalition)
    action = getattr(p_knowledge_for_Y, 'action')
    state = getattr(p_knowledge_for_Y, 'state')
    set_capacity = getattr(p_knowledge_for_Y, 'knowledge')
    graph = get_graph()

    act_st = [] # actions of the coalition that lead to an accessible state
    accessible_state = [] #state accessible from q
    act_coalition = get_coalition_action(coalition)
    index = get_index_by_state_name(state)
    
    if index is None :
        return None 
    
    # accessible state list build by checking in the row of state if there is an action of the coalition
    for count, value in enumerate(graph[index]):
        if value != 0 :
            accessible_state.append(count)
            act_st.append(value)

    act_interm = []
    action_acceptable = []
    action_acceptable_final = []
    k = 0
    non_acc_state = []
    # need to check if these actions match with beta for all the coalition
    for supp, act in enumerate(act_st) : 
        action_acceptable = []
        act_interm = build_list(act) # list of possible actions from q to act

        for count, elem in enumerate(act_interm) :
            for count2, value2 in enumerate(list(format_agents(set(agents_coal)))): 
                if str(elem[value2]) != str(action[count2]):
                    k +=1 
            
            if k==0 : # each action corresponds to beta 
                action_acceptable.append(elem)
            k = 0
        
        if len(action_acceptable) == 0 : # no action to reach the state corresponds to beta 
            non_acc_state.append(accessible_state[supp])
        else :
            action_acceptable_final.append(action_acceptable)
        act_interm = []

    accessible_state = [ x for x in accessible_state if x not in non_acc_state]
    capacity_interm = [] # delta,a'
    set_capacity2 = [] # set of delta,a'
    intersection = set_capacity
    z = []
    agents_tot = list(range(1,get_number_of_agents()+1)) #[1,2,...]
    for count2bis, q in enumerate(accessible_state) :   
        for alpha in action_acceptable_final[count2bis] :
            set_capacity2 = []
            # g, d = 0
            for a in agents_tot : 
                z = []
                if function_F_for_succ(state, get_state_name_by_index(q), alpha, a) == None :
                    capacity_interm = []
                
                else :
                    if type(set_capacity[a-1][0]) != tuple :
                        g = {set_capacity[a-1]}
                    else : 
                        g = set(set_capacity[a-1])
                    if len(function_F_for_succ(state, get_state_name_by_index(q), alpha, a)) == 1 : 
                        d = {function_F_for_succ(state, get_state_name_by_index(q), alpha, a)[0]}
                    else : 
                        d = set(function_F_for_succ(state, get_state_name_by_index(q), alpha, a))
                    capacity_interm = g & d 
                for u in capacity_interm : 
                    z.append(u)
                set_capacity2.append(z)
            intersection = intersection_n_listes(set_capacity2)
            set_capacity2 = tuple((sublist[0]) if len(sublist) == 1 else tuple(sublist) for sublist in set_capacity2 )
            obj = p_knowledge(get_state_name_by_index(q), set_capacity2, agents_tot )
            if len(intersection) != 0 and obj.not_in(S) :
                S.append(obj)
    return S


def point_know_in_set(point_know_subset, Set) :
    result = []
    for elem in Set : 
        if elem.not_in(point_know_subset) :
            result.append(elem)
    return result


# returns the possible actions for agent in state
def protocol_function(agent, state) :
    return get_coalition_action_from_q(str(agent), state)


# return if there is some possible set of action to do in st
def final_state(st) :
    graph = get_graph()
    if get_index_by_state_name(st) is not None :
        for j in graph[get_index_by_state_name(st)] :
            if j != 0 :
                return True
    return False 

# returns true if the model is correct otherwise false
def validity_model() :
    # 1st condition 
    for ag in range(1, get_number_of_agents()) :
        for st in get_states() :
            act = []
            act_graph = protocol_function(ag, st)
            cap = get_capacities_assignment()[ag-1]
            for elem in cap[1:] :
                for j in get_actions_from_capacity(elem) :
                    act.append(j)
            for x in act_graph : 
                if x not in act :
                    return False
    
    # 2nd condition 
    graph = get_graph()
    for ag in range(1, get_number_of_agents()) :
        for st in get_states() :
            if final_state(st) is not False :
                for c in get_capacities_assignment()[ag-1][1:] :
                    intersec = [l for l in protocol_function(ag, st) if l in get_actions_from_capacity(c)]
                    if len(intersec) == 0 :
                        print(st, c, ag)
                        return False

    return True
