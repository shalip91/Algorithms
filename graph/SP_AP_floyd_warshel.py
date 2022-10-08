from graph_package.graph import Graph
import math
from SP_bellman_ford import *
from copy import deepcopy

"""""""""""""""""""""""""""""""""""""""""""""""""""
""""""""""""""""""""""""""""""""""""""""""""""""""
DIJKSTRA
this script will detect the shortest path between all pairs
O(V^3)
""""""""""""""""""""""""""""""""""""""""""""""""""
"""""""""""""""""""""""""""""""""""""""""""""""""""
def init_mat(g):
    dists = deepcopy(g.container.graph)

    # distances matrix
    for i in range(len(g.container.graph[0])):
        for j in range(len(g.container.graph[0])):
            if i == j:
                dists[i][j] = 0
            if dists[i][j] is None:
                dists[i][j] = math.inf

    # parent matrix
    parents = deepcopy(g.container.graph)
    vertices_names = g.get_vertices_names()
    for i in range(len(dists[0])):
        for j in range(len(dists[0])):
            if i is j or dists[i][j] is math.inf:
                parents[i][j] = None
            else:
                parents[i][j] = vertices_names[i]

    return dists, parents

def floyd_warshel(g):
    mat_prev, parents = init_mat(g)
    for k in range(len(mat_prev[0])):
        mat_next = mat_prev.copy()
        for i in range(len(mat_prev[0])):
            for j in range(len(mat_prev[0])):
                if i is not k and j is not k:
                    mat_next[i][j] = min(mat_prev[i][j], mat_prev[i][k]+mat_prev[k][j])
                    if mat_prev[i][j] != mat_next[i][j]:
                        parents[i][j] = parents[k][j]
    return mat_next, parents

if __name__ == '__main__':

    test_graph = {
        's': {'w': -1},
        'x': {'s': 1, 'z': 2},
        't': {'x': 2, 'y': -8},
        'y': {'x': 5, 't': 10},
        'w': {'x': 7},
        'z': {'w': 3, 's': -4}
    }

    g = Graph(graph=test_graph, container='matrix', directed=True, size=len(test_graph.keys()))
    graph_nodes = ['s', 'x', 't', 'y', 'w', 'z']

    # print(g, end='\n\n')
    dists, parents =  floyd_warshel(g)

    for i, start_point in enumerate(dists):
        print(start_point)
        print(bellman_ford(g, graph_nodes[i]))


