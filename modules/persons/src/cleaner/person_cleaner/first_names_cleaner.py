from modules.persons.src.models.person.person_names import PersonNames
from modules.persons.src.parser.constants.tags import TAG_NONE_FOUND
from modules.persons.src.parser.names_parser.names_separator import separate_names


def clean_first_names(names: PersonNames) -> PersonNames:
    if names.first_names == TAG_NONE_FOUND and names.last_names not in [
        TAG_NONE_FOUND,
        "",
    ]:
        if "-" in names.last_names:
            first, separator, second = names.last_names.partition("-")
            if second:
                return PersonNames(first, second)

        return separate_names(names.last_names)

    return names
