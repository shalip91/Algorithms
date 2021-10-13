# from graph_package.graph import Graph
from graph_package.graph import Graph
import numpy as np
import heapq

"""""""""""""""""""""""""""""""""""""""""""""""""""
""""""""""""""""""""""""""""""""""""""""""""""""""
this script will detect cycles in the graph
""""""""""""""""""""""""""""""""""""""""""""""""""
"""""""""""""""""""""""""""""""""""""""""""""""""""


def chosen_edge(min_heap, visited):
    edge = heapq.heappop(min_heap)
    while edge[1][1] in visited:
        try:
            edge = heapq.heappop(min_heap)
        except IndexError:
            return False
    return edge


def prim_connected_component(g, start, visited):
    # creating the heap with the neigbhors of the start node
    min_heap = [(g.container.graph[start][dst.key], (start, dst.key)) for dst in g[start]]

    visited.append(start)
    taken_edges = []
    heapq.heapify(min_heap)

    # taking the next, unconncted edge
    new_edge = chosen_edge(min_heap, visited)
    while new_edge:
        # adding the vertex to the visited list
        new_vertex = new_edge[1][1]
        visited.append(new_vertex)

        # inserting the edge to the tree
        taken_edges.append(new_edge)
        for dst in g[new_vertex]:
            heapq.heappush(min_heap, (g.container.graph[new_vertex][dst.key], (new_vertex, dst.key)))

        new_edge = chosen_edge(min_heap, visited)

    return taken_edges


def prim(g):
    visited = []
    trees = []
    for start in g.get_vertices():
        if start.key not in visited:
            trees.append(prim_connected_component(g, start.key, visited))

    return trees


if __name__ == '__main__':

    test_graph = {'a': {'b': 4, 'h': 8},
                  'b': {'a': 4, 'h': 11, 'c': 8},
                  'c': {'b': 8, 'i': 2, 'f': 4, 'd': 7},
                  'd': {'c': 7, 'f': 14, 'e': 9},
                  'e': {'d': 9, 'f': 10},
                  'f': {'e': 10, 'd': 14, 'c': 4, 'g': 2},
                  'g': {'f': 2, 'i': 6, 'h': 1},
                  'h': {'i': 7, 'g': 1, 'b': 11, 'a': 8},
                  'i': {'c': 2, 'g': 6, 'h': 7},
                  'x': {'w': 10},
                  'w': {}
                  }

    g = Graph(container='list', size=11)
    for src, neighbors in test_graph.items():
        for dst, w in neighbors.items():
            g.add_edge(src, dst, w)

    print(g)
    print(prim(g))



