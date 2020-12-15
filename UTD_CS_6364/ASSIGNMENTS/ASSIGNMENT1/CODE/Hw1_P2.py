from utils import *
from search import *
from search_modified import *
import math

"""
-------------------------------------------------------------------------------------
---------------------------- MISSIONARY CANNIBAL PROBLEM ----------------------------
-------------------------------------------------------------------------------------

Missionaries and Cannibals are to be brought from left to the right side of the river.
Maintaining the constraint of number of cannibals not exceeding number of missionaries.

"""


class MissionaryCannibalProblem(Problem):
    def __init__(self, initial, goal):
        Problem.__init__(self, initial, goal)
        self.state = initial

    def actions(self, state):
        """
        State : (M,C,B)
        1. Boat on the left side [Indicated by B=0]
            1. Number of missionaries on the left side (0,1,2,3) [Indicated by '3-M']
                1. Number of cannibals on the left side (0,1,2,3) [Indicated by '3-C']
        2. Boat on the right side [Indicated by B=1]
            1. Number of missionaries on the right side (0,1,2,3) [Indicated by 'M']
                1. Number of cannibals on the right side (0,1,2,3) [Indicated by 'C']

        Based on M, C, B each state has a set of legal and illegal actions available.
        We return the legal actions available for each state
        """
        if state[2] == 0:  # Boat on the left
            if state[0] == 0:  # 3 missionaries on the left
                if state[1] == 0:
                    return ['MC', 'C', 'CC']
                elif state[1] == 1:
                    return ['M', 'C', 'CC']
                elif state[1] == 2:
                    return ['MM', 'C']
                else:
                    return []
            elif state[0] == 1:  # 2 missionaries on the left
                if state[1] == 1:
                    return ['MC', 'MM']
                else:
                    return []
            elif state[0] == 2:  # 1 missionary on the left
                if state[1] == 2:
                    return ['MC', 'M']
                else:
                    return []
            else:  # 0 missionary on the left
                if state[1] <= 1:
                    return ['C', 'CC']
                elif state[1] == 2:
                    return ['C']
                else:
                    return []
        elif state[2] == 1:  # Boat on the right side
            if state[0] == 0:  # 3 missionaries on the left
                if state[1] == 0:
                    return []
                elif state[2] == 1:
                    return ['C']
                else:
                    return ['C', 'CC']
            elif state[0] == 1:  # 2 missionaries on the left
                if state[1] == 1:
                    return ['M', 'MC']
                else:
                    return []
            elif state[0] == 2:  # 1 missionary on the left
                if state[1] == 2:
                    return ['MM', 'MC']
                else:
                    return []
            else:  # No missionary on the left
                if state[1] == 1:
                    return ['MM', 'C']
                elif state[1] == 2:
                    return ['M', 'C', 'CC']
                else:
                    return []
        else:
            return []

    def result(self, state, action):
        state = list(state)
        if state[2] == 0:  # Boat on the left, (For actions we add them)
            if action == 'M':
                state[0] = state[0] + 1
                state[2] = 1
            elif action == 'MM':
                state[0] = state[0] + 2
                state[2] = 1
            elif action == 'MC':
                state[0] = state[0] + 1
                state[1] = state[1] + 1
                state[2] = 1
            elif action == 'C':
                state[1] = state[1] + 1
                state[2] = 1
            else:
                state[1] = state[1] + 2
                state[2] = 1
        elif state[2] == 1:  # Boat on the right, (For actions we subtract them)
            if action == 'M':
                state[0] = state[0] - 1
                state[2] = 0
            elif action == 'MM':
                state[0] = state[0] - 2
                state[2] = 0
            elif action == 'MC':
                state[0] = state[0] - 1
                state[1] = state[1] - 1
                state[2] = 0
            elif action == 'C':
                state[1] = state[1] - 1
                state[2] = 0
            else:
                state[1] = state[1] - 2
                state[2] = 0

        state = tuple(state)
        self.state = state
        return self.state

    def goal_test(self, state):
        if state == self.goal:
            return True
        else:
            return False

    def h(self, node):
        """
        Here we define the following heuristic function:
        h(M,C,B) = ceil([(3-M) + (3-B)]/2)
        [This is a consistent heuristic (Optimal for graph search strategies)]
        """
        current_state = node.state
        return math.ceil(((3 - current_state[0]) + (3 - current_state[1]))/2)


initial = tuple([0, 0, 0])
goal = tuple([3, 3, 1])

missionary_cannibal_problem = MissionaryCannibalProblem(initial, goal)

"""
---------------------------------------------------------------------------------
1. Using the implementation of breadth first tree search to find solution
---------------------------------------------------------------------------------
"""

bread_first_tree_search_solution = breadth_first_tree_search(missionary_cannibal_problem)
for node in bread_first_tree_search_solution.path():
    print(node.action, node.state)

"""
---------------------------------------------------------------------------------
2. Path to the solution generated by code for the following strategies
    a. Uniform Cost Search
    b. Iterative Deepening Search
    c. Greedy Best First Search
    d. A* Search
    e. Recursive best first search
---------------------------------------------------------------------------------
"""

print('------------------------------------------------------------------------------------')
print('------------------------------------UCS STRATEGY-----------------------------------')
print('------------------------------------------------------------------------------------')

"""
UNIFORM COST SEARCH STRATEGY
As we define cost for each action as 1.
Uniform cost search strategy equals the breadth first tree search.
"""

uniform_cost_search_solution = uniform_cost_search_modified(missionary_cannibal_problem, lambda n: n.path_cost)
for node in bread_first_tree_search_solution.path():
    print(node.action, node.state, node.path_cost)

print('------------------------------------------------------------------------------------')
print('------------------------ITERATIVE DEEPENING SEARCH STRATEGY-------------------------')
print('------------------------------------------------------------------------------------')

"""
ITERATIVE DEEPENING SEARCH STRATEGY
"""

iterative_deepening_search_solution = iterative_deepening_search_modified(missionary_cannibal_problem)
for node in iterative_deepening_search_solution.path():
    print(node.action, node.state)

print('------------------------------------------------------------------------------------')
print('-------------------------HEURISTIC CONSISTENCY CHECK--------------------------')
print('------------------------------------------------------------------------------------')

print('Is Heuristic consistent ? ' + str(consistent_heuristic_check(missionary_cannibal_problem)))

print('------------------------------------------------------------------------------------')
print('-------------------------GREEDY BEST FIRST SEARCH STRATEGY--------------------------')
print('------------------------------------------------------------------------------------')

"""
GREEDY BEST FIRST SEARCH STRATEGY
It requires the usage of a heuristic function.
Heuristic used here : ceil(((3-M) + (3-C))/2)
"""

h = memoize(missionary_cannibal_problem.h, 'h')
greedy_best_first_search_solution = best_first_search_modified('GBFS', missionary_cannibal_problem, lambda n: h(n))

for node in greedy_best_first_search_solution.path():
    print(node.action, node.state, node.path_cost)

print('------------------------------------------------------------------------------------')
print('-----------------------------------A* SEARCH STRATEGY-------------------------------')
print('------------------------------------------------------------------------------------')

"""
A* SEARCH STRATEGY
It requires the usage of a heuristic function.
We define an admissible heuristic h(M,C,B) = ceil(((3-M) + (3-C))/2)
"""

h = memoize(missionary_cannibal_problem.h, 'h')
a_star_search_solution = best_first_search_modified('A*', missionary_cannibal_problem, lambda n: n.path_cost + h(n))

for node in a_star_search_solution.path():
    print(node.action, node.state, node.path_cost)

print('------------------------------------------------------------------------------------')
print('------------------------------------RBFS STRATEGY-----------------------------------')
print('------------------------------------------------------------------------------------')

"""
RBFS SEARCH STRATEGY
It requires the usage of a heuristic function.
We define an admissible heuristic h(M,C,B) = ceil(((3-M) + (3-C))/2)
"""

rbfs_result = recursive_best_first_search_modified(missionary_cannibal_problem)

for node in rbfs_result.path():
    print(node.action, node.state, node.path_cost)