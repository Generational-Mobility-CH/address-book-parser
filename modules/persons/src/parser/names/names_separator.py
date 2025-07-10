import logging
import re

from modules.persons.src.models.person.person_names import PersonNames
from modules.persons.src.parser.constants.tags import TAG_NONE_FOUND
from modules.persons.src.parser.names.constants.names_keywords import (
    KEYWORDS_DIVORCED,
    KEYWORDS_NAMES_SEPARATOR,
)

logger = logging.getLogger(__name__)


def separate_names(original_names: str) -> PersonNames:
    separated_names: PersonNames = PersonNames(
        last_names=TAG_NONE_FOUND, first_names=TAG_NONE_FOUND
    )

    if found_marker := get_separation_marker(original_names):
        return split_at_marker(original_names, found_marker)

    name_parts = original_names.split(" ")

    match len(name_parts):
        case 1:
            unmerged_names = unmerge_name_parts(name_parts[0])

            if len(unmerged_names.split(" ")) == 1:
                separated_names.last_names = unmerged_names.strip()
            else:
                return separate_names(unmerged_names)
        case 2:
            separated_names.last_names = name_parts[0]
            separated_names.first_names = name_parts[1]
        case 3:
            separated_names.last_names = f"{name_parts[0]} {name_parts[1]}"
            separated_names.first_names = name_parts[2]
        case 4:
            separated_names.last_names = f"{name_parts[0]} {name_parts[1]}"
            separated_names.first_names = f"{name_parts[2]} {name_parts[3]}"
        case _:
            logger.warning(f"Could not parse name: {original_names}")
            separated_names.last_names = original_names

    return separated_names


def get_separation_marker(data: str) -> str | None:
    for marker in KEYWORDS_DIVORCED:
        if marker in data.lower():
            pattern = rf"^.*?{re.escape(marker)}\s+(?:\(\S+\)|\S+)\s+(.*)$"
            match = re.match(pattern, data.lower())
            if match:
                return match.group(1).strip()

    for marker in KEYWORDS_NAMES_SEPARATOR:
        if marker in data.lower():
            return marker

    first_name_abbreviation_pattern = r"\b\w{1,3}\."
    match = re.search(first_name_abbreviation_pattern, data.lower())
    if match:
        return match.group(0)

    return None


def split_at_marker(data: str, marker: str) -> PersonNames:
    s = data.lower()
    parts = s.split(marker, 1)

    name_parts = PersonNames(last_names="", first_names=marker.strip().title())

    name_parts.last_names += (
        " ".join(word for word in parts[0].split(" ")).title().strip()
    )

    name_parts.first_names += (
        " ".join(word for word in parts[1].split(" ")).title().strip()
    )

    return name_parts


def unmerge_name_parts(data: str) -> str:
    """
    Separate names by looking at changes from lower-case to upper-case within the string.
    E.g.: 'MüllerMeier' -> 'Müller Meier'
    """
    s = re.split(r"(?<![ -])(?=[A-ZÄÖÜẞ])", data)
    s = " ".join([part.strip() for part in s if part.strip()])

    return s
