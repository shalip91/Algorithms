from .flow_edge import FlowEdge
from .graph import Graph


class FlowGraph(Graph):
    def __init__(self, graph=None, src='s', dst='t') -> None:
        super().__init__(graph=graph, directed=True)
        self.src = src
        self.dst = dst

    def __getitem__(self, key):
        return self.container.graph[key]

    #overriding the base class method
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
        if src not in self.container.vertices:
            self.add_vertex(src)
        if dst not in self.container.vertices:
            self.add_vertex(dst)

        # creating the 2 edges at the residual graph
        self.container.graph[src][dst] = FlowEdge(src, dst, w)
        self.container.graph[dst][src] = FlowEdge(dst, src, capacity=0)

        # assigning each of the edges to be the residuql of the other
        self.container.graph[src][dst].residual = self.container.graph[dst][src]
        self.container.graph[dst][src].residual = self.container.graph[src][dst]

    def get_edges(self):
        edges = []

        for row in self.container.graph.values():
            for edge in row.values():
                edges.append(edge)
        return edges
        # return [e for row in self.container.graph for e in row]

    def residual(self):

        return "Residual Graph\n" + "\n".join(
            [str(src) + ' -> ' + str({s: neighbor.get_flow()
                                      for s, neighbor in neighbors.items()})
             for src, neighbors in self.container.graph.items()]) + '\n'

    def __str__(self) -> str:
        return "Flow Network Graph\n" + "\n".join(
            [str(src) + ' -> ' + str({s: f'{neighbor.get_flow()}/{neighbor.get_capacity()}'
                                      for s, neighbor in neighbors.items()
                                      if not neighbor.is_residual()})
             for src, neighbors in self.container.graph.items()]) + '\n'

    def result(self):
        return f"Flow Network Graph after solving \nResult: {self.flow()}\n" + "\n".join(
            [str(src) + ' -> ' + str({s: f'{neighbor.get_flow()}/{neighbor.get_capacity()}'
                                      for s, neighbor in neighbors.items()
                                      if not neighbor.is_residual() and neighbor.get_flow()})
             for src, neighbors in self.container.graph.items()]) + '\n'

    def flow(self):
        return sum([edge.get_flow() for edge in self.container.graph[self.src].values()])