from graph_package.graph import Graph
import math

"""""""""""""""""""""""""""""""""""""""""""""""""""
""""""""""""""""""""""""""""""""""""""""""""""""""
DIJKSTRA
this script will detect the shortest path 
from (u --> v) in the graph
""""""""""""""""""""""""""""""""""""""""""""""""""
"""""""""""""""""""""""""""""""""""""""""""""""""""

class DijkstraNode:

    def __init__(self, name, dist, parent=None) -> None:
        self.name = name
        self.dist = dist
        self.parent = parent
        super().__init__()

def init_dist(nodes, start):
    distances = {node: DijkstraNode(node, math.inf) for node in nodes}
    distances[start].dist = 0
    return distances

def relax(src, dst, w):
    if dst.dist > src.dist + w:
        dst.dist = src.dist + w
        dst.parent = src.name

def dijkstra(g, start):
    # initiate all the node except start to INF
    distances = init_dist(g.get_vertices_names(), start)
    result = {start: DijkstraNode(name=start, dist=0)}
    while distances:
        closest = min(distances, key=lambda node: distances[node].dist)
        result[closest] = (distances[closest].parent,
                           distances[closest].dist)
        for dst in g[closest]:
            if dst.key in distances:
                relax(src=distances[closest], dst=distances[dst.key],
                      w=g.container.graph[closest][dst.key])

        del distances[closest]

    return result


if __name__ == '__main__':

    test_graph = {'s': {'t': 3, 'y': 5},
                  't': {'y': 2, 'x': 6},
                  'x': {'z': 11},
                  'z': {'x': 7, 's': 3},
                  'y': {'t': -3, 'x': 4, 'z': 6}
                  }

    g = Graph(container='list', directed=True)
    for src, neighbors in test_graph.items():
        for dst, w in neighbors.items():
            g.add_edge(src, dst, w)

    print(dijkstra(g, 'y'))