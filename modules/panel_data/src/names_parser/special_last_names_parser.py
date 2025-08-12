from modules.panel_data.src.names_parser.constants.last_name_prefixes import (
    LAST_NAME_PREFIXES_MAP,
)
from modules.persons.src.util.regex.substitute_with_map import substitute_with_map


def merge_last_names_with_prefixes(text: str) -> str:
    text = substitute_with_map(
        text,
        LAST_NAME_PREFIXES_MAP,
        r"\b{PLACEHOLDER}\s+",
        r"(\b\w+\b)",
        r"\1",
    )

    return text
