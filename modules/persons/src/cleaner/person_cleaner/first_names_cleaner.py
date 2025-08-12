from modules.panel_data.src.names_parser.names_parser import parse_names
from modules.persons.src.cleaner.text_cleaner.words_separator import (
    SEPARATE_WORDS_PATTERNS_AND_REPL,
)
from modules.persons.src.models.person.person_names import PersonNames
from modules.persons.src.parser.constants.tags import TAG_NONE_FOUND
from modules.persons.src.util.regex.apply_regex_patterns import apply_regex_patterns


def clean_first_names(names: PersonNames) -> PersonNames:
    if names.first_names == TAG_NONE_FOUND and names.last_names not in [
        TAG_NONE_FOUND,
        "",
    ]:
        if "-" in names.last_names:
            first, separator, second = names.last_names.partition("-")
            if second:
                first_names = apply_regex_patterns(
                    first, SEPARATE_WORDS_PATTERNS_AND_REPL
                )
                return PersonNames(first_names, second)

        return parse_names(names.last_names)

    return names
