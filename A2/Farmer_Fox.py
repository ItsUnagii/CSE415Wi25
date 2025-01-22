'''Farmer_Fox.py
by Aidan Lee and Dane Grassy
UWNetIDs: alee2005, [INSERT HERE]
Student numbers: 2176869, [INSERT HERE]

Assignment 2, in CSE 415, Winter 2025
 
This file contains our problem formulation for the problem of
the Farmer, Fox, Chicken, and Grain.
'''

# Put your formulation of the Farmer-Fox-Chicken-and-Grain problem here.
# Be sure your name(s), uwnetid(s), and 7-digit student number(s) are given above in 
# the format shown.

# You should model your code closely after the given example problem
# formulation in HumansRobotsFerry.py

# Put your metadata here, in the same format as in HumansRobotsFerry.
#<METADATA>
PROBLEM_NAME = "Farmer, Fox, Chicken, and Grain"
PROBLEM_VERSION = "1.0"
PROBLEM_AUTHORS = ['A. Lee']
PROBLEM_CREATION_DATE = "22-JAN-2025"

PROBLEM_DESC=\
 '''The <b>"Farmer, Fox, Chicken, and Grain"</b> problem, also known as
a river crossing puzzle, is a classic puzzle in which the player starts
off with a farmer, a fox, a chicken, and a bag of grain on one side of
a river. The object is to execute a sequence of legal moves that transfer
all four items to the other side of the river. In this puzzle, there is
a boat that can carry at most two items, and the farmer must be present
to steer the boat. It is forbidden to ever have the fox and the chicken
together (or the chicken will be eaten by the fox), or the chicken and the
grain together (or the grain will be eaten by the chicken). The computer
will not let you make a move to these forbidden situations, and it will
only show safe executable moves.
'''
#</METADATA>

# Start your Common Code section here.

#<COMMON_DATA>
#</COMMON_DATA>

#<COMMON_CODE>
LEFT=0 # values for left and right side of river
RIGHT=1

class State:
    
    def __init__(self, old=None):
        if old is None:
            self.farmer = LEFT
            self.fox = LEFT
            self.chicken = LEFT
            self.grain = LEFT
        else:
            self.farmer = old.farmer
            self.fox = old.fox
            self.chicken = old.chicken
            self.grain = old.grain
    
    def __eq__(self, s2):
        if self.farmer != s2.farmer: return False
        if self.fox != s2.fox: return False
        if self.chicken != s2.chicken: return False
        if self.grain != s2.grain: return False
        return True
    
    def __str__(self):
        # Produces a description of the current state, in text
        txt = "\n Farmer on the "
        txt += "left" if self.farmer == LEFT else "right"
        txt += "\n Fox on the "
        txt += "left" if self.fox == LEFT else "right"
        txt += "\n Chicken on the "
        txt += "left" if self.chicken == LEFT else "right"
        txt += "\n Grain on the "
        txt += "left" if self.grain == LEFT else "right"
        return txt
    
    def __hash__(self):
        # Produces a hash value for the current state
        return (self.__str__()).__hash__()
    
    def copy(self):
        # Creates a deep copy of the current state
        return State(old=self) # deep copy
    
    def can_move(self, item):
        ''' Tests whether it is legal to move the selected item. '''
        side = self.farmer # Where the farmer is.
        if item == "farmer": 
            return not ((self.fox == side and self.chicken == side) or (self.chicken == side and self.grain == side)) # can't leave the fox and chicken or chicken and grain alone
        elif item == "fox": # farmer must be there to pick up fox, can't leave other two unattended
            return self.fox == side and not (self.chicken == side and self.grain == side)
        elif item == "chicken":
            return self.chicken == side
        elif item == "grain":
            return self.grain == side and not (self.fox == side and self.chicken == side) # same idea for chicken and grain
        return False
        

    def move(self, item):
        ''' Moves the item across the river, assuming the move is safe. '''
        news = self.copy() # deep copy
        # move the selected item by reversing its side
        if item == "fox":
            news.fox = 1 - news.fox
        elif item == "chicken":
            news.chicken = 1 - news.chicken
        elif item == "grain":
            news.grain = 1 - news.grain
        # farmer always moves
        news.farmer = 1 - news.farmer
        return news
    
    def goal_message(self):
        return goal_message(self)
    
    

def goal_message(self):
    return "Congratulations on successfully moving the farmer, fox, chicken, and grain across the river!"

class Operator:
    def __init__(self, name, precond, state_transf):
        self.name = name
        self.precond = precond
        self.state_transf = state_transf

    def is_applicable(self, s):
        return self.precond(s)
    
    def apply(self, s):
        return self.state_transf(s)

#</COMMMON_CODE>
    
#<INITIAL_STATE>
CREATE_INITIAL_STATE = lambda: State()
#</INITIAL_STATE>

#<OPERATORS>

combinations = ["farmer", "fox", "chicken", "grain"]

OPERATORS = [Operator("Move " + item,
                      lambda s, item1=item: s.can_move(item1),
                      lambda s, item1=item: s.move(item1))
             for item in combinations]

#</OPERATORS>

# Finish off with the GOAL_TEST and GOAL_MESSAGE_FUNCTION here.
#<GOAL_TEST>
def GOAL_TEST(self):
    ''' Tests whether the current state is the goal state. '''
    return self.farmer == RIGHT and self.fox == RIGHT and self.chicken == RIGHT and self.grain == RIGHT 
#</GOAL_TEST>

#<GOAL_MESSAGE_FUNCTION>
GOAL_MESSAGE_FUNCTION = lambda s: goal_message(s)
#</GOAL_MESSAGE_FUNCTION>
