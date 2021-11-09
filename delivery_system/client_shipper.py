import math
from copy import deepcopy

from shipments.shipment import Shipment
from dependencies.graph_package.graph import Graph


class ClientShipper:
    """ this object is responsible for creating a schedule out of a given list of
        of shipments and other parameters.
        the process of doing so is by using the "lawler" algorithm that uses the
        precedence graph as a prerequisite."""

    g = {
        "identity": lambda x: 1,
        "sum": lambda values: sum(values),
        "max": lambda values: max(values),
        "len": lambda values: len(values)
    }

    def __init__(self, shipments, q_diff_factor=0.75, cost_function_type="sum") -> None:
        super().__init__()
        self.cost_func = lambda x, ai, values: (x * ClientShipper.g[cost_function_type](values)) / ai
        self.prec_graph = self.__graph_init(shipments, q_diff_factor)
        self.schedule = self.__lawler_scheduler()

    def __graph_init(self, shipments, q_diff_factor):
        """ create the precedence graph containing all the shipments

        :param shipments: list of all the shipments in the batch
        :param q_diff_factor: factor to determine distinct difference between primes
        :return: graph containing all the shipments
        """
        graph = Graph(container='list', directed=True)
        graph = self.__add_prime_shipments(graph, shipments, q_diff_factor)
        graph = self.__add_reg_shipments(graph, shipments)
        return graph

    def __add_prime_shipments(self, graph, shipments, q_diff_factor):
        """ create the precedence tree of the primes. the root is a dummy
            node that will not be taken into consideration later.

        :param graph: empty graph
        :param shipments: list of all the shipments in the batch
        :param q_diff_factor: factor to determine distinct difference between primes
        :return: graph containing the primes
        """
        prime_shipments = list(filter(lambda s: s.type == 'prime', shipments))

        # add the dummy shipment
        dummy_shipment = Shipment(client_name='dummy', distance=0, ai=0)
        graph.add_vertex(key=dummy_shipment.client_name, value=dummy_shipment)

        while prime_shipments:
            # pop the max ai shipment and add it to the graph
            curr_min_ai = min(prime_shipments, key=lambda s: s.ai)
            prime_shipments.remove(curr_min_ai)
            graph.add_vertex(key=curr_min_ai.client_name, value=curr_min_ai)

            # connect the new vertex to all his predecessors if ai < q*aj
            for old_vertex in graph.get_vertices():
                if old_vertex.weight.ai < (q_diff_factor * curr_min_ai.ai):
                    graph.add_edge(src=old_vertex.weight.client_name, dst=curr_min_ai.client_name)

        return graph

    def __add_reg_shipments(self, graph, shipments):
        """ insert all the regular shipments as children of the least significant prime

        :param graph: graph containing all the primes
        :param shipments: list of all the shipments in the batch
        :return: graph containing all the shipments
        """
        # filter out all the primes, leaving all the regular shipments
        reg_shipments = list(filter(lambda s: s.type != 'prime', shipments))

        # getting the least significant prime by his price
        last_prime = min(graph.get_vertices(), key=lambda v: v.weight.get_price()).weight

        for shipment in reg_shipments:
            # add as child to the last prime node
            graph.add_vertex(key=shipment.client_name, value=shipment)
            graph.add_edge(src=last_prime.client_name, dst=shipment.client_name)

        return graph

    def __lawler_scheduler(self):
        graph = deepcopy(self.prec_graph)
        vertices = list(filter(lambda v: v.weight.client_name != 'dummy', self.prec_graph.get_vertices()))
        total_process_time = sum([v.weight.distance for v in vertices])
        schedule = []
        n = len(vertices)
        num_of_reg_remaining = sum([1 for v in vertices if v.weight.type != 'prime'])

        for k in range(n-1, 0, -1):
            taken_vertex, taken_idx, f_k = None, -1, math.inf
            # find vertex j such that out deg is 0 and fj(p) is minimal
            for idx, vertex in enumerate(vertices):
                if vertex.weight.type == 'prime' and num_of_reg_remaining > 0:
                    continue
                if graph.degree(vertex.key)[1] == 0:
                    cost = self.cost_func(x=total_process_time,
                                          ai=vertex.weight.ai,
                                          values=vertex.weight.get_items_value())
                    if f_k > cost:
                        f_k = cost
                        taken_vertex = vertex
                        taken_idx = idx

            # update given data
            if taken_idx != -1:
                num_of_reg_remaining -= 1
                taken_vertex.weight.cost_value = cost
                schedule.append(taken_vertex)
                vertices.remove(taken_vertex)
                total_process_time -= taken_vertex.weight.distance
                graph.remove_vertex(taken_vertex.key)

        return [v.weight for v in schedule][::-1]

