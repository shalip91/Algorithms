
class Task:
    def __init__(self, name, start, end, value=1) -> None:
        self.name = name
        self.start = start
        self.end = end
        self.value = value

    def __str__(self) -> str:
        return f'{self.name}:\t{self.start}|---{self.value}---|{self.end}'

