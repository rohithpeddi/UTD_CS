# from .SEARCH.CORE import Graph
# from .SEARCH.CORE import Problem
# from .SEARCH.RecursiveBestFirstSearch import *

from utils import *
from search import *
from search_modified import *

"""
Simplified road map of US
"""

us_map = UndirectedGraph((dict(
    LosAngeles=dict(SanFrancisco=383, Austin=1377, Bakersville=153),
    SanFrancisco=dict(Bakersville=283, Seattle=807),
    Seattle=dict(SantaFe=1463, Chicago=2064),
    Bakersville=dict(SantaFe=864),
    Austin=dict(Dallas=195, Charlotte=1200),
    SantaFe=dict(Dallas=640),
    Boston=dict(Austin=1963, Chicago=983, SanFrancisco=3095),
    Dallas=dict(NewYork=1548),
    Charlotte=dict(NewYork=634),
    NewYork=dict(Boston=225),
    Chicago=dict(SantaFe=1272)
)))
us_map.locations = dict(
    Austin=(0, 182),
    Charlotte=(0, 929),
    SanFrancisco=(0, 1230),
    LosAngeles=(0, 1100),
    NewYork=(0, 1368),
    Chicago=(0, 800),
    Seattle=(0, 1670),
    SantaFe=(0, 560),
    Bakersville=(0, 1282),
    Boston=(0, 1551),
    Dallas=(0, 0)
)


class USRoadMapProblem(Problem):
    """The problem of searching a graph from one node to another."""

    def __init__(self, initial, goal, graph):
        super().__init__(initial, goal)
        self.graph = graph

    def actions(self, A):
        """The actions at a graph node are just its neighbors."""
        return list(self.graph.get(A).keys())

    def result(self, state, action):
        """The result of going to a neighbor is just that neighbor."""
        return action

    def path_cost(self, cost_so_far, A, action, B):
        return cost_so_far + (self.graph.get(A, B) or np.inf)

    def find_min_edge(self):
        """Find minimum value of edges."""
        m = np.inf
        for d in self.graph.graph_dict.values():
            local_min = min(d.values())
            m = min(m, local_min)
        return m

    def h(self, node):
        """h function is straight-line distance from a node's state to goal."""
        locs = getattr(self.graph, 'locations', None)
        if locs:
            if type(node) is str:
                return int(distance(locs[node], locs[self.goal]))
            return int(distance(locs[node.state], locs[self.goal]))
        else:
            return np.inf

    def value(self, state):
        pass


# 1. PROBLEM FORMULATION
initial = 'Seattle'
goal = 'Dallas'
us_map_problem = USRoadMapProblem(initial, goal, us_map)

# 2. USING RBFS SEARCH STRATEGY
print('------------------------------------------------------------------------------------')
print('------------------------------------RBFS STRATEGY-----------------------------------')
print('------------------------------------------------------------------------------------')

rbfs_result = recursive_best_first_search(us_map_problem)
for node in rbfs_result.path():
    print(node.action, node.state, node.path_cost)

# 2. USING A STAR SEARCH STRATEGY
print('------------------------------------------------------------------------------------')
print('--------------------------------A* SEARCH STRATEGY----------------------------------')
print('------------------------------------------------------------------------------------')

h = memoize(us_map_problem.h, 'h')
a_star_search_solution = greedy_best_first_search_modified('A*', us_map_problem, lambda n: n.path_cost + h(n))

a_star_result = astar_search(us_map_problem, None, True)
for node in a_star_result.path():
    print(node.action, node.state, node.path_cost)


"""
-----------------------------------------------------------------------------------------
---------------------------------- EXTRA CREDIT ----------------------------------------
-----------------------------------------------------------------------------------------
"""

print('Is Heuristic consistent ? ' + str(consistent_heuristic_check(us_map_problem)))