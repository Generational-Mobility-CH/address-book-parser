import logging
import re

from modules.persons.common.special_chars import (
    TAG_NONE_FOUND,
    KEYWORDS_NAMES_SPLITTING,
)
from modules.persons.models.person.person_names import PersonNames


logger = logging.getLogger(__name__)


def separate_names(original_names: str) -> PersonNames:
    separated_names: PersonNames = PersonNames(
        last_names=TAG_NONE_FOUND, first_names=TAG_NONE_FOUND
    )
    found_marker: str | None = get_splitting_marker(original_names)

    if found_marker:
        separated_names = split_at_marker(original_names, found_marker)

    # elif any(
    #     substr in original_names.lower() for substr in KEYWORDS_SPECIAL_LAST_NAMES
    # ):
    #     separated_names = separate_special_last_names(original_names)

    else:
        parts = original_names.split(" ")

        match len(parts):
            case 1:
                unmerged_names = unmerge_name_parts(parts[0])

                if len(unmerged_names.split(" ")) == 1:
                    separated_names.last_names = unmerged_names.strip()
                else:
                    separated_names = separate_names(unmerged_names)
                    return separated_names  # TODO: make sure this works
            case 2:
                separated_names.last_names = parts[0]
                separated_names.first_names = parts[1]
            case 3:
                separated_names.last_names = f"{parts[0]} {parts[1]}"
                separated_names.first_names = parts[2]
            case 4:
                separated_names.last_names = f"{parts[0]} {parts[1]}"
                separated_names.first_names = f"{parts[2]} {parts[3]}"
            case _:
                logger.error(f"Could not parse name: {original_names}")
                separated_names.last_names = original_names

    return separated_names


def get_splitting_marker(data: str) -> str | None:
    found_marker = None

    for marker in KEYWORDS_NAMES_SPLITTING:
        if marker in data.lower():
            found_marker = marker
            break

    if found_marker is None:
        first_name_abbreviation_pattern = r"\b\w{1,3}\."
        match = re.search(first_name_abbreviation_pattern, data.lower())
        if match:
            found_marker = match.group(0)

    return found_marker


def split_at_marker(data: str, marker: str) -> PersonNames:
    s = data.lower()
    parts = s.split(marker, 1)

    name_parts = PersonNames(last_names="", first_names=marker.strip().capitalize())
    name_parts.last_names += " ".join(
        word.capitalize().strip() for word in parts[0].split(" ")
    )
    name_parts.first_names += " ".join(
        word.capitalize().strip() for word in parts[1].split(" ")
    )

    return name_parts


def unmerge_name_parts(data: str) -> str:
    marker = "|"

    s = re.split(r"(?<![ -])(?=[A-ZÄÖÜẞ])", data)
    s = " ".join([part.strip() for part in s if part.strip()])

    # TODO: check if this is adding parentheses where it shouldn't
    # Abom( Helene
    s = s.replace(")", f"){marker}")
    s = s.replace("(", " (")

    s = s.replace("—", marker)
    s = s.replace("-", marker)

    return s.replace(marker, " ").strip()


def separate_special_last_names(original_names: str) -> PersonNames:
    pass
