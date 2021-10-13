from graph_package.graph import Graph
import numpy as np


"""""""""""""""""""""""""""""""""""""""""""""""""""
""""""""""""""""""""""""""""""""""""""""""""""""""
this script will find the SCC of a graph
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


def find_SSC(g):
    # getting the order of closing time with DFS
    stack = []
    for v in g.get_vertices():
        if v.key not in stack:
            stack.extend(dfs(g, v.key, stack.copy()))

    # transposing the matrix
    mat = g.container.graph
    g.container.graph = np.array(mat).T.tolist()

    # apply DFS again on each SCC
    ssc_list = []
    visited = []
    for v in stack[::-1]:
        if v not in visited:
            ssc = dfs(g, v, visited)
            ssc_list.append(ssc)
            visited.extend(ssc.copy())

    return ssc_list




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

    # MUST be matrix. we dont support transpose on list
    g = Graph(directed=True, container='matrix')
    for src, neighbors in test_graph.items():
        for dst, _ in neighbors.items():
            g.add_edge(src, dst)


    print(f'SCC: {find_SSC(g)}')
