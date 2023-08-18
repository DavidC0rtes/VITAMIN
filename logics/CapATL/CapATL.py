from itertools import combinations
from logics.CapATL.functions import *
from logics.CapATL.pre import *
from utilities.parser.CapATL import *
from logics.CapATL.classes import *

def verifier_chiffres_et_lettres(liste):
    a_des_chiffres = False
    a_des_lettres = False
    if liste == None :
        return None
    for element in liste:
        if isinstance(element, int) or element.isdigit():
            a_des_chiffres = True
        elif isinstance(element, str) and element.isalpha():
            a_des_lettres = True

    return a_des_chiffres and a_des_lettres


# returns the complement of point_know_subset in set, i.e. all the elements of set that are not in subset
def point_know_in_set(point_know_subset, Set) :
    result = []
    for elem in Set : 
        if elem.not_in(point_know_subset) :
            result.append(elem)
    return result


# returns the intersection of two sets of pointed knowledge 
def intersection_set_pointkno(set1, set2) :
    result = []
    for elem in set1 :
        if elem.not_in(set2) == False :
            result.append(elem)
    return result


# retruns true if set1 is in or equal to set2 
def set_in(set1, set2) : 
    size1 = len(set1)
    size2 = len(set2)
    if size1 > size2 :
        return False 
    for elem in set1 :
        if elem.not_in(set2) == True :
            return False
    return True 


# returns given a tpl 36c1 ag=36
def get_ag_capag(tpl) :
    result = ""
    for elem in tpl : 
        if (elem.isdigit() == False) :
            return result 
        result = result + elem
    return int(result)


# returns the subset of ensemble = pointed knowledge such as the actions corresponds to the cap of agent
def select(ensemble, agent, cap) : 
    ris2 = []
    list_ag = agent.split(',')
    cap = cap.split(',')
    for i in ensemble : 
        k=0
        act = getattr(i, 'action')
        for count, value in enumerate(act) :
            capacity = capacities_from_agact(list_ag[count], value)
            if cap[count] in capacity : 
                k +=1
        if k == len(act) :
            ris2.append(i)
    return ris2


def build_tree(tpl):
    if isinstance(tpl, tuple):
        root = Node_PK(tpl[0])
        if len(tpl) > 1:
            left_child = build_tree(tpl[1])
            if left_child is None:
                return None
            root.left = left_child
            if len(tpl) > 2:
                right_child = build_tree(tpl[2])
                if right_child is None:
                    return None
                root.right = right_child
    else:
        if verifier_chiffres_et_lettres(tpl) :
            phi = []
            capacity = set()
            ag = int(get_ag_capag(tpl)) - 1
            cap_a = tpl[len(str(ag)):]
            X_ag_cap = X_agt_cap()
            for cap in X_ag_cap :
                if cap[ag] == cap_a : 
                    phi.append(cap)
            for elem in phi :
                capacity.add(tuple(elem))
            if len(capacity) == 0 : 
                return None 
            root = Node_PK(capacity)
        else :
            phi = []
            pointed_know = set()
            Theta = pointed_knowledge_set()
            states = get_states_prop_holds(str(tpl))
            if states is None : 
                return None 
            for theta in Theta :
                if get_index_by_state_name(getattr(theta, 'state')) != None :
                    if get_index_by_state_name(getattr(theta, 'state')) in states :
                        phi.append(theta)
            if phi is [] :
                return None 
            else : 
                for elem in phi :
                    pointed_know.add(elem)
                root = Node_PK(pointed_know)
    return root


# returns the coalition string given <1,2,3>jjdhdj
def get_coalition(string) :
    result = ""
    for elem in string[1:] : 
        if elem == '>' :
            return result 
        result = result + elem
    return result


# returns all the numbers of the given string 
def get_agents(string) :
    result =""
    for elem in string :
        if elem.isdigit() :
            result = result + elem
    return result 


# returns [1,2,3], [cap,cop,get] given :  1,2,3 is cap,cop,get
def extract_values_and_words(chaine):
    parties = chaine.split(' is ')
    valeurs_f = parties[0]
    mots_f = parties[1]
    return valeurs_f, mots_f


def capacities_from_agact(ag, act) : 
    capacities_agent = get_capacities_assignment()[int(ag)-1][1:]
    if act == '*' :
        return capacities_agent
    cap = get_capacities_from_action(act)
    result = [ x for x in capacities_agent if x in cap]
    return result 


def is_sublist_present(liste_principale, sous_liste):
    set1 = set(liste_principale)
    if type(list(sous_liste)[0]) != tuple :
        set2 = {sous_liste}
    else :
        set2 = set(sous_liste)
    return set2.issubset(set1)
    

def solve_tree(node):
    if node.left is not None:
        solve_tree(node.left)
    if node.right is not None:
        solve_tree(node.right)
    if node.right is None:   # UNARY OPERATORS: not, globally, next, eventually

        if len(str(node.value)) > 32 :
            return node.value

        if verify('NOT', str(node.value)): 
             # e.g. ¬φ
            states = node.left.value # set 
            if type(next(iter(states))) == tuple : 
                ris = []
                Xagtcap = X_agt_cap() # list of lists
                for elem in Xagtcap : 
                    if tuple(elem) not in states : 
                        ris.append(tuple(elem))
                node.value = set(ris)

            if type(next(iter(states))) == p_knowledge :
                pointed_know = set(pointed_knowledge_set())
                ris = pointed_know - states
                node.value = set(ris)
        

        elif verify('COALITION', str(node.value)) and verify('NEXT', str(node.value)):  # e.g. <1>Xφ
            agent = str(get_coalition(node.value))
            states = list(node.left.value)
            ris = pi_omega_Y(states, agent)
            ris2 = []
            list_ag = agent.split(',')
            ris = pre(ris, agent)
            ris = pi_theta(ris)
            node.value = set(ris)


        elif verify('KCAP', str(node.value)) :
            ag = get_agents(node.value)
            ag = int(ag) -1 
            result = []
            Theta = pointed_knowledge_set()
            know = 0
            ens = set()
            for elem in node.left.value :
                ens.add(tuple(elem))
            for elem in Theta :
                know = tuple(getattr(elem, 'knowledge')[ag])
                if is_sublist_present(ens, know) :
                    result.append(elem)
            node.value = set(result)

    
    

    if node.left is not None and node.right is not None:  # BINARY OPERATORS: or, and, until, implies
        
        if verify('COALITION', str(node.value)) and verify('RELEASE', str(node.value)) :
            agent = str(get_coalition(node.value))
            
            W1 = Omega_Y(agent)
            W2 = pi_omega_Y(node.right.value, agent)
            cst = pi_omega_Y(node.left.value, agent)
            
            while set_in(W1, W2) == False :
                W1 = intersection_set_pointkno(W1, W2)
                W2 = pre(W1, agent) + cst
            ris = set(pi_theta(W1))
            node.value = ris

        elif verify('COALITION', str(node.value)) and verify('UNTIL', str(node.value)):  # e.g. <1>φUθ
            agent = str(get_coalition(node.value))
            W1 = []
            W2 = pi_omega_Y(node.right.value, agent)
            cst = pi_omega_Y(node.left.value, agent) #a
            k = 0
            while set_in(W2, W1) == False :
                W1 = W1 + W2 
                k += 1
                W2 = intersection_set_pointkno(pre(W1, agent), cst)
            ris = set(pi_theta(W1))
            node.value = ris

        
        elif verify('AND', str(node.value)):  # e.g. φ ^ θ
            states1 = node.left.value
            
            states2 = node.right.value
            ris = set()
            if type(next(iter(states1))) == p_knowledge : 
                ris = states1 & states2
                node.value = ris

                # ris = states1.intersection(states2)
                node.value = ris
            
            if type(next(iter(states1))) == tuple : 
                ris = states1.intersection(states2)
                
    return node.value


def convert_state_set(state_set):
    states = set()
    for elem in state_set:
        position = get_index_by_state_name(elem)
        states.add(int(position))
    return states


# converts a string into a set
def string_to_set(string):
    if string == 'set()':
        return set()
    set_list = string.strip("{}").split(", ")
    new_string = "{" + ", ".join(set_list) + "}"
    return eval(new_string)


# returns whether the result of model checking is true or false in the initial state
def verify_initial_state(initial_state, string):
    if initial_state in string:
        return True
    return False

def model_checking(formula, filename) :
    debug = ''
    if not formula.strip():
        result = {'res': 'Error: formula not entered', 'initial_state': ''}
        return result

    # model parsing
    read_file(filename)

    # check if the model is acceptable
    if validity_model() is False :
        result = {'res': "Incorrect model", 'initial state': '' }


    # formula parsing
    res_parsing = do_parsing(formula, get_number_of_agents())

    if res_parsing is None:
        result = {'res': "Syntax Error", 'initial_state': ''}
        print(result)
        return result

    root = build_tree(res_parsing)
    debug += 'root : ' + str(root) + '\n'
    if root is None:
        result = {'res': "Syntax Error: the atom does not exist", 'initial_state': ''}
        print(result)
        return result

    # model checking
    solve_tree(root)
    state = []
    for elem in root.value : 
        debug += 'elem : ' + str(elem) + '\n'
        # elem.print_p_knowledge()
        k = 0
        for know in getattr(elem, 'knowledge') :
            debug += 'know : ' + str(know) + '\n'
            debug += 'know : ' + str(tuple(X_agt_cap2())) + '\n'
            if know == tuple(X_agt_cap2()) : 
                k +=1        
        debug += 'k : ' + str(k) + '\n'
        if k == get_number_of_agents() and getattr(elem, 'state') not in state:
            state.append(getattr(elem, 'state'))
    # print(state)
    # print(root.value)
    # # solution
    # initial_state = get_initial_state()
    # bool_res = verify_initial_state(initial_state, root.value)
    result = {'res': formula}

    return result



