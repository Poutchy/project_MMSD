from random import shuffle

from libraries.paper import Paper
from libraries.list_papers import PaperCollection


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
