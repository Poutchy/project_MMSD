"""File for PersonCollection Class"""

from typing import Optional

from libraries.person import Person


class PersonCollection:
    def __init__(
        self,
        persons: Optional[list[Person]] = None,
        id_map: Optional[dict[str, Person]] = None,
    ):
        self.persons: list[Person]
        if persons:
            self.person = persons
        else:
            self.person = []
        self.id_map: dict[str, Person]
        if id_map:
            self.id_map = id_map
        else:
            self.id_map = {}

    def add_person(self, person: Person):
        if person.id in self.id_map:
            raise ValueError(f"A person with ID {person.id} already exist.")
        self.persons.append(person)
        self.id_map[str(person.id)] = person

    def get_by_id(self, person_id: int):
        return self.id_map.get(str(person_id), None)

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
            return self
        return NotImplemented

    def __repr__(self):
        return f"PersonCollection({self.persons})"
