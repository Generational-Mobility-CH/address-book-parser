from modules.persons.src.models.person.person_names import PersonNames


def clean_first_names(names: PersonNames) -> PersonNames:
    if "-" in names.last_names:
        first, separator, second = names.last_names.partition("-")
        if second:
            return PersonNames(first, second)

    return names
