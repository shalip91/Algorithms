import json
from .order import Order
from .item import Item

class OrdersFileReader:
    """this class consist of static methods that parse the json orders files
       and construct a list of Order object."""

    @staticmethod
    def __parse_invenroty(inventory):
        items = []
        for item_name, values in inventory.items():
            items.append(Item(name=item_name, value=values['v'], weight=values['w']))
        return items

    @staticmethod
    def parse_orders(filename):
        orders = []
        with open(filename) as json_file:
            data = json.load(json_file)
            for order in data.values():
                orders.append(Order(
                    client_name=order['name'],
                    distance=order['distance'],
                    type=order['type'],
                    ai=order['ai'],
                    inventory=OrdersFileReader.__parse_invenroty(order['inventory'])
                ))
            return orders

if __name__ == '__main__':
    reader = OrdersFileReader.parse_orders('orders.json')
    print(reader[0])