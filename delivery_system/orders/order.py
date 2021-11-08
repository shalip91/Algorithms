class Order:
    def __init__(self, client_name, distance, type, ai, inventory) -> None:
        super().__init__()
        self.client_name = client_name
        self.distance = distance
        self.type = type
        self.ai = ai
        self.inventory = inventory

    def get_items_weight(self):
        return [item.weight for item in self.inventory]

    def get_items_value(self):
        return [item.value for item in self.inventory]

    def __str__(self) -> str:
        items = ''
        for item in self.inventory:
            items += f'{item}, '

        return f'name:{self.client_name},  ' \
               f'distance:{self.distance},  ' \
               f'type:{self.type},  ' \
               f'ai:{self.ai},  ' \
               f'inventory:{items}'

