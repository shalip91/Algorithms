from .graph_interface import GraphInterface
from .graph_vertex import Vertex
from .graph_edge import Edge

class GraphList(GraphInterface):
    def __init__(self, directed=False) -> None:
        super().__init__()
        self.directed = directed
        self.graph = {}
        self.vertices = {}
        self.size = 0

    def __str__(self) -> str:
        return super().__str__() \
               + "\n".join([str(src) + ' -> '
                            + str(neighbors) for src, neighbors in self.graph.items()])

    def add_vertex(self, key, value=0):
        """
        this function will add Vertex to the graph
        :param key: vertex name
        :param value: default=0
        :return: None
        """
        if key in self.vertices:
            raise Exception("already exist")
        # creating the vertex
        self.vertices[key] = Vertex(key, 0, value)
        self.graph[key] = {}
        self.size += 1

    def get_size(self):
        return self.size

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
        self.graph[src][dst] = w
        if not self.directed:
            self.graph[dst][src] = w

    def get_edges(self):
        edges = []
        visited = []
        for src, neighbors in self.graph.items():
            visited.append(src)
            for dst, w in neighbors.items():
                if dst in visited and self.directed is False:
                    continue
                edges.append(Edge(src, dst, w))

        return edges

    def neighbors(self, key):
        """
        this function will get all the neighbors names.
        :param key:
        :return: list of neighbors names
        """
        if key not in self.vertices:
            raise Exception("Not exist")

        return [self.vertices[neighbor] for neighbor in self.graph[key].keys()]

    def remove_vertex(self, vertex_to_rmv):
        """
        will remove the vertex (if exists)
        :param key:
        :return: None
        """
        if vertex_to_rmv in self.vertices:
            # removing the vertex from the dictionaries
            del self.vertices[vertex_to_rmv]
            # removing the outgoing edges
            del self.graph[vertex_to_rmv]
            # removing the incoming edges
            for src, neighbors in self.graph.items():
                if vertex_to_rmv in neighbors:
                    del neighbors[vertex_to_rmv]

    def remove_edge(self, src, dst):
        """
        will remove the edge
        :param src: from vertex
        :param dst: to vertex
        :return: None
        """
        if src in self.graph and dst in self.graph[src]:
            del self.graph[src][dst]
            if not self.directed:
                del self.graph[dst][src]

    def degree(self, key):
        """
        will return the number of in/out-degree in case of directed graphs
        will return the number of degree in case of indirected graph.
        :param key:
        :return: degree for undirected /  Tuple(in_degree, out_degree) for directed
        """
        degree = len(self.graph[key])
        if self.directed:
            in_degree = sum([sum([1 for dst, _ in neighbors.items() if dst is key])
                             for _, neighbors in self.graph.items()])
            out_degree = degree
            return in_degree, out_degree
        else:
            return degree

if __name__ == '__main__':

    g = GraphList(directed=True)
    g.add_vertex('s')
    g.add_vertex('e')
    g.add_vertex('i')
    g.add_vertex('y')

    g.add_edge('s', 'i', w=5)
    g.add_edge('s', 'y')
    g.add_edge('y', 'e')
    g.add_edge('e', 'i')
    g.add_edge('i', 's')
    g.add_edge('i', 'e')
    g.add_edge('i', 'y')

    # g.remove_vertex('i')
    # g.remove_edge('s', 'i')
    # g.remove_edge('y', 'e')
    print(g.neighbors('e'))
    # print(g.degree('i'))  # print(g.get_neighbors('i'))
    # g.degree()
    # g.remove_edge()










