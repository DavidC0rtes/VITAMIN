from enum import Enum
import re
from vitamin_model_checker.models.CGS.CGS import *

class timedCGS():
    def __init__(self):
        self.clocks = []
        self.cgs = None
        self.clock_constraint_struct = []
    
    def read_file(self, filename):
        """
        Parses the definition file for the CGS with real-time constraints.
        First the file is parsed ignoring every timed aspect using the CGS class.
        Then, we parse the timed aspects.
        """
        self.cgs = CGS()
        self.cgs.read_file(filename)
        with open(filename, 'r') as f:
            lines = f.readlines()

        current_section = Sections('Unsupported')
        # Initialize flattened 2d array to hold clock constraints.
        self.clock_constraint_struct = [None] * (len(self.cgs.get_states())**2)
        self.invariants_dict = dict.fromkeys([x for x in range(len(self.cgs.get_states()))])

        custom_index = 0
        for line in lines:
            line = line.strip()
            if (custom_index >= len(self.cgs.get_states())):
                custom_index = 0
            # Section header
            if line == 'Clocks':
                current_section = Sections.CLOCKS
            elif line  == 'Clock_constraints':
                current_section = Sections.CLOCK_CONSTRAINTS
            elif line  == 'Invariants':
                current_section = Sections.INVARIANTS
            else:
                match current_section.name:
                    case Sections.CLOCKS.name:
                        self.clocks = line.strip().split()
                        print(f"Clocks: {self.clocks}")
                    case Sections.CLOCK_CONSTRAINTS.name:
                        values = line.strip().split()
                        self.__parse_clock_constraints(values, custom_index)
                        custom_index += 1
                    case Sections.INVARIANTS.name:
                        self.__parse_invariants(line.strip().split(), custom_index)
                        custom_index +=1

    def get_states(self):
        return self.cgs.get_states()

    def get_graph(self):
        return self.cgs.get_graph()

    def get_atomic_prop(self):
        return self.cgs.get_atomic_prop()
    
    def get_matrix_proposition(self):
        return self.cgs.get_matrix_proposition()
    
    def get_initial_state(self):
        return self.cgs.get_initial_state()
    
    def get_clock_constraints(self):
        return self.clock_constraint_struct
    
    def get_invariants(self):
        return self.invariants_dict

    def __parse_clock_constraints(self, line: list[str], row: int):
        columns = len(self.cgs.get_states())
        for col, constraint in enumerate(line):
            if (re.match(r'\w+(?:=|>|<|>=|<|<=)\d+', constraint)):
                self.clock_constraint_struct[row*columns + col] = constraint

    
    def __parse_invariants(self, line: list[str], state: int):
        """
        Receives a row of the invariants matrix (state x clock) and a reference
        to the current line being parsed (the state).
        Returns 
        dict: A dictionary where keys are states (s0,s1,...) and values are
                formatted strings (e.g., 'x<2', 'x<1, y<3') or None.
        """
        parts = []
        for index, value in enumerate(line):
            if value != "-1":
                parts.append(f"{self.clocks[index]}<{value}")

        if parts:
            self.invariants_dict[state] = ", ".join(parts)

class Sections(Enum):
    CLOCKS = 'Clocks',
    CLOCK_CONSTRAINTS = 'Clock_constraints',
    INVARIANTS = 'Invariants',
    UNSUPPORTED = 'Unsupported'