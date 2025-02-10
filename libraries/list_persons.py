"""File for PersonCollection Class"""

from typing import Optional

from libraries.person import Person


class PersonCollection:
    def __init__(
        self,
        persons: Optional[list[Person]] = None,
        id_map: Optional[dict[str, int]] = None,
    ):
        self.persons: list[Person]
        if persons:
            self.person = persons
        else:
            self.person = []
        self.id_map: dict[str, int]
        if id_map:
            self.id_map = id_map
        else:
            self.id_map = {}
        self.is_set = True

    def add_person(self, person: Person):
        if person.id in self.id_map:
            raise ValueError(f"A person with ID {person.id} already exist.")
        self.persons.append(person)
        self.is_set = False

    def get_by_id(self, person_id: int) -> Person:
        indice = self.id_map.get(str(person_id), None)
        if indice is None:
            raise ValueError(f"No Person with ID {person_id} exist")
        return self.persons[indice]

    def remove_person(self, person: Person):
        if person.id not in self.id_map:
            raise ValueError(f"No person with ID {person.id} exist.")
        self.persons.remove(person)
        self.id_map.pop(str(person.id))

    def setup(self) -> None:
        self.persons = self.sorted_persons()
        for i, person in enumerate(self.persons):
            self.id_map[str(person.id)] = i
        self.is_set = True

    def sorted_persons(self):
        return sorted(self.persons)

    def __add__(self, other):
        if isinstance(other, PersonCollection):
            return PersonCollection(
                persons=self.persons + other.persons, id_map=self.id_map | other.id_map
            )
        return NotImplemented

    def __contains__(self, item) -> bool:
        if isinstance(item, Person):
            return item in self.persons
        return False

    def __getitem__(self, item):
        return self.get_by_id(item)

    def __iadd__(self, other):
        if isinstance(other, PersonCollection):
            self.persons += other.persons
            self.id_map.update(other.id_map)
            self.is_set = False
            return self
        return NotImplemented

    def __repr__(self):
        return f"PersonCollection({self.persons})"
