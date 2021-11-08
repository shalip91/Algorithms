import json

from shipments.shipment_factory import ShipmentFactory
from shipments.shipment import Shipment
from orders.orders_file_reader import OrdersFileReader


class ClientPacker:
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
        shipment_w_reg = Shipment(client_name='w-reg_group', distance=0)
        for order in self.orders:
            # Factory design pattern to create the shipment according to order type.
            shipment = ShipmentFactory.create(order, self.order_limits)
            if shipment is None: continue
            if shipment.type != 'w-reg':
                self.shipments.append(shipment)
            else:  # combine all the "w-reg" shipments
                shipment_w_reg += shipment

        self.shipments.append(shipment_w_reg)
        return self.shipments


if __name__ == '__main__':
    packer = ClientPacker(filename='orders.json',
                          ship_size=12,
                          reg_w_max_size=10,
                          reg_v_max_value=5)

    for order in packer.orders:
        print(order)

    print("after calculating")
    for s in packer.calculate_shipments():
        print(s)

