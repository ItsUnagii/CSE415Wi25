"""EightPuzzleHamming.py
This file augments EightPuzzle.py with heuristic information,
so that it can be used by an A* implementation.
The particular heuristic is the Hamming heuristic, which is the number of tiles
that are in the wrong location.
"""

from EightPuzzle import *

def h(s):
    """The Hamming heuristic function."""
    count = 0
    goal = [[0, 1, 2], [3, 4, 5], [6, 7, 8]]
    for i in range(3):
        for j in range(3):
            if s.b[i][j] != goal[i][j] and s.b[i][j] != 0:
                count += 1
    return count