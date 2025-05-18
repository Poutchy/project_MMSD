class Paper:
    """
    A class used to represent a Scientific Paper.

    ...

    Attributes
    ----------
    id : int
        Unique identifier for the paper
    name : str
        Title of the paper
    type : str
        Type or category of the paper (e.g., journal, conference)
    value : float
        The evaluation score or metric value associated with the paper
    status : int
        A flag indicating whether the paper has been presented (0 or 1)
    presenter : int
        The ID of the person who presents the paper

    Methods
    -------
    add_presenter(person)
        Assigns a presenter to the paper
    is_presented()
        Returns True if the paper has a presenter, False otherwise
    __eq__(other_paper)
        Compares equality based on the paper ID
    __le__(other_paper)
        Compares papers based on value (less than or equal)
    __lt__(other_paper)
        Compares papers based on value (less than)
    __str__()
        Returns a string representation of the paper
    to_json()
        Returns a JSON-serializable dictionary of the paper
    """

    def __init__(
        self,
        id: int,
        name: str,
        type: str,
        value: float,
    ):
        """
        Constructs all the necessary attributes for the paper object.

        Parameters
        ----------
        id : int
            Unique identifier for the paper
        name : str
            Title of the paper
        type : str
            Type/category of the paper
        value : float
            The metric or evaluation value associated with the paper
        """
        self.id: int = id
        self.name: str = name
        self.value: float = value
        self.status: int = 0
        self.type: str = type
        self.presenter: int = 0

        # scopus: Percentili pubblicazione - miglior percentile
        # wos: Percentili pubblicazione - miglior percentile

    def add_presenter(self, person):
        """Assigns a presenter to this paper.

        If the presenter is an instance of `Person`, assigns their ID.
        If the presenter is already an ID (int), assigns it directly.

        Parameters
        ----------
        person : Person or int
            The presenter, either as a `Person` object or an ID
        """
        from libraries.person import Person

        if isinstance(person, Person):
            self.status = 1
            self.presenter = person.id

        if isinstance(person, int):
            self.status = 1
            self.presenter = person

    def is_presented(self) -> bool:
        """Checks whether the paper has been presented.

        Returns
        -------
        bool
            True if presented, False otherwise
        """
        return bool(self.status)

    def __eq__(self, other_paper: object, /) -> bool:
        """Checks equality based on the paper's ID.

        Parameters
        ----------
        other_paper : object
            Another paper object or ID to compare with

        Returns
        -------
        bool
            True if IDs match, False otherwise
        """
        if isinstance(other_paper, Paper):
            return self.id == other_paper.id
        if isinstance(other_paper, int):
            return self.id == other_paper
        return False

    def __le__(self, other_paper: object, /) -> bool:
        """Compares two papers based on their value (<=).

        Parameters
        ----------
        other_paper : object
            Another paper to compare with

        Returns
        -------
        bool
            True if this paper's value is less than or equal to the other
        """
        if isinstance(other_paper, Paper):
            return self.value <= other_paper.value
        return False

    def __lt__(self, other_paper: object, /) -> bool:
        """Compares two papers based on their value (<).

        Parameters
        ----------
        other_paper : object
            Another paper to compare with

        Returns
        -------
        bool
            True if this paper's value is less than the other
        """
        if isinstance(other_paper, Paper):
            return self.value < other_paper.value
        return False

    def __str__(self):
        """Returns a human-readable representation of the paper.

        Returns
        -------
        str
            Formatted string with paper ID, name, and value
        """
        return f"{self.id}, {self.name}: {self.value}"

    def to_json(self) -> dict:
        """Returns a dictionary representation of the paper for serialization.

        Returns
        -------
        dict
            A JSON-compatible dictionary of paper attributes
        """
        return {
            "ID prodotto": self.id,
            "Titolo": self.name,
            "type": self.type,
            "value": self.value,
        }


def threshold(value, configs):
    """
    Maps a continuous value to a quantile bucket based on predefined thresholds.

    Parameters
    ----------
    value : float
        The numeric value to evaluate against thresholds
    configs : dict
        A configuration dictionary containing:
            - "quantile_thresholds": list of threshold floats
            - "quantile_values": list of corresponding values to return

    Returns
    -------
    any
        The quantile value corresponding to the range in which `value` falls
    """
    for i in range(len(configs["quantile_thresholds"])):
        if value < configs["quantile_thresholds"][i]:
            return configs["quantile_values"][i]

    return configs["quantile_values"][-1]
