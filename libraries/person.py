from libraries.list_papers import PaperCollection
from libraries.paper import Paper


class Person:
    """docstring for Person."""

    def __init__(self, id: int, name: str, surname: str, matricule: int):
        super().__init__()
        self.id: int = id
        self.name: str = name
        self.surname: str = surname
        self.matricule: int = matricule

        self.proposed_papers: PaperCollection = PaperCollection()
        self.writted_papers: PaperCollection = PaperCollection()
        self.nb_writted_papers: int = 0
        self.nb_proposed_papers: int = 0
        self.nb_papers: int = 0

    def add_writted_paper(self, paper: Paper):
        self.writted_papers.add_paper(paper)
        self.nb_writted_papers += 1
        self.nb_papers += 1

    def has_written(self, paper: Paper) -> bool:
        return paper in self.writted_papers

    def propose_paper(self, paper: Paper):
        self.proposed_papers.add_paper(paper)
        self.nb_proposed_papers += 1
        paper.add_presenter(self)

    def unpropose_paper(self, paper: Paper):
        self.proposed_papers.remove_paper(paper)
        self.nb_proposed_papers -= 1

    def __eq__(self, ohter_person: object, /) -> bool:
        if isinstance(ohter_person, Person):
            return self.id == ohter_person.id
        return False

    def __le__(self, ohter_person: object, /) -> bool:
        if isinstance(ohter_person, Person):
            return self.nb_proposed_papers <= ohter_person.nb_proposed_papers
        return False

    def __lt__(self, ohter_person: object, /) -> bool:
        if isinstance(ohter_person, Person):
            return self.nb_proposed_papers < ohter_person.nb_proposed_papers
        return False

    def __str__(self):
        return f"{self.name} {self.surname}"

    def to_json(self) -> dict:
        l_book: list[dict] = []
        sum_value_paper: int = 0
        for p in self.proposed_papers:
            l_book.append(p.to_json())
            sum_value_paper += p.value
        res = {
            "ID": self.id,
            "nome": self.surname,
            "cognome": self.name,
            "products": l_book,
            "value": sum_value_paper,
        }
        return res


from libraries.list_papers import PaperCollection
