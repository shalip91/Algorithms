from .graph_interface import GraphInterface
from .graph_vertex import Vertex
from .graph_edge import Edge

class GraphMatrix(GraphInterface):
    def __init__(self, size=10, directed=False) -> None:
        super().__init__()
        self.max_size = size
        self.graph = [[None] * size for row in range(size)]
        self.directed = directed
        self.vertices = {}
        self.idx_to_key = {}

    def __str__(self) -> str:
        return super().__str__() + "\n".join([str(row) for row in self.graph])

    def add_vertex(self, key, value=0):
        """
        this function will add Vertex to the graph
        :param key:
        :param value:
        :return: None
        """
        if self.max_size == len(self.vertices):
            raise Exception("max size exceeded")
        if key in self.vertices:
            raise Exception("already exist")

        num_of_vertices = len(self.vertices)
        self.vertices[key] = Vertex(key, num_of_vertices, value)
        self.idx_to_key[num_of_vertices] = key

    def get_size(self):
        return len(self.graph[0])

    def get_vertices(self):
        return list(self.vertices.values())

    def get_vertices_names(self):
        return list(self.vertices.keys())

    def add_edge(self, src, dst, w=1):
        """
        this funcion will add edge to the graph.
        in case of missing Vertexies, they will be inserted automatically.
        :param src:
        :param dst:
        :param w:
        :return: None
        """
        # adding the vertexies if not exist
        if src not in self.vertices:
            self.add_vertex(src)
        if dst not in self.vertices:
            self.add_vertex(dst)
        # assigning the weight of the edge
        self.graph[self.vertices[src].idx][self.vertices[dst].idx] = w
        if not self.directed:
            self.graph[self.vertices[dst].idx][self.vertices[src].idx] = w

    def get_edges(self):
        edges = []
        for i in range(self.max_size):
            # in case of undirected graph, take only the upper diagonal matrix's edges
            start = i if self.directed is False else 0
            for j in range(start, self.max_size):
                if self.graph[i][j] is not None:
                    # appending [from, to, weight]
                    edges.append(
                        Edge(self.idx_to_key[i], self.idx_to_key[j], self.graph[i][j]))
        return edges

    def neighbors(self, key):
        """
        this function will get all the neighbors names.
        :param key:
        :return: list of neighbors names
        """
        if key not in self.vertices:
            raise Exception("Not exist")

        return [self.vertices[self.idx_to_key[j]]
                for j, w in enumerate(self.graph[self.vertices[key].idx])
                if w is not None]

    def remove_vertex(self, key):
        """
        will remove the vertex (if exists)
        :param key:
        :return: None
        """
        if key in self.vertices:
            """ reseting the columns and rows of the Vertex """
            ver_idx = self.vertices[key].idx
            self.graph[ver_idx] = [None] * self.max_size
            for row in self.graph:
                row[ver_idx] = None
            """removing the vertex from the dictionaries"""
            del self.vertices[key]
            del self.idx_to_key[ver_idx]

    def remove_edge(self, src, dst):
        """
        will remove the edge
        :param src: from vertex
        :param dst: to vertex
        :return: None
        """
        if 0 <= src < self.max_size and 0 <= dst < self.max_size:
            self.graph[self.vertices[src].idx][self.vertices[dst].idx] = None
            if not self.directed:
                self.graph[self.vertices[dst].idx][self.vertices[src].idx] = None

    def degree(self, key):
        """
        will return the number of in/out-degree in case of directed graphs
        will return the number of degree in case of indirected graph.
        :param key:
        :return: degree
        """
        degree = sum([1 for w in self.graph[self.vertices[key].idx] if w is not None])
        if self.directed:
            incoming_edges = [self.graph[i][self.vertices[key].idx] for i in range(self.max_size)]
            in_degree = sum([1 for w in incoming_edges if w is not None])
            out_degree = degree
            return in_degree, out_degree
        else:
            return degree

if __name__ == '__main__':

    g = GraphMatrix(size=4)
    g.add_vertex('s')
    g.add_vertex('e')
    g.add_vertex('i')
    g.add_vertex('y')

    g.add_edge('s', 'i', w=5)
    g.add_edge('s', 'y')
    g.add_edge('y', 'e')
    g.add_edge('e', 'i')

    print(g.get_vertices())
    g.remove_vertex('s')
    print(g.get_vertices())
    print(g.neighbors('i'))



































# from graph_package.graph import Graph
# import math
# from SP_bellman_ford import *
#
# """""""""""""""""""""""""""""""""""""""""""""""""""
# """"""""""""""""""""""""""""""""""""""""""""""""""
# DIJKSTRA
# this script will detect the shortest path
# from (u --> v) in the graph
# """"""""""""""""""""""""""""""""""""""""""""""""""
# """""""""""""""""""""""""""""""""""""""""""""""""""
# def init_mats(g):
#     dists = g.container.graph.copy()
#
#     # distances matrix
#     for i in range(len(g.container.graph[0])):
#         for j in range(len(g.container.graph[0])):
#             if i == j:
#                 dists[i][j] = 0
#             if dists[i][j] is None:
#                 dists[i][j] = math.inf
#
#     # parent matrix
#     parents = g.container.graph.copy()
#     for i in range(len(dists[0])):
#         for j in range(len(dists[0])):
#             if i is j or dists[i][j] is math.inf:
#                 parents[i][j] = None
#             else:
#                 parents[i][j] = i
#
#     return dists, parents
#
# def floyd_warshel(g):
#     mat_prev, mat_parent = init_mats(g)
#     for k in range(len(mat_prev[0])):
#         mat_next = mat_prev.copy()
#         for i in range(len(mat_prev[0])):
#             for j in range(len(mat_prev[0])):
#                 if i is not k and j is not k:
#                     mat_next[i][j] = min(mat_prev[i][j], mat_prev[i][k]+mat_prev[k][j])
#                     if mat_next[i][j] != mat_prev[i][j]:
#                         mat_parent[i][j] = mat_parent[k][j]
#     return mat_next, mat_parent
#
# if __name__ == '__main__':
#
#     test_graph = {
#         's': {'w': -1},
#         'x': {'s': 1, 'z': 2},
#         't': {'x': 2, 'y': -8},
#         'y': {'x': 5, 't': 10},
#         'w': {'x': 7},
#         'z': {'w': 3, 's': -4}
#     }
#
#     g = Graph(graph=test_graph, container='matrix', directed=True, size=len(test_graph.keys()))
#     graph_nodes = ['s', 'x', 't', 'y', 'w', 'z']
#
#     print(g, end='\n\n')
#     distances, parents =  floyd_warshel(g)
#
#     for i, start_point in enumerate(distances):
#         print(start_point)
#         print(bellman_ford(g, graph_nodes[i]))






