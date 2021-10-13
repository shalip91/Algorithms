from graph_package.graph import Graph
import numpy as np


"""""""""""""""""""""""""""""""""""""""""""""""""""
""""""""""""""""""""""""""""""""""""""""""""""""""
this script will detect cycles in the graph
""""""""""""""""""""""""""""""""""""""""""""""""""
"""""""""""""""""""""""""""""""""""""""""""""""""""

def has_cycle(g, start):
    """this is an exploration DFS to search for cycles in graph

    Args:
        g: Graph
        start: starting node
    Returns:
        list of cycles
    """
    visited = [start]
    def dfs_helper(src, parent):
        nonlocal visited
        for dst in g[src]:
            if dst.key not in visited:
                visited.append(dst.key)
                if (dfs_helper(dst.key, src)):
                    return True
            elif dst.key != parent:
                return True

        return False

    return dfs_helper(start, None)


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
    g = Graph(container='matrix')
    for src, neighbors in test_graph.items():
        for dst, _ in neighbors.items():
            g.add_edge(src, dst)



    print(f'has cycle: {has_cycle(g, "s")}')
    print(f'has cycle: {g.has_cycle()}')
