from graph_package.graph import Graph
import numpy as np


"""""""""""""""""""""""""""""""""""""""""""""""""""
""""""""""""""""""""""""""""""""""""""""""""""""""
this script will detect cycles in the graph
""""""""""""""""""""""""""""""""""""""""""""""""""
"""""""""""""""""""""""""""""""""""""""""""""""""""

GRAY = 0
BLACK = 1


def has_cycle(g):
    """this is an exploration DFS to search for cycles in graph

    Args:
        g: Graph
    Returns:
        list of cycles
    """

    def dfs_helper(src):
        nonlocal visited
        for dst in g[src]:
            if dst.key not in visited:
                # white node
                visited[dst.key] = GRAY
                if dfs_helper(dst.key):
                    return True
            elif visited[dst.key] == GRAY:
                # gray node - cycle found
                return True

        visited[src] = BLACK
        return False

    visited = {}
    for start in g.get_vertices():
        # 0 - gray: in processes, 1 - black: finished
        visited[start.key] = GRAY
        if dfs_helper(start.key):
            return True

    return False


if __name__ == "__main__":
    # test_graph = {'s': {'v': 1},
    #               'v': {'w': 1},
    #               'w': {'s': 1},
    #               'q': {'w': 1, 's': 1, 't': 1},
    #               't': {'x': 1, 'y': 1},
    #               'x': {'z': 1},
    #               'z': {'x': 1},
    #               'y': {'q': 1},
    #               'r': {'u': 1, 'y': 1},
    #               'u': {'y': 1}
    #               }

    test_graph = {
        0: {1: 1},
        1: {},
        2: {1: 1, 3: 1},
        3: {4: 1},
        4: {0: 1 , 2: 1}
    }
    g = Graph(directed=True, container='matrix')
    for src, neighbors in test_graph.items():
        for dst, _ in neighbors.items():
            g.add_edge(src, dst)


    print(g)
    print(f'has cycle: {has_cycle(g)}')
    print(f'has cycle: {g.has_cycle()}')
