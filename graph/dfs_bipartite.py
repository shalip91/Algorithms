from graph_package.graph import Graph
import numpy as np


"""""""""""""""""""""""""""""""""""""""""""""""""""
""""""""""""""""""""""""""""""""""""""""""""""""""
this script will detect cycles in the graph
""""""""""""""""""""""""""""""""""""""""""""""""""
"""""""""""""""""""""""""""""""""""""""""""""""""""


def bipartite(g):
    """this is an exploration DFS to search for cycles in graph

    Args:
        g: Graph
    Returns:
        list of cycles
    """

    def dfs_helper(src, color):
        nonlocal visited
        for dst in g[src]:
            if dst.key not in visited:
                # white node
                visited[dst.key] = color
                if dfs_helper(dst.key, not color) == []:
                    return []
            elif visited[dst.key] != color:
                return []


    visited = {}
    color = True
    for start in g.get_vertices():
        # 0 - gray: in processes, 1 - black: finished
        if start.key not in visited:
            visited[start.key] = color
            if dfs_helper(start.key, not color) == []:
                return []

    return [[node for node, color in visited.items() if color],
            [node for node, color in visited.items() if not color]]


if __name__ == "__main__":
    bipartite_graph = {'s': {'w': 1, 'x': 1},
                       'w': {'s': 1, 'v': 1},
                       'x': {'s': 1, 'v': 1},
                       'v': {'w': 1, 'x': 1}}

    g = Graph(container='matrix')
    for src, neighbors in bipartite_graph.items():
        for dst, _ in neighbors.items():
            g.add_edge(src, dst)


    # print(g)
    print(f'bipartite devision: {bipartite(g)}')
    # print(f'has cycle: {g.has_cycle()}')
