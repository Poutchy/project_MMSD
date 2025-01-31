from libraries.list_papers import PaperCollection
from libraries.paper import Paper


class Person:
    """docstring for Person."""

    def __init__(self, id: str, name: str, surname: str, matricule: str):
        super().__init__()
        self.id: str = id
        self.name: str = name
        self.surname: str = surname
        self.matricule: str = matricule
        self.papers: PaperCollection = PaperCollection()
        self.proposed_papers: int = 0

    def add_paper(self, paper: Paper):
        self.papers.add_paper(paper)
        self.proposed_papers += 1

    def __eq__(self, value: object, /) -> bool:
        if isinstance(value, Person):
            return self.id == value.id
        return False

    def __le__(self, value: object, /) -> bool:
        if isinstance(value, Person):
            return self.proposed_papers <= value.proposed_papers
        return False

    def __lt__(self, value: object, /) -> bool:
        if isinstance(value, Person):
            return self.proposed_papers < value.proposed_papers
        return False

    def __str__(self):
        return f"{self.name} {self.surname}"
