from modules.panel_data.src.models.person_names import PersonNames
from modules.panel_data.src.names_handler.last_and_first_names_separator import (
    separate_names_legacy,
)
from modules.persons_data_processor.src.parser.constants.tags import TAG_NONE_FOUND
from modules.persons_data_processor.src.text_cleaner.words_separator import (
    SEPARATE_WORDS_PATTERNS_AND_REPL,
)
from modules.persons_data_processor.src.utility.regex.apply_regex_patterns import (
    apply_regex_patterns,
)


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

        return separate_names_legacy(names.last_names)

    return names
