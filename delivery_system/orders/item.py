class Item:
    def __init__(self, name, value, weight) -> None:
        super().__init__()
        self.name = name
        self.value = value
        self.weight = weight

    def __str__(self) -> str:
        return f'{self.name}:(v:{self.value},w:{self.weight})'


