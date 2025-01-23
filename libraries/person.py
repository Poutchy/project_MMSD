from typing import Dict

from libraries.paper import Paper


class Person:
    """docstring for Person."""

    def __init__(self, id: str, name: str, surname: str, matricule: str):
        super().__init__()
        self.id: str = id
        self.name: str = name
        self.surname: str = surname
        self.matricule: str = matricule
        self.papers: Dict[str, Paper] = {}
        self.proposed_papers: int = 0

    def add_paper(self, paper_id: str, paper: Paper):
        self.papers[paper_id] = paper
        self.proposed_papers += 1
