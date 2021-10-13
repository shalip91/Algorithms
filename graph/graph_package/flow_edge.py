class FlowEdge:
    def __init__(self, src, dst, capacity=0) -> None:
        self.src = src
        self.dst = dst
        self.flow = 0
        self.capacity = capacity
        self.residual = None

    def augment(self, flow):
        if flow <= 0:
            raise Exception("flow must be positive")
        if self.remaining_capacity() < flow:
            raise Exception("the adding flow is bigger than the remaining capacity")
        self.flow += flow
        self.residual.flow -= flow

    def remaining_capacity(self):
        assert((self.capacity - self.flow) >= 0) # must be possitive
        return self.capacity - self.flow

    def is_residual(self):
        return self.capacity == 0

    def get_flow(self):
        return -1*self.flow if self.is_residual() else self.flow

    def get_capacity(self):
        return -1*self.flow if self.is_residual() else self.capacity

    def get_src(self):
        return self.src

    def get_dst(self):
        return self.dst




