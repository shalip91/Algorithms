from abc import ABC, abstractmethod

class GraphInterface(ABC):
    def __init__(self) -> None:
        super().__init__()

    def __str__(self) -> str:
        return f'the graph representation is: \n'

    @abstractmethod
    def add_vertex(self, key, value=0):
        pass

    @abstractmethod
    def get_vertices(self):
        pass

    @abstractmethod
    def get_vertices_names(self):
        pass

    @abstractmethod
    def get_edges(self):
        pass

    @abstractmethod
    def get_size(self):
        pass

    @abstractmethod
    def add_edge(self, src, dst, w=1):
        pass

    @abstractmethod
    def neighbors(self, key):
        pass

    @abstractmethod
    def remove_vertex(self, key):
        pass

    @abstractmethod
    def remove_edge(self, src, dst):
        pass

    @abstractmethod
    def degree(self, key):
        pass




