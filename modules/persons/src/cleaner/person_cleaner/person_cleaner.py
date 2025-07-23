from modules.persons.src.cleaner.person_cleaner.address_cleaner import clean_address
from modules.persons.src.cleaner.person_cleaner.first_names_cleaner import (
    clean_first_names,
)
from modules.persons.src.util.apply_regex_patterns import apply_regex_patterns
from modules.persons.src.cleaner.text_cleaner.words_separator import (
    SEPARATE_WORDS_PATTERNS_AND_REPL,
)
from modules.persons.src.models.person.person import Person
from modules.persons.src.models.person.person_names import PersonNames


def clean_person(person: Person) -> Person:
    all_names = PersonNames(person.first_names, person.last_names)

    all_names = clean_first_names(all_names)

    cleaned_first_names = apply_regex_patterns(
        all_names.first_names, SEPARATE_WORDS_PATTERNS_AND_REPL
    ).title()  # TODO: title still needed here ???

    person.first_names = cleaned_first_names

    person.address = clean_address(person.address)

    return person
