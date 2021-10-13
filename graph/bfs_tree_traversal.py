import numpy as np
import pandas as pd
from graph_package.graph import Graph



def bfs(g, src, dst=None):
    """return the list of tuple(parent, distance) or
    shortest path to the dst

    Args:
        g: graph
        src: starting vertex
    Returns:
        if dst=None - list of tuple(parent, distance from start) / dst=dst - shortest path from src to dst
    """
    visited = []
    q =[]
    parent = {src: ('non', 0)}

    def bfs_helper(v):
        visited.append(v)
        q.append(v)
        while q:
            s = q.pop(0)
            for neighbour in g[s]:
                if neighbour.key not in visited:
                    visited.append(neighbour.key)
                    parent[neighbour.key] = (s, parent[s][1] + 1)
                    q.append(neighbour.key)


    bfs_helper(src)
    # return the parents list
    if dst is None:
        return parent

    # returns the shortest path to the dst
    path_to_dst = [dst]
    while parent[dst][1]:
        path_to_dst.append(parent[dst][0])
        dst = parent[dst][0]

    return path_to_dst[::-1]


if __name__ == '__main__':

    df = pd.read_csv("data/delivery_map.csv")
    vertexes = list(df['Unnamed: 0'])

    galaxy_graph = Graph(container='matrix')

    for src in vertexes:
        galaxy_graph.add_vertex(src)

    for src in vertexes:
        for i, w in enumerate(list(df[src])):
            if w != 0:
                galaxy_graph.add_edge(src, vertexes[i])

    parent = bfs(galaxy_graph, 'rigel')
    for dst in ['acturus', 'sol', 'pollux', 'vega']:
        if parent[dst][1] <= 1:
            print(f'{dst} length: {parent[dst][1]}')

    print(bfs(galaxy_graph, 'polaris', 'vega'))


