from shipments.shipment_factory import ShipmentFactory
from shipments.shipment import Shipment
from orders.orders_file_reader import OrdersFileReader


class ClientPacker:
    """ this class can read the json file containing all the clients orders
        and process and calculate the optimal/approximal best item list
        to yield the best value/weight.
        the result is a list of all the clients shipments."""
    def __init__(self, filename='orders.json',
                 ship_size=100,
                 reg_w_max_size=10,
                 reg_v_max_value=10) -> None:
        super().__init__()
        self.orders = OrdersFileReader.parse_orders(filename)
        self.shipments = []
        self.order_limits = {
            "reg_w_max_size": reg_w_max_size,
            "reg_v_max_value": reg_v_max_value,
            "ship_size": ship_size,
        }


    def calculate_shipments(self):
        """ calculate the ideal shipment for each client, and
            combining all the "w-reg" client together.

        :return: list of shipments.
        """
        # creating dummy shipment that all "w-reg" will sum into it.
        shipment_w_reg = Shipment(client_name='w-reg_group', distance=0)
        for order in self.orders:
            # Factory design pattern to create the shipment according to order type.
            shipment = ShipmentFactory.create(order, self.order_limits)

            if shipment is None:  # in case client shipment calculation failed
                continue
            if shipment.type != 'w-reg':
                self.shipments.append(shipment)
            else:  # combine all the "w-reg" shipments
                shipment_w_reg += shipment

        if shipment_w_reg.distance != 0:  # append the group of "w-reg"
            self.shipments.append(shipment_w_reg)
        return self.shipments




