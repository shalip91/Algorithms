from graph_package.graph import Graph
import math

"""""""""""""""""""""""""""""""""""""""""""""""""""
""""""""""""""""""""""""""""""""""""""""""""""""""
Bellman-Ford
this script will detect the shortest path 
from (u --> v) in the graph
""""""""""""""""""""""""""""""""""""""""""""""""""
"""""""""""""""""""""""""""""""""""""""""""""""""""

class Node:
    def __init__(self, name, dist, parent=None) -> None:
        self.name = name
        self.dist = dist
        self.parent = parent
        super().__init__()

def init_dist(nodes, start):
    distances = {node: Node(node, math.inf) for node in nodes}
    distances[start].dist = 0
    return distances

def relax(src, dst, w):
    if dst.dist > src.dist + w:
        dst.dist = src.dist + w
        dst.parent = src.name

def bellman_ford(g, start):
    # initiate all the node except start to INF
    distances = init_dist(g.get_vertices_names(), start)

    edges = g.get_edges()

    for _ in range(g.get_size()):
        for edge in edges:
            relax(src=distances[edge.src], dst=distances[edge.dst],
                  w=edge.weight)


    # check if there a negative cycle
    for edge in edges:
        if distances[edge.dst].dist > distances[edge.src].dist + edge.weight:
            return {}

    return {node.name: (node.parent, node.dist) for node in distances.values()}


if __name__ == '__main__':

    test_graph = {'s': {'t': 3, 'y': 5},
                  't': {'y': 2, 'x': 6},
                  'x': {'z': 11},
                  'z': {'x': 7, 's': 3},
                  'y': {'t': -1, 'x': 4, 'z': 6}
                  }

    g = Graph(container='list', directed=True)
    for src, neighbors in test_graph.items():
        for dst, w in neighbors.items():
            g.add_edge(src, dst, w)

    print(bellman_ford(g, 's'))