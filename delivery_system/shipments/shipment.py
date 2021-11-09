import math


class Shipment:
    def __init__(self, client_name, distance=0, type='w-reg', ai=1, inventory=[]) -> None:
        super().__init__()
        self.client_name = client_name
        self.distance = distance
        self.type = type
        self.ai = ai
        self.inventory = inventory
        self.cost_value = None

    def get_items_weight(self):
        return [item.weight for item in self.inventory]

    def get_items_value(self):
        return [item.value for item in self.inventory]

    def get_price(self):
        if self.client_name == 'dummy':
            return math.inf
        return sum(self.get_items_value())

    def get_ai(self): return self.ai

    def __iadd__(self, other):
        self.name = 'w_reg_group'
        self.distance += other.distance
        self.inventory = self.inventory + other.inventory

        return self

    def __str__(self) -> str:
        items = ''
        for item in self.inventory:
            items += f'{item}, '

        return f'name:{self.client_name},  ' \
               f'distance:{self.distance},  ' \
               f'price:{sum(self.get_items_value())},  ' \
               f'type:{self.type},  ' \
               f'ai:{self.ai},  ' \
               f'inventory:{items}'

