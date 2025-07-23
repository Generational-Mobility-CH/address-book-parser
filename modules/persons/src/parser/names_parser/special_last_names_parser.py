import re

from modules.persons.src.parser.names_parser.constants.last_name_prefixes import (
    LAST_NAME_PREFIXES_MAP,
)


LAST_NAMES_PREFIXES_PATTERN = re.compile(
    "|".join(
        rf"\b{k}\s+" for k in sorted(LAST_NAME_PREFIXES_MAP, key=len, reverse=True)
    ),
    flags=re.IGNORECASE,
)


def merge_last_names_with_prefixes(text: str) -> str:
    found_prefixes = set(LAST_NAMES_PREFIXES_PATTERN.findall(text))

    if found_prefixes:
        for prefix in found_prefixes:
            key = prefix.strip().lower()
            repl = LAST_NAME_PREFIXES_MAP[key]
            text = re.sub(rf"{prefix}(\b\w+\b)", rf"{repl}\1", text)

    return text
