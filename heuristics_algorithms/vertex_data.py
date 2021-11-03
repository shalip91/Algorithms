import math


class VertexData:
    def __init__(self, h):
        self.parent = None
        self.g = math.inf  # distance to start node
        self.h = h  # distance to goal node
        self.f = h  # total cost

    def __le__(self, other):
        return self.f <= other.f

    def __lt__(self, other):
        return self.f < other.f

    def __ge__(self, other):
        return not self.__lt__(other)

    def __gt__(self, other):
        return not self.__le__(other)

    def __str__(self):
        return f'parent: {self.parent}, f_val: {self.f}'

