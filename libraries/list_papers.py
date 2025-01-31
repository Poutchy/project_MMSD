"""File for PaperCollection Class"""

from typing import Optional

from libraries.paper import Paper


class PaperCollection:
    def __init__(
        self,
        papers: Optional[list[Paper]] = None,
        id_map: Optional[dict[str, Paper]] = None,
    ):
        self.papers: list[Paper]
        if papers:
            self.papers = papers
        else:
            self.papers = []
        self.id_map: dict[str, Paper]
        if id_map:
            self.id_map = id_map
        else:
            self.id_map = {}

    def add_paper(self, paper: Paper):
        if paper.id in self.id_map:
            raise ValueError(f"A paper with ID {paper.id} already exist.")
        self.papers.append(paper)
        self.id_map[str(paper.id)] = paper

    def get_by_id(self, paper_id: int):
        return self.id_map.get(str(paper_id), None)

    def sorted_papers(self):
        return sorted(self.papers)

    def __add__(self, other):
        if isinstance(other, PaperCollection):
            return PaperCollection(
                papers=self.papers + other.papers, id_map=self.id_map | other.id_map
            )
        return NotImplemented

    def __contains__(self, item) -> bool:
        if isinstance(item, Paper):
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

    def __repr__(self):
        return f"PaperCollection({self.papers})"
