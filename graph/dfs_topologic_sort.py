from graph_package.graph import Graph
import numpy as np


"""""""""""""""""""""""""""""""""""""""""""""""""""
""""""""""""""""""""""""""""""""""""""""""""""""""
this script will run the topologic sort in case of 
DAG - Directed acyclic graphs - HAS TO BE DAG !!!
""""""""""""""""""""""""""""""""""""""""""""""""""
"""""""""""""""""""""""""""""""""""""""""""""""""""

def dfs(g, start, visited=None):
    """this is an exploration DFS, meanning it will return a list of
    all the reachable Nodes starting from 'start'

    Args:
        g: Graph
        start: starting node
        visited: default=None, supplying the unwanted list of node to explore
    """
    if visited is None:
        visited = []
    visited.append(start)
    stack = []

    def dfs_helper(src):
        nonlocal stack, visited
        for dst in g[src]:
            if dst.key not in visited:
                visited.append(dst.key)
                dfs_helper(dst.key)
        stack.append(src)

    dfs_helper(start)
    return stack


def topological_sort(g):
    """ creating the topo

    Args:
        g: graph
    Returns:
        list of nodes with descending closing times
    """
    stack = []
    for v in g.get_vertices():
        if v.key not in stack:
            stack.extend(dfs(g, v.key, stack.copy()))

    return stack[::-1]


if __name__ == "__main__":
    test_graph = {'s': {'v': 1},
                  'v': {'w': 1},
                  'w': {'s': 1},
                  'q': {'w': 1, 's': 1, 't': 1},
                  't': {'x': 1, 'y': 1},
                  'x': {'z': 1},
                  'z': {'x': 1},
                  'y': {'q': 1},
                  'r': {'u': 1, 'y': 1},
                  'u': {'y': 1}
                  }
    g = Graph(directed=True, container='list')
    for src, neighbors in test_graph.items():
        for dst, _ in neighbors.items():
            g.add_edge(src, dst)


    print(f'topological sort:\n{topological_sort(g)}')
