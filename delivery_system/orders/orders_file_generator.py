import json
import random
import string
import numpy as np


class OrderFileGenerator:

    # static variables
    items_names = ["banana", "apple", "sand", "bottle", "hat", "shirt", "pants", "bag",
                   "vase", "ring", "chair", "clock", "cup", "ball", "key", "phone",
                   "guitar", "glasses", "shoe", "bread", "egg", "cheese", "meat"]
    order_type = ["w-reg", "v-reg", "prime"]

    def __init__(self, order_num=2,
                 max_inventory_size=5,
                 max_distance=10,
                 max_weight=10,
                 max_value=10,
                 ai_min=0.1,
                 ai_max=1) -> None:
        super().__init__()
        self.order_num = order_num
        self.max_inventory_size = max_inventory_size
        self.max_distance = max_distance
        self.max_weight = max_weight
        self.max_value = max_value
        self.ai_min = ai_min,
        self.ai_max = ai_max
        self.dict = {}


    @staticmethod
    def generate_name(random_name_len=8):
        return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(random_name_len))

    def __random_inventory(self):
        inventory = {}
        for _ in range(self.max_inventory_size):
            inventory[random.choice(self.items_names)] = {
                'v': np.random.randint(1, self.max_value),
                'w': np.random.randint(1, self.max_weight)
            }
        return inventory

    def __new_order(self, client_name):
        order = {
            'name': client_name,
            'distance': np.random.randint(1, self.max_distance),
            'type': random.choice(self.order_type)
            }
        if order['type'] == 'prime':
            order['ai'] = round(random.uniform(0.1, 1), 3)
        else:
            order['ai'] = 1

        order['inventory'] = self.__random_inventory()

        print(order)

        return order

    def generate_json(self, filename):
        for _ in range(self.order_num):
            client_name = OrderFileGenerator.generate_name()
            self.dict[client_name] = self.__new_order(client_name)

        with open(filename, 'w') as outfile:
            output_str = json.dumps(self.dict, indent=4)
            outfile.write(output_str)

if __name__ == '__main__':

    generator = OrderFileGenerator(order_num=10,
                                   max_inventory_size=5,
                                   max_distance=10,
                                   max_weight=10,
                                   max_value=10,
                                   ai_min=0.1,
                                   ai_max=1)
    generator.generate_json("../orders.json")

