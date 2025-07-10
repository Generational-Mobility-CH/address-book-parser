from modules.persons.src.cleaner.last_names_cleaner import clean_last_names
from modules.persons.src.common.special_chars import TAG_NONE_FOUND
from modules.persons.src.models.person.person import Person
from modules.persons.src.models.person.person_names import PersonNames
from modules.persons.src.parser.names.names_separator import separate_names


def clean_person(person: Person) -> Person:
    person.last_names = clean_last_names(person.last_names)

    re_separated_names = re_separate_names(person.first_names, person.last_names)
    person.first_names = re_separated_names.first_names
    person.last_names = re_separated_names.last_names

    return person


def re_separate_names(first_names: str, last_names: str) -> PersonNames:
    all_names = f"{safe_name(last_names)} {safe_name(first_names)}".strip()

    return separate_names(all_names)


def safe_name(text: str) -> str:
    return text if text != TAG_NONE_FOUND else ""
