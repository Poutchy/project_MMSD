from typing import Optional

from libraries.person import Person


class PersonCollection:
    """
    A class used to manage a collection of Person instances.

    ...

    Attributes
    ----------
    persons : list[Person]
        The list of `Person` instances in the collection
    id_map : dict[str, int]
        A mapping from person ID (as string) to their index in the `persons` list
    is_set : bool
        A flag indicating if the collection has been sorted and indexed

    Methods
    -------
    add_person(person)
        Adds a person to the collection and updates the ID map
    get_by_id(person_id)
        Retrieves a person from the collection using their ID
    remove_person(person)
        Removes a person from the collection
    setup()
        Sorts the collection and updates the ID map accordingly
    sorted_persons()
        Returns a new list of persons sorted using their comparison methods
    """

    def __init__(
        self,
        persons: Optional[list[Person]] = None,
        id_map: Optional[dict[str, int]] = None,
    ):
        """
        Constructs all the necessary attributes for the PersonCollection object.

        Parameters
        ----------
        persons : list[Person], optional
            An optional list of Person instances to initialize the collection
        id_map : dict[str, int], optional
            An optional mapping from person IDs to their index in `persons`
        """
        self.persons: list[Person]
        if persons:
            self.persons = persons
        else:
            self.persons = []
        self.id_map: dict[str, int]
        if id_map:
            self.id_map = id_map
        else:
            self.id_map = {}
        self.is_set = True

    def add_person(self, person: Person):
        """Adds a new person to the collection.

        Parameters
        ----------
        person : Person
            The person instance to add

        Raises
        ------
        ValueError
            If a person with the same ID already exists
        """
        if person.id in self.id_map:
            raise ValueError(f"A person with ID {person.id} already exist.")
        self.persons.append(person)
        self.id_map[str(person.id)] = len(self.persons) - 1
        self.is_set = False

    def get_by_id(self, person_id: int) -> Person:
        """Retrieves a person by their unique ID.

        Parameters
        ----------
        person_id : int
            The ID of the person to retrieve

        Returns
        -------
        Person
            The `Person` object with the given ID

        Raises
        ------
        ValueError
            If no person with the specified ID exists
        """
        indice = self.id_map.get(str(person_id), None)
        if indice is None:
            raise ValueError(f"No Person with ID {person_id} exist")
        return self.persons[indice]

    def remove_person(self, person: Person):
        """Removes a person from the collection.

        Parameters
        ----------
        person : Person
            The person instance to remove

        Raises
        ------
        ValueError
            If the person is not in the collection
        """
        if person.id not in self.id_map:
            raise ValueError(f"No person with ID {person.id} exist.")
        self.persons.remove(person)
        self.id_map.pop(str(person.id))

    def setup(self) -> None:
        """Sorts the persons and rebuilds the ID map."""
        self.persons = self.sorted_persons()
        for i, person in enumerate(self.persons):
            self.id_map[str(person.id)] = i
        self.is_set = True

    def sorted_persons(self):
        """Returns a sorted list of persons.

        Returns
        -------
        list[Person]
            A new list of sorted persons
        """
        return sorted(self.persons)

    def __add__(self, other):
        """Combines two collections and returns a new PersonCollection.

        Parameters
        ----------
        other : PersonCollection

        Returns
        -------
        PersonCollection
            A new collection with persons from both collections

        Raises
        ------
        NotImplementedError
            If `other` is not of type PersonCollection
        """
        if isinstance(other, PersonCollection):
            return PersonCollection(
                persons=self.persons + other.persons, id_map=self.id_map | other.id_map
            )
        return NotImplemented

    def __contains__(self, item) -> bool:
        """Checks if a person is in the collection.

        Parameters
        ----------
        item : Person

        Returns
        -------
        bool
            True if item is in the collection, False otherwise
        """
        if isinstance(item, Person):
            return item in self.persons
        return False

    def __getitem__(self, item):
        """Allows access using square brackets via person ID.

        Parameters
        ----------
        item : int
            The ID of the person

        Returns
        -------
        Person
            The `Person` object associated with the ID
        """
        return self.get_by_id(item)

    def __iadd__(self, other):
        """In-place addition of another collection.

        Parameters
        ----------
        other : PersonCollection

        Returns
        -------
        PersonCollection
            The current collection updated with persons from the other
        """
        if isinstance(other, PersonCollection):
            self.persons += other.persons
            self.id_map.update(other.id_map)
            self.is_set = False
            return self
        return NotImplemented

    def __iter__(self):
        """Returns an iterator over the persons.

        Returns
        -------
        Iterator[Person]
        """
        return self.persons.__iter__()

    def __repr__(self):
        """Returns a string representation of the collection.

        Returns
        -------
        str
            String representation of the collection
        """
        return f"PersonCollection({self.persons})"
