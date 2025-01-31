class Paper:
    def __init__(self, id: int, name: str, value: int):
        self.id: int = id
        self.name: str = name
        self.value: int = value
        self.status: int = 0

    def __eq__(self, value: object, /) -> bool:
        if isinstance(value, Paper):
            return self.id == value.id
        return False

    def __le__(self, value: object, /) -> bool:
        if isinstance(value, Paper):
            return self.value <= value.value
        return False

    def __lt__(self, value: object, /) -> bool:
        if isinstance(value, Paper):
            return self.value < value.value
        return False

    def __str__(self):
        return self.name
