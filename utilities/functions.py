import numpy as np

from utilities.read_input import *



def get_atom_index(element): # returns the index of the given atom, in the array of atomic propositions
    array = get_atomic_prop()
    try:
        index = np.where(array == element)[0][0]
        print(index)
        return index
    except IndexError:
        print("Element not found in array.")
        return None

def get_index_by_state_name(state):  # returns the index, given a state name
    state_list = get_states()
    index = np.where(state_list == state)[0][0]
    return index


def get_state_name_by_index(index):  # returns the state, given an index
    states = get_states()
    return states[index]


def build_list(action_string):   # converts action_string into a list
    if action_string == '*':
        action_string = '**,**'
    action_list = action_string.split(',')
    return action_list
