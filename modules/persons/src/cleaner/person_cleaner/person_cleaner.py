from modules.persons.src.cleaner.person_cleaner.first_names_cleaner import (
    clean_first_names,
)
from modules.persons.src.cleaner.person_cleaner.last_names_cleaner import (
    clean_last_names,
)
from modules.persons.src.models.person.person import Person
from modules.persons.src.models.person.person_names import PersonNames
from modules.persons.src.parser.names_parser.names_parser import unmerge_name_parts


def clean_person(person: Person) -> Person:
    all_names = PersonNames(person.first_names, person.last_names)

    all_names = clean_last_names(all_names)
    all_names = clean_first_names(all_names)

    all_names = PersonNames(
        first_names=unmerge_name_parts(all_names.first_names).title(),
        last_names=unmerge_name_parts(all_names.last_names).title(),
    )

    person.first_names = all_names.first_names
    person.last_names = all_names.last_names

    return person
