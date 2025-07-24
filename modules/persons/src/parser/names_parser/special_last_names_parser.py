from modules.persons.src.parser.names_parser.constants.last_name_prefixes import (
    LAST_NAME_PREFIXES_MAP,
)
from modules.persons.src.util.regex.substitute_with_map import substitute_with_map


LAST_NAMES_PREFIXES_PATTERN_FORMAT = r"\b{PLACEHOLDER}\s+"
LAST_NAMES_PREFIXES_SUB_PAT_ADD = r"(\b\w+\b)"
LAST_NAMES_PREFIXES_REPL_ADD = r"\1"


def merge_last_names_with_prefixes(text: str) -> str:
    text = substitute_with_map(
        text,
        LAST_NAME_PREFIXES_MAP,
        LAST_NAMES_PREFIXES_PATTERN_FORMAT,
        LAST_NAMES_PREFIXES_SUB_PAT_ADD,
        LAST_NAMES_PREFIXES_REPL_ADD,
    )

    return text
