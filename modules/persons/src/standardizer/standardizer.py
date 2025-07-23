from modules.persons.src.models.person.person import Person
from modules.persons.src.standardizer.street_name_standardizer.street_name_standardizer import (
    standardize_street_name,
)


def standardize(person: Person) -> Person:
    person.address.street_name = standardize_street_name(person.address.street_name)

    return person
