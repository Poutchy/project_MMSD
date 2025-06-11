from libraries.list_papers import PaperCollection
from libraries.paper import Paper


class Person:
    """
    A class used to represent a Person involved with scientific papers.

    ...

    Attributes
    ----------
    id : int
        A unique identifier for the person
    name : str
        The first name of the person
    surname : str
        The last name of the person
    matricule : int
        The registration or identification number
    proposed_papers : PaperCollection
        A collection of papers proposed by the person
    writted_papers : PaperCollection
        A collection of papers written by the person
    nb_writted_papers : int
        The number of papers written by the person
    nb_proposed_papers : int
        The number of papers proposed by the person
    nb_papers : int
        The total number of papers involving the person

    Methods
    -------
    add_writted_paper(paper)
        Adds a paper to the person's list of written papers
    has_written(paper)
        Checks if the person has written the specified paper
    propose_paper(paper)
        Adds a paper to the proposed list and sets this person as presenter
    unpropose_paper(paper)
        Removes a paper from the proposed list
    __eq__(other_person)
        Checks if two persons are the same based on their ID
    __le__(other_person)
        Less than or equal comparison based on non-presented written papers
    __lt__(other_person)
        Less than comparison based on non-presented written papers
    __str__()
        Returns a string representation of the person
    to_json()
        Converts the person's data to a JSON-serializable dictionary
    """

    def __init__(self, id: int, name: str, surname: str, matricule: int):
        """
        Constructs all the necessary attributes for the person object.

        Parameters
        ----------
        id : int
            Unique identifier for the person
        name : str
            First name of the person
        surname : str
            Last name of the person
        matricule : int
            Registration or identification number
        """
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
        """Adds a paper to the person's list of written papers and updates counters.

        Parameters
        ----------
        paper : Paper
            The paper to add to the written papers
        """
        self.writted_papers.add_paper(paper)
        self.writted_papers.setup()
        self.nb_writted_papers += 1
        self.nb_papers += 1

    def has_written(self, paper: Paper) -> bool:
        """Checks if the person has written the specified paper.

        Parameters
        ----------
        paper : Paper
            The paper to check for authorship

        Returns
        -------
        bool
            True if the person wrote the paper, False otherwise
        """
        return paper in self.writted_papers

    def propose_paper(self, paper: Paper):
        """Proposes a paper and sets the person as a presenter.

        Parameters
        ----------
        paper : Paper
            The paper to propose
        """
        self.proposed_papers.add_paper(paper)
        self.nb_proposed_papers += 1
        paper.add_presenter(self)

    def unpropose_paper(self, paper: Paper):
        """Removes a proposed paper from the list.

        Parameters
        ----------
        paper : Paper
            The paper to remove from the proposed list
        """
        self.proposed_papers.remove_paper(paper)
        self.nb_proposed_papers -= 1

    def __eq__(self, other_person: object, /) -> bool:
        """Checks equality based on ID.

        Parameters
        ----------
        other_person : object
            The person to compare with

        Returns
        -------
        bool
            True if both persons have the same ID, False otherwise
        """
        if isinstance(other_person, Person):
            return self.id == other_person.id
        return False

    def __le__(self, other_person: object, /) -> bool:
        """Compares the number of non-presented written papers (<=).

        Parameters
        ----------
        other_person : object
            The other person to compare with

        Returns
        -------
        bool
            True if this person has fewer or equal non-presented written papers
        """
        if isinstance(other_person, Person):
            sum = 0
            sum_other = 0
            for p in self.writted_papers:
                if p.is_presented():
                    sum += 1
            for p in other_person.writted_papers:
                if p.is_presented():
                    sum_other += 1
            return self.nb_writted_papers - sum <= other_person.nb_writted_papers - sum
        return False

    def __lt__(self, other_person: object, /) -> bool:
        """Compares the number of non-presented written papers (<).

        Parameters
        ----------
        other_person : object
            The other person to compare with

        Returns
        -------
        bool
            True if this person has fewer non-presented written papers
        """
        if isinstance(other_person, Person):
            sum = 0
            sum_other = 0
            for p in self.writted_papers:
                if p.is_presented():
                    sum += 1
            for p in other_person.writted_papers:
                if p.is_presented():
                    sum_other += 1
            return self.nb_writted_papers - sum < other_person.nb_writted_papers - sum
        return False

    def __str__(self):
        """Returns a string representation of the person.

        Returns
        -------
        str
            The full name of the person
        """
        return f"{self.name} {self.surname}"

    def to_json(self) -> dict:
        """Serializes the person and their proposed papers to a JSON-compatible dictionary.

        Returns
        -------
        dict
            A dictionary representation of the person and their proposed papers
        """
        l_book: list[dict] = []
        sum_value_paper: int = 0
        for p in self.proposed_papers:
            l_book.append(p.to_json())
            sum_value_paper += p.value
        res = {
            "ID": self.id,
            "nome": self.surname,
            "cognome": self.name,
            "nb_writted_papers": self.nb_writted_papers,
            "products": l_book,
            "value": sum_value_paper,
        }
        return res


from libraries.list_papers import PaperCollection
