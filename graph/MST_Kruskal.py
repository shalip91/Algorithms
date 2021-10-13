from graph_package.graph import Graph
from collections import defaultdict

"""""""""""""""""""""""""""""""""""""""""""""""""""
""""""""""""""""""""""""""""""""""""""""""""""""""
this script will detect cycles in the graph
""""""""""""""""""""""""""""""""""""""""""""""""""
"""""""""""""""""""""""""""""""""""""""""""""""""""

class UnionFind:
    def __init__(self) -> None:
        super().__init__()
        self.representor = {}

    def make_set(self, key):
        self.representor[key] = key

    def find(self, key):
        return self.representor[key]

    def union(self, x, y):
        x_r, y_r = self.find(x), self.find(y)
        for k, r in self.representor.items():
            if r == y_r:
                self.representor[k] = x_r


def kruskal(g):
    """this algorithm finds the minimum spanning tree.
        in case disconnected graph, it will find all the
        minimum stpanning trees

        Args:
            g - graph
        Return:
            list of trees. each tree is a list of edges. edge = (from, to, weight)
    """
    uf = UnionFind()
    trees = defaultdict(list)
    taken_adges = []
    edges = sorted(g.get_edges(), key=lambda x: x.weight)

    for v in g.get_vertices():
        uf.make_set(v.key)
    for edge in edges:
        if uf.find(edge.src) != uf.find(edge.dst):
            taken_adges.append(edge)
            uf.union(edge.src, edge.dst)

    # in case of disconnected graph, multiple trees will result.
    for edge in taken_adges:
        trees[uf.find(edge.src)] += [(edge.src, edge.dst, edge.weight)]

    return [tree for _, tree in dict(trees).items()]


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

    g = Graph(container='list')
    for src, neighbors in test_graph.items():
        for dst, w in neighbors.items():
            g.add_edge(src, dst, w)

    print(kruskal(g))

