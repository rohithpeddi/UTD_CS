"""From Taha 'Introduction to Operations Research', example 6.4-2."""

from __future__ import print_function
from ortools.graph import pywrapgraph

def main():
  """MaxFlow simple interface example."""

  # Define three parallel arrays: start_nodes, end_nodes, and the capacities
  # between each pair. For instance, the arc from node 0 to node 1 has a
  # capacity of 20.

  #start_nodes = [0, 1, 2, 0, 0, 1, 1, 2, 3, 3, 4, 5, 6, 4, 5, 5, 6, 6, 6, 7, 8, 9, 10, 8, 8, 9, 9, 10, 11, 11, 12, 13, 14 ]
  #end_nodes = [1, 2, 3, 4, 5, 5, 6, 6, 6, 7, 5, 6, 7, 8, 8, 9, 9, 10, 11, 11, 9, 10, 11, 12, 13, 13, 14, 14, 14, 15, 13, 14, 15]

  start_nodes = [0, 1, 2, 0, 0, 1, 1, 2, 3, 3, 4, 5, 6, 4, 5, 5, 6, 6, 6, 7, 8, 9, 10, 8, 8, 9, 9, 10, 11, 11, 12, 13, 14, 1, 2, 3, 4, 5, 5, 6, 6, 6, 7, 5, 6, 7, 8, 8, 9, 9, 10, 11, 11, 9, 10, 11, 12, 13, 13, 14, 14, 14, 15, 13, 14, 15]
  end_nodes =   [1, 2, 3, 4, 5, 5, 6, 6, 6, 7, 5, 6, 7, 8, 8, 9, 9, 10, 11, 11, 9, 10, 11, 12, 13, 13, 14, 14, 14, 15, 13, 14, 15, 0, 1, 2, 0, 0, 1, 1, 2, 3, 3, 4, 5, 6, 4, 5, 5, 6, 6, 6, 7, 8, 9, 10, 8, 8, 9, 9, 10, 11, 11, 12, 13, 14]
  #capacities = [12, 16, 4, 10, 6, 1, 4, 1, 12, 1, 6, 4, 8, 4, 12, 4, 10, 4, 12, 20, 15, 12, 14, 10, 8, 12, 20, 6, 16, 10, 16, 18, 16, 12, 16, 4, 10, 6, 1, 4, 1, 12, 1, 6, 4, 8, 4, 12, 4, 10, 4, 12, 20, 15, 12, 14, 10, 8, 12, 20, 6, 16, 10, 16, 18, 16]
  capacities = [4, 16, 4, 10, 6, 1, 4, 1, 12, 1, 12, 12, 8, 4, 12, 18, 10, 4, 6, 10, 15, 12, 14, 10, 8, 12, 20, 6, 16, 20, 16, 4, 16, 4, 16, 4, 10, 6, 1, 4, 1, 12, 1, 12, 12, 8, 4, 12, 18, 10, 4, 6, 10, 15, 12, 14, 10, 8, 12, 20, 6, 16, 20, 16, 4, 16]

  # Instantiate a SimpleMaxFlow solver.
  max_flow = pywrapgraph.SimpleMaxFlow()
  # Add each arc.
  for i in range(0, len(start_nodes)):
    capacity = capacities[i]
    #capacity = min(capacity, 10)
    max_flow.AddArcWithCapacity(start_nodes[i], end_nodes[i], capacity)

  # Find the maximum flow between node 0 and node 4.
  if max_flow.Solve(9, 10) == max_flow.OPTIMAL:
    print('Max flow:', max_flow.OptimalFlow())
    print('')
    print('  Arc    Flow / Capacity')
    for i in range(max_flow.NumArcs()):
      print('%1s -> %1s   %3s  / %3s' % (
          max_flow.Tail(i),
          max_flow.Head(i),
          max_flow.Flow(i),
          max_flow.Capacity(i)))
    print('Source side min-cut:', max_flow.GetSourceSideMinCut())
    print('Sink side min-cut:', max_flow.GetSinkSideMinCut())
  else:
    print('There was an issue with the max flow input.')

if __name__ == '__main__':
  main()