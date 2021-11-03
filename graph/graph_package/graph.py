from .graph_matrix import GraphMatrix
from .graph_list import GraphList



class Graph:
    """
    this class implements the Graph Data Structure
    -   container can be adjacency Matrix/List
    """

    GRAY = 0
    BLACK = 1

    def __init__(self,
                 graph=None,
                 vertexs=None,
                 container='list',
                 size=10,
                 directed=False) -> None:
        """Graph Constructor

        Args:
            container(str, optional): default='list' - {'list', 'matrix'}
            size(int, optional): default=10 - only in case of matrix container
            directed(bool, optional): default=True
        """
        super().__init__()
        if container == 'matrix':
            self.container = GraphMatrix(size=size, directed=directed)
        elif container == 'list':
            self.container = GraphList(directed=directed)
        if graph is not None and vertexs is None:
            self.__construct_graph_with_weightless_vertex(graph)
        if vertexs is not None and graph is not None:
            self.__construct_graph_with_weight_vertex(graph, vertexs)

    def __str__(self) -> str:
        return self.container.__str__()
    
    def __getitem__(self, key):
        return self.neighbors(key)

    def add_vertex(self, key, value=0):
        """add Vertex to the graph

        Args:
            key(any): Vertex Name
            value(int, optional): default=0, Vertex cost
        Returns:
            None
        """
        self.container.add_vertex(key, value)

    def add_edge(self, src, dst, w=1):
        """add edge to the graph. in case of missing Vertexies,
        they will be inserted automatically.

        Args:
            src: from
            dst: to
            w: edge weight, default=1
        Returns:
            None
        """
        self.container.add_edge(src, dst, w)

    def get_size(self):
        return self.container.get_size()

    def get_vertices(self):
        return self.container.get_vertices()

    def get_vertex_by_name(self, name):
        return self.container.vertices[name]

    def get_vertices_names(self):
        return self.container.get_vertices_names()

    def get_edges(self):
        return self.container.get_edges()

    def get_distance(self, src, dst):
        return self.container.graph[src][dst]

    def remove_vertex(self, key):
        """will remove the vertex (if exists)

        Args:
            key: vertex name
        Returns:
            None
        """
        self.container.remove_vertex(key)

    def remove_edge(self, src, dst):
        """will remove the edge

        Args:
            src: from vertex
            dst: to vertex
        Returns:
            None
        """
        self.container.remove_edge(src, dst)

    def neighbors(self, key):
        """this function will get all the neighbors names.

        Args:
            key: vertex name
        Returns:
            list of neighbors names
        """
        return self.container.neighbors(key)

    def degree(self, key):
        """return the number of in/out-degree in case of directed graphs
        return the number of degree in case of indirected graph.

        Args:
            key: vertex name
        Returns:
            degree of the vertex
        """
        return self.container.degree(key)

    def has_cycle(self):
        if self.container.directed:
            return self.__has_cycle_directed()
        return self.__has_cycle_undirected()

    def __has_cycle_directed(self):
        """this is an exploration DFS to search for cycles in graph

        Args:
            g: Graph
        Returns:
            list of cycles
        """

        def dfs_helper(src):
            nonlocal visited
            for dst in self.neighbors(src):
                if dst.key not in visited:
                    # white node
                    visited[dst.key] = self.GRAY
                    if dfs_helper(dst.key):
                        return True
                elif visited[dst.key] == self.GRAY:
                    # gray node - cycle found
                    return True

            visited[src] = self.BLACK
            return False

        visited = {}
        for start in self.get_vertices():
            # 0 - gray: in processes, 1 - black: finished
            visited[start.key] = self.GRAY
            if dfs_helper(start.key):
                return True

        return False

    def __has_cycle_undirected(self):
        """this is an exploration DFS to search for cycles in graph

        Args:
            g: Graph
            start: starting node
        Returns:
            list of cycles
        """
        visited = [self.get_vertices()[0].key]

        def dfs_helper(src, parent):
            nonlocal visited
            for dst in self.neighbors(src):
                if dst.key not in visited:
                    visited.append(dst.key)
                    if dfs_helper(dst.key, src):
                        return True
                elif dst.key != parent:
                    return True

            return False

        return dfs_helper(self.get_vertices()[0].key, None)

    def __construct_graph_with_weightless_vertex(self, graph):
        for k in graph.keys():
            self.add_vertex(k)
        for src, neighbors in graph.items():
            for dst, w in neighbors.items():
                self.add_edge(src, dst, w)

    def __construct_graph_with_weight_vertex(self, graph, vertexs):
        for k, v in vertexs.items():
            self.add_vertex(k, v)
        for src, neighbors in graph.items():
            for dst, w in neighbors.items():
                self.add_edge(src, dst, w)