""" ItrBFS.py
Student Names: Aidan Lee & Dane Grassy
UW NetIDs: alee2005, dgrassy
CSE 415, Winter, 2025, University of Washington

This code contains my implementation of the Iterative BFS algorithm.

Usage:
 python ItrBFS.py HumansRobotsFerry
"""

import sys
import importlib


class ItrBFS:
    """
    Class that implements Iterative BFS for any problem space (provided in the required format)
    """

    def __init__(self, problem):
        """ Initializing the ItrBFS class.
        Please DO NOT modify this method. You may populate the required instance variables
        in the other methods you implement.
        """
        self.Problem = importlib.import_module(problem)
        self.COUNT = None  # Number of nodes expanded
        self.MAX_OPEN_LENGTH = None  # Maximum length of the open list
        self.PATH = None  # Solution path
        self.PATH_LENGTH = None  # Length of the solution path
        self.BACKLINKS = None  # Predecessor links, used to recover the path
        print("\nWelcome to ItrBFS")

    def runBFS(self):
        # Comment out the line below when this function is implemented.
        # raise NotImplementedError
        """This is an encapsulation of some setup before running
        BFS, plus running it and then printing some stats."""
        initial_state = self.Problem.CREATE_INITIAL_STATE()
        print("Initial State:")
        print(initial_state)
        
        self.COUNT = 0
        self.MAX_OPEN_LENGTH = 0
        self.BACKLINKS = {}

        self.IterativeBFS(initial_state)
        print(f"Number of states expanded: {self.COUNT}")
        print(f"Maximum length of the open list: {self.MAX_OPEN_LENGTH}")
        print(f"Path Length: {self.PATH_LENGTH}")
    
    def IterativeBFS(self, initial_state):
        """Actual BFS algorithm"""
        # STEP 1. Put the start state on a list OPEN
        OPEN = [initial_state]
        CLOSED = []
        self.BACKLINKS[initial_state] = None

        # STEP 2. If OPEN is empty, output “DONE” and stop.
        while OPEN != []:
            report(OPEN, CLOSED, self.COUNT, self.PATH_LENGTH)
            if len(OPEN) > self.MAX_OPEN_LENGTH:
                self.MAX_OPEN_LENGTH = len(OPEN)

            # STEP 3. Select the first state on OPEN and call it S.
            #         Delete S from OPEN.
            #         Put S on CLOSED.
            #         If S is a goal state, output its description
            S = OPEN.pop(0)
            CLOSED.append(S)

            if self.Problem.GOAL_TEST(S):
                print(self.Problem.GOAL_MESSAGE_FUNCTION(S))
                self.PATH = [str(state) for state in self.backtrace(S)]
                self.PATH_LENGTH = len(self.PATH) - 1
                return

            # STEP 4. Generate each state that can be reached from S,
            #         and if it has not been seen before, put it on OPEN
            self.COUNT += 1
            L = []
            for op in self.Problem.OPERATORS:
                if op.is_applicable(S):
                    new_state = op.apply(S)
                    if not (new_state in CLOSED):
                        L.append(new_state)
                        if new_state not in self.BACKLINKS:
                            self.BACKLINKS[new_state] = S

            # STEP 5. Delete from L any members of OPEN that occur on L.
            # 
            for s2 in OPEN:
                for i in range(len(L)):
                    if s2 == L[i]:
                        del L[i]
                        break
            
            OPEN = OPEN + L
            print_state_list("OPEN", OPEN)

    # STEP 6. Go to Step 2.
    
    def backtrace(self, s):
        path = []
        while s:
            path.append(s)
            s = self.BACKLINKS[s]
        path.reverse()
        print("Solution path: ")
        for s in path:
            print(s)
        return path

def print_state_list(name, lst):
    """
    Prints the states in the list
    """
    print(name + " is now: ", end='')
    for s in lst[:-1]:
        print(str(s), end=', ')
    print(str(lst[-1]))


def report(open, closed, count, PATH_LENGTH):
    """
    Reports the current statistics
    """
    print(f"len(OPEN)= {len(open)}", end='; ')
    print(f"len(CLOSED)= {len(closed)}", end='; ')
    print(f"COUNT = {count}")
    print(PATH_LENGTH)


if __name__ == '__main__':
    if sys.argv == [''] or len(sys.argv) < 2:
        Problem = "TowersOfHanoi"
    else:
        Problem = sys.argv[1]
    BFS = ItrBFS(Problem)
    BFS.runBFS()
