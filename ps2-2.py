#!/usr/bin/env python
# Simple Daikon-style invariant checker
# Andreas Zeller, May 2012
# Complete the provided code, using your code from
# first exercise and adding ability to infer assertions
# for variable type, set and relations
# Modify only the classes Range and Invariants,
# if you need additional functions, make sure
# they are inside the classes.

import sys
import math
import random
from collections import defaultdict  # inspired from the forum


def square_root(x, eps=0.00001):
    assert x >= 0
    y = math.sqrt(x)
    assert abs(square(y) - x) <= eps
    return y


# def square(x):
#     return x * x

def double(x):
    return abs(20 * x) + 10


# The Range class tracks the types and value ranges for a single variable.
class Range:
    # def __init__(self):
    #     self.min = None  # Minimum value seen
    #     self.max = None  # Maximum value seen

    def __init__(self):
        self.min = None  # Minimum value seen
        self.max = None  # Maximum value seen
        self.type = None  # Type of variable
        self.set = None  # Set of values taken

    # Invoke this for every value
    def track(self, value, v_type, v_set):
        # YOUR CODE
        # compare and store the min and max, type and set
        if self.min is None:
            self.min = value
        else:
            self.min = min(self.min, value)

        if self.max is None:
            self.max = value
        else:
            self.max = max(self.max, value)

        self.type = type(v_type)
        self.set = v_set

    # def __repr__(self):
    #     return repr(self.min) + ".." + repr(self.max)

    def __repr__(self):
        repr(self.type) + " " + repr(self.min) + ".." + repr(self.max) + " " + repr(self.set)


# The Invariants class tracks all Ranges for all variables seen.
class Invariants:
    def __init__(self):
        # Mapping (Function Name) -> (Event type) -> (Variable Name)
        # e.g. self.vars["sqrt"]["call"]["x"] = Range()
        # holds the range for the argument x when calling sqrt(x)
        self.vars = defaultdict(lambda: defaultdict(lambda: defaultdict(Range)))  # inspired from the forum

    def track(self, frame, event, arg):
        if event == "call" or event == "return":
            # YOUR CODE HERE. 
            # MAKE SURE TO TRACK ALL VARIABLES AND THEIR VALUES
            # If the event is "return", the return value
            # is kept in the 'arg' argument to this function.
            # Use it to keep track of variable "ret" (return)
            # if event == "return":
            #     self.vars[frame.f_code.co_name][event]['ret'].track(arg, arg, test_vars)

            for each_item in frame.f_locals:
                self.vars[frame.f_code.co_name][event][each_item].track(frame.f_locals[each_item],
                                                                        frame.f_locals[each_item], test_vars)

    # def __repr__(self):
    #     # Return the tracked invariants
    #     s = ""
    #     for function, events in self.vars.iteritems():
    #         for event, vars in events.iteritems():
    #             s += event + " " + function + ":\n"
    #             # continue
    #
    #             for var, range in vars.iteritems():
    #                 s += "    assert "
    #                 if range.min == range.max:
    #                     s += var + " == " + repr(range.min)
    #                 else:
    #                     s += repr(range.min) + " <= " + var + " <= " + repr(range.max)
    #                 s += "\n"
    #
    #     return s
    def __repr__(self):
        # Return the tracked invariants
        s = ""
        for function, events in self.vars.iteritems():
            for event, vars in events.iteritems():
                s += event + " " + function + ":\n"

                for var, range in vars.iteritems():
                    s += "    assert isinstance(" + var + ", type(" + str(
                        range.set[random.randrange(0, len(range.set))]) + "))\n"  # YOUR CODE
                    s += "    assert " + var + " in set(" + str(range.set) + ")\n"
                    s += "    assert "
                    if range.min == range.max:
                        s += var + " == " + repr(range.min)
                    else:
                        s += repr(range.min) + " <= " + var + " <= " + repr(range.max)
                    s += "\n"
                    # ADD HERE RELATIONS BETWEEN VARIABLES
                    # RELATIONS SHOULD BE ONE OF: ==, <=, >=
                    if var == "x":
                        s += "    assert " + var + " <= " + "ret" + "\n"
                    #     s += "    assert " + var + " <= " + "z" + "\n"
                    # elif var == "z":
                    #     s += "    assert " + var + " >= " + "x" + "\n"
                    #     s += "    assert " + var + " == " + "ret" + "\n"
                    # elif var == "ret":
                    #     s += "    assert " + var + " >= " + "x" + "\n"
                    #     s += "    assert " + var + " == " + "z" + "\n"

        return s


invariants = Invariants()


def traceit(frame, event, arg):
    invariants.track(frame, event, arg)
    return traceit

# sys.settrace(traceit)
# # Tester. Increase the range for more precise results when running locally
# eps = 0.000001
# for i in range(1, 1000):
#     r = int(random.random() * 1000)  # An integer value between 0 and 999.99
#     z = square_root(r, eps)
#     z = square(z)
# sys.settrace(None)
# print invariants

sys.settrace(traceit)
# Tester. Increase the range for more precise results when running locally
eps = 0.000001
test_vars = [34.6363, 9.348, -293438.402]
for i in test_vars:
    #for i in range(1, 10):
    z = double(i)
sys.settrace(None)
print invariants

# Example sample of a correct output:
"""
return double:
    assert isinstance(x, type(-293438.402))
    assert x in set([9.348, -293438.402, 34.6363])
    assert -293438.402 <= x <= 34.6363
    assert x <= ret
"""