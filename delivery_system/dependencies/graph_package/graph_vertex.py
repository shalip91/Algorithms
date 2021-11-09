class Vertex():
    def __init__(self, key, idx, weight=0) -> None:
        self.key = key
        self.idx = idx
        self.weight = weight

    def __eq__(self, other):
        return self.key == other.key

    def __le__(self, other):
        return self.weight <= other.weight

    def __lt__(self, other):
        return self.weight < other.weight

    def __ge__(self, other):
        return not self.__lt__(other)

    def __gt__(self, other):
        return not self.__le__(other)

    def __str__(self) -> str:
        return f'vertex: {self.key}\t vertex_data: {self.weight}'


