class Paper:
    def __init__(self, id: int, name: str, value: int):
        self.id: int = id
        self.name: str = name
        self.value: int = value
        self.status: int = 0
        self.presenter: int = 0

    def add_presenter(self, person):
        from libraries.person import Person

        if isinstance(person, Person):
            self.status = 1
            self.presenter = person.id

        if isinstance(person, int):
            self.status = 1
            self.presenter = person

    def is_presented(self) -> bool:
        return bool(self.status)

    def __eq__(self, other_paper: object, /) -> bool:
        if isinstance(other_paper, Paper):
            return self.id == other_paper.id
        return False

    def __le__(self, other_paper: object, /) -> bool:
        if isinstance(other_paper, Paper):
            return self.value <= other_paper.value
        return False

    def __lt__(self, other_paper: object, /) -> bool:
        if isinstance(other_paper, Paper):
            return self.value < other_paper.value
        return False

    def __str__(self):
        return self.name
