from modules.persons.src.cleaner.constants.allowed_special_characters import (
    ALLOWED_SPECIAL_CHARACTERS,
)
from modules.persons.src.cleaner.constants.unallowed_strings import (
    UNALLOWED_AT_START_OF_STRING,
    UNALLOWED_STRINGS,
)


def remove_unallowed_strings(line: str) -> str:
    for prefix in UNALLOWED_AT_START_OF_STRING:
        if line.startswith(prefix):
            line = line[len(prefix) :]

    line = remove_partial_matches(line)

    line = "".join(
        char for char in line if char in ALLOWED_SPECIAL_CHARACTERS or char.isalnum()
    )

    return line


def remove_partial_matches(line: str) -> str:
    for keyword in UNALLOWED_STRINGS:
        line = line.replace(keyword, "")

    return line.strip()
