"""File for PaperCollection Class"""

from typing import Optional

from libraries.paper import Paper


class PaperCollection:
    """
    A class used to manage a collection of Paper instances.

    ...

    Attributes
    ----------
    papers : list[Paper]
        The list of `Paper` instances in the collection
    id_map : dict[str, int]
        A mapping from paper ID (as string) to their index in the `papers` list
    is_set : bool
        A flag indicating if the collection has been sorted and indexed

    Methods
    -------
    add_paper(paper)
        Adds a paper to the collection and updates the ID map
    remove_paper(paper)
        Removes a paper from the collection
    get_by_id(paper_id)
        Retrieves a paper from the collection using its ID
    setup()
        Sorts the collection and updates the ID map accordingly
    sorted_papers()
        Returns a new list of papers sorted in descending order of value
    """

    def __init__(
        self,
        papers: Optional[list[Paper]] = None,
        id_map: Optional[dict[str, int]] = None,
    ):
        """
        Constructs all the necessary attributes for the PaperCollection object.

        Parameters
        ----------
        papers : list[Paper], optional
            An optional list of Paper instances to initialize the collection
        id_map : dict[str, int], optional
            An optional mapping from paper IDs to their index in `papers`
        """
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
        """Adds a new paper to the collection.

        Parameters
        ----------
        paper : Paper
            The paper instance to add

        Raises
        ------
        ValueError
            If a paper with the same ID already exists
        """
        if paper.id in self.id_map:
            raise ValueError(f"A paper with ID {paper.id} already exist.")
        self.papers.append(paper)
        self.id_map[str(paper.id)] = len(self.papers) - 1
        self.is_set = False

    def remove_paper(self, paper: Paper):
        """Removes a paper from the collection.

        Parameters
        ----------
        paper : Paper
            The paper instance to remove

        Raises
        ------
        ValueError
            If the paper is not in the collection
        """
        if str(paper.id) not in self.id_map:
            raise ValueError(f"No paper with ID {paper.id} exist.")
        self.papers.remove(paper)
        self.id_map.pop(str(paper.id))

    def get_by_id(self, paper_id: int) -> Paper:
        """Retrieves a paper by its unique ID.

        Parameters
        ----------
        paper_id : int
            The ID of the paper to retrieve

        Returns
        -------
        Paper
            The `Paper` object with the given ID

        Raises
        ------
        ValueError
            If no paper with the specified ID exists
        """
        if not self.is_set:
            self.setup()
        indice = self.id_map.get(str(paper_id), None)
        if indice is None:
            raise ValueError(f"No paper with ID {paper_id} exist.")
        return self.papers[indice]

    def setup(self) -> None:
        """Sorts the papers and rebuilds the ID map."""
        self.papers = self.sorted_papers()

        for i, paper in enumerate(self.papers):
            self.id_map[str(paper.id)] = i
        self.is_set = True

    def sorted_papers(self):
        """Returns a list of papers sorted in descending order of value.

        Returns
        -------
        list[Paper]
            A new list of sorted papers
        """
        return sorted(self.papers, reverse=True)

    def __add__(self, other):
        """Combines two collections and returns a new PaperCollection.

        Parameters
        ----------
        other : PaperCollection

        Returns
        -------
        PaperCollection
            A new collection with papers from both collections

        Raises
        ------
        NotImplementedError
            If `other` is not of type PaperCollection
        """
        if isinstance(other, PaperCollection):
            return PaperCollection(
                papers=self.papers + other.papers, id_map=self.id_map | other.id_map
            )
        return NotImplemented

    def __contains__(self, item) -> bool:
        """Checks if a paper is in the collection.

        Parameters
        ----------
        item : Paper or int

        Returns
        -------
        bool
            True if item is in the collection, False otherwise
        """
        if isinstance(item, Paper):
            return item in self.papers
        if isinstance(item, int):
            return item in self.papers
        return False

    def __getitem__(self, item):
        """Allows access using square brackets via paper ID.

        Parameters
        ----------
        item : int
            The ID of the paper

        Returns
        -------
        Paper
            The `Paper` object associated with the ID
        """
        return self.get_by_id(item)

    def __iadd__(self, other):
        """In-place addition of another collection.

        Parameters
        ----------
        other : PaperCollection

        Returns
        -------
        PaperCollection
            The current collection updated with papers from the other
        """
        if isinstance(other, PaperCollection):
            self.papers += other.papers
            self.id_map.update(other.id_map)
            return self
        return NotImplemented

    def __iter__(self):
        """Returns an iterator over the papers.

        Returns
        -------
        Iterator[Paper]
        """
        return self.papers.__iter__()

    def __repr__(self):
        """Returns a string representation of the collection.

        Returns
        -------
        str
            String representation of the collection
        """
        return f"PaperCollection({self.papers})"
