"""EightPuzzleManhattan.py
This file augments EightPuzzle.py with heuristic information,
so that it can be used by an A* implementation.
The particular heuristic is the sum of the Manhattan distances
of every tile from the correct location.

"""

from EightPuzzle import *

def h(s):
    """Sum of Manhattan distances for every tile to its desired location"""
    sum = 0
    goal = [[0, 1, 2], [3, 4, 5], [6, 7, 8]]
    for row in range(3):
        for col in range(3):

            if s.b[row][col] != goal[row][col] and s.b[row][col] != 0:
                sum += abs(row - (s.b[row][col] // 3)) + abs(col - (s.b[row][col] % 3))
                print("Add " + str(abs(row - (s.b[row][col] // 3))) + " rows and " + str(abs(col - (s.b[row][col] % 3))) + " cols for " + str(s.b[row][col]))
            # if s.b[i][j] != goal[i][j] and s.b[i][j] != 0:
            # print("Manhattan heuristic for " + str(s.b[i][j]) + " is " + str(abs(i - s.b[i][j]) + abs(j - s.b[i][j])))
            #     sum += abs(i - s.b[i][j]) + abs(j - s.b[i][j])
    
    
    print("Total manhattan heuristic: " + str(sum))
    return sum