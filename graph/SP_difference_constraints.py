import pandas as pd
import math
from graph_package.graph import Graph
from SP_bellman_ford import *
from collections import defaultdict

"""""""""""""""""""""""""""""""""""""""""""""""""""
""""""""""""""""""""""""""""""""""""""""""""""""""
Bellman-Ford
this script will detect the shortest path 
from (u --> v) in the graph
""""""""""""""""""""""""""""""""""""""""""""""""""
"""""""""""""""""""""""""""""""""""""""""""""""""""


if __name__ == '__main__':

    df = pd.read_csv("data/diff_constraints.csv", header=None).T
    nums = list(df[0])


    test_graph = defaultdict(dict)
    for i in range(0, len(nums), 3):
        test_graph[nums[i+1]][nums[i]] = -1*nums[i+2]
    print(nums)
    print(test_graph)

    g = Graph(container='list', directed=True)
    for src, neighbors in test_graph.items():
        for dst, w in neighbors.items():
            g.add_edge(src, dst, w)

    g.add_vertex(0)
    for v in g.get_vertices():
        if v.key != 0:
            g.add_edge(0, v.key, w=0)

    print(g)
    print(bellman_ford(g, 0))
