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

            if s.b[row][col] != 0 and int(s.b[row][col]) != (int(goal[row][col])):
                sum += abs(row - (s.b[row][col] // 3)) + abs(col - (s.b[row][col] % 3))
    return sum