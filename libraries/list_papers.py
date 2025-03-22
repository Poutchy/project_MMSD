"""File for PaperCollection Class"""

from typing import Optional

from libraries.paper import Paper


class PaperCollection:

    def __init__(
        self,
        papers: Optional[list[Paper]] = None,
        id_map: Optional[dict[str, int]] = None,
    ):
        self.papers: list[Paper]
        if papers:
            self.papers = papers
        else:
            self.papers = []
        self.id_map: dict[str, int]
        if id_map:
            self.id_map = id_map
        else:
            self.id_map = {}
        self.is_set = True

    def add_paper(self, paper: Paper):
        if paper.id in self.id_map:
            raise ValueError(f"A paper with ID {paper.id} already exist.")
        self.papers.append(paper)
        self.id_map[str(paper.id)] = len(self.papers) - 1
        self.is_set = False

    def remove_paper(self, paper: Paper):
        if str(paper.id) not in self.id_map:
            raise ValueError(f"No paper with ID {paper.id} exist.")
        self.papers.remove(paper)
        self.id_map.pop(str(paper.id))

    def get_by_id(self, paper_id: int) -> Paper:
        if not self.is_set:
            self.setup()
        indice = self.id_map.get(str(paper_id), None)
        if indice is None:
            raise ValueError(f"No paper with ID {paper_id} exist.")
        return self.papers[indice]

    def setup(self) -> None:
        self.papers = self.sorted_papers()

        for i, paper in enumerate(self.papers):
            self.id_map[str(paper.id)] = i
        self.is_set = True

    def sorted_papers(self):
        return sorted(self.papers, reverse=True)

    def __add__(self, other):
        if isinstance(other, PaperCollection):
            return PaperCollection(
                papers=self.papers + other.papers, id_map=self.id_map | other.id_map
            )
        return NotImplemented

    def __contains__(self, item) -> bool:
        if isinstance(item, Paper):
            return item in self.papers
        if isinstance(item, int):
            return item in self.papers
        return False

    def __getitem__(self, item):
        return self.get_by_id(item)

    def __iadd__(self, other):
        if isinstance(other, PaperCollection):
            self.papers += other.papers
            self.id_map.update(other.id_map)
            return self
        return NotImplemented

    def __iter__(self):
        return self.papers.__iter__()

    def __repr__(self):
        return f"PaperCollection({self.papers})"
