from utils import *
from search import *
from search_modified import *

graph_dict = dict(
    S=dict(A=1, B=2, C=3),
    A=dict(H=5, D=1),
    B=dict(D=2, E=1),
    C=dict(E=3, F=2),
    H=dict(G=1),
    D=dict(H=3, G=3),
    E=dict(G=4),
    F=dict(E=6)
)

p1_graph = Graph(graph_dict=graph_dict, directed=True)

p1_graph.locations = dict(
    S=(0, 5),
    A=(0, 4),
    B=(0, 5),
    C=(0, 3),
    D=(0, 3),
    E=(0, 4),
    F=(0, 2),
    G=(0, 0),
    H=(0, 1)
)


class P1Problem(Problem):
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

initial = 'B'
goal = 'G'
p1_problem = P1Problem(initial, goal, p1_graph)

uniform_cost_search_solution = uniform_cost_search_modified(p1_problem, lambda n: n.path_cost)
for node in uniform_cost_search_solution.path():
    print(node.action, node.state, node.path_cost)


print('Is Heuristic consistent ? ' + str(consistent_heuristic_check(p1_problem)))