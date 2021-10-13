from graph_package.graph import Graph
from dfs_topologic_sort import topological_sort, dfs
import math
"""""""""""""""""""""""""""""""""""""""""""""""""""
""""""""""""""""""""""""""""""""""""""""""""""""""
this script will detect the shortest path 
from (u --> v) in the graph
""""""""""""""""""""""""""""""""""""""""""""""""""
"""""""""""""""""""""""""""""""""""""""""""""""""""



def init_dist(nodes, start):
    distances = {node: (math.inf, None) for node in nodes}
    distances[start] = (0, None)
    return distances

def relex(distances, src, dst, src_dist, dst_dist, w):
    if dst_dist > src_dist + w:
        distances[dst] = (src_dist + w, src)


def shortest_path_dag(g, start):
    sorted_nodes = topological_sort(g)
    distances = init_dist(sorted_nodes, start)
    for node in sorted_nodes:
        for neighbor in g[node]:
            relex(distances=distances,
                  src=node, dst=neighbor.key,
                  src_dist=distances[node][0], dst_dist=distances[neighbor.key][0],
                  w=g.container.graph[node][neighbor.key])

    return distances


if __name__ == '__main__':

    test_graph = {'r': {'s': 5, 't': 3},
                  's': {'x': 6, 't': 2},
                  't': {'x': 7, 'y': 4, 'z': 2},
                  'x': {'z': 1, 'y': -1},
                  'y': {'z': -2},
                  'z': {}
                  }

    g = Graph(container='list', directed=True)
    for src, neighbors in test_graph.items():
        for dst, w in neighbors.items():
            g.add_edge(src, dst, w)

    # print(g)
    print(shortest_path_dag(g, 's'))
    # print(test_graph['r']['s'])


