from lib.paper import Paper


class PaperCollection:
    def __init__(self):
        self.papers: list[Paper] = []
        self.id_map: dict[str, Paper] = {}  # Dictionnaire pour un accès rapide par ID

    def add_paper(self, paper: Paper):
        if paper.id in self.id_map:
            raise ValueError(f"Un papier avec l'ID {paper.id} existe déjà.")
        self.papers.append(paper)
        self.id_map[str(paper.id)] = paper

    def get_by_id(self, paper_id: int):
        return self.id_map.get(str(paper_id), None)

    def sorted_papers(self):
        return sorted(self.papers, key=lambda paper: paper.value)

    def __repr__(self):
        return f"PaperCollection({self.papers})"
