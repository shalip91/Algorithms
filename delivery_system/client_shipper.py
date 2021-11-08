from client_packer import ClientPacker
from algorithms.graph.graph_package.graph import Graph
from collections import defaultdict


class ClientShipper:
    g = {
        "identity": lambda x: 1,
        "sum": lambda values: sum(values),
        "max": lambda values: max(values)
    }

    def __init__(self, shipments, q_diff_factor=0.75, cost_function_type="sum") -> None:
        super().__init__()
        self.cost_func = lambda x, ai, values: (x * ClientShipper.g[cost_function_type](values)) / ai
        self.prec_graph = self.__graph_init(shipments, q_diff_factor)

    def __graph_init(self, shipments, q_diff_factor):
        graph = Graph(container='list', directed=True)
        graph = self.__add_prime_shipments(graph, shipments, q_diff_factor)

    def __add_prime_shipments(self, graph, shipments, q_diff_factor):
        prime_shipments = list(filter(lambda s: s.type == 'prime', shipments))
        while prime_shipments:
            # pop the max paid shipment
            curr_max_paid = max(prime_shipments, key=lambda s: sum(s.get_items_value()))
            prime_shipments.remove(curr_max_paid)

            # add the first 2 shipments as father and son
            graph.add_vertex(key=curr_max_paid.client_name, value=curr_max_paid)
            if len(graph.get_vertices()) == 2:
                graph.add_edge(src=prev_max_paid.client_name, dst=curr_max_paid.client_name)
                prev_max_paid = curr_max_paid

            # add the last 2+ shipments
            if len(graph.get_vertices()) > 2:
                # add as child to the prev node
                if sum(prev_max_paid.get_items_value()) * q_diff_factor > sum(curr_max_paid.get_items_value()):
                    graph.add_edge(src=prev_max_paid.client_name, dst=curr_max_paid.client_name)
                    prev_prev_max_paid = prev_max_paid
                    prev_max_paid = curr_max_paid

                # add as brother to the prev node
                else:
                    graph.add_edge(src=prev_prev_max_paid.client_name, dst=curr_max_paid.client_name)
                    prev_max_paid = curr_max_paid




            # print("max_paid", max_paid)
            # for s in prime_shipments: print(s)

        # for src, neighbors in mat_graph.items():
        #     for dst in neighbors.keys():
        #         graph.add_edge(src, dst)
        #
        # return graph


if __name__ == '__main__':

    packer = ClientPacker(filename='orders.json',
                          ship_size=12,
                          reg_w_max_size=10,
                          reg_v_max_value=5)
    for s in packer.calculate_shipments(): print(s)
    shipper = ClientShipper(packer.shipments)
