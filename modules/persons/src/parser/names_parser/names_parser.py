import logging
import re

from modules.persons.src.models.person.person_names import PersonNames
from modules.persons.src.parser.constants.tags import TAG_NONE_FOUND
from modules.persons.src.parser.names_parser.constants.names_special_keywords import (
    KEYWORDS_DIVORCED,
    KEYWORDS_NAMES_SEPARATOR,
)

logger = logging.getLogger(__name__)


def _get_separation_marker(data: str) -> str | None:
    data = data.lower()

    for marker in KEYWORDS_NAMES_SEPARATOR:
        if marker in data:
            return marker

    # Info: (Mostly) only first names are shortened and end with "." (E.g. 'Joh.'->'Johannes')
    for i, part in enumerate(data.split(" ")[1:]):
        is_reserved_keyword = part in KEYWORDS_DIVORCED
        part = part.strip()
        if part.endswith(".") and not is_reserved_keyword:
            p = [p.strip() for p in part.split(" ") if p.strip()][0]
            return p

    return None


def _find_divorced_keyword(data: str) -> str | None:
    for marker in KEYWORDS_DIVORCED:
        if marker in data.lower():
            return marker

    return None


# TODO: better name for diz
def _handle_divorced(data: str, keyword: str) -> str:
    data = data.lower()

    if keyword not in data:
        logger.error(f"Keyword '{keyword}' not found in '{data}'")
        return data

    keyword_start = data.find(keyword)
    start = data[:keyword_start].strip().title()
    keyword_match = keyword
    for i in range(keyword_start + len(keyword), len(data) - 1):
        if data[i].isspace():
            break
        keyword_match += data[i]

    end = data[keyword_start + len(keyword_match) :].strip().title()
    keyword_match = keyword_match.title().replace(" ", "")

    if end.startswith("-"):
        return f"{start}{keyword_match}{end}"

    return f"{start}{keyword_match} {end}"


def _split_at_marker(data: str, keyword: str) -> PersonNames:
    data = data.lower()
    parts = data.split(keyword, 1)
    keyword = keyword.strip().title()
    last_names = " ".join(word for word in parts[0].split(" ")).title().strip()
    person_names = PersonNames(last_names=last_names, first_names=keyword)

    if len(parts) == 2:
        sub_parts = parts[1].strip().split(" ")
        for part in sub_parts:
            person_names.first_names += " " + part.title().strip()

    person_names.first_names = person_names.first_names.strip()

    return person_names


def _ensure_space_after_dot(data: str) -> str:
    # Info: E.g. 'Rob.Saml.' -> 'Rob. Saml.'
    return re.sub(r"(?<=[A-ZÄÖÜẞa-zäöü]\.)(?=[a-zäöüA-ZÄÖÜẞ])", " ", data)


def _split_on_camel_case(data: str) -> str:
    # Info: E.g. 'MüllerMeier' -> 'Müller Meier'
    result = data[0]
    for i in range(1, len(data) - 2):
        result += data[i]
        if data[i].islower() and data[i + 1].isupper():
            result += " "

    result += data[len(data) - 2 :]

    return result


def unmerge_name_parts(data: str) -> str:
    data = _split_on_camel_case(data)
    data = _ensure_space_after_dot(data)

    return data


def parse_names(original_names: str) -> PersonNames:
    separated_names: PersonNames = PersonNames(
        last_names=TAG_NONE_FOUND, first_names=TAG_NONE_FOUND
    )
    original_names = unmerge_name_parts(original_names).strip()

    if divorced_keyword := _find_divorced_keyword(original_names):
        original_names = _handle_divorced(original_names, divorced_keyword)

    if found_marker := _get_separation_marker(original_names):
        return _split_at_marker(original_names, found_marker)

    name_parts = original_names.split(" ")

    match len(name_parts):
        case 1:
            if (
                "-" in original_names
                and not original_names.endswith("-")
                and not original_names.startswith("-")
            ):
                name_parts = original_names.split("-", 1)
                separated_names.last_names = name_parts[0]
                separated_names.first_names = name_parts[1]
            else:
                logger.warning(f"TODO check dizz only 1 part: {original_names}")
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
            # TODO:
            # for i, part in enumerate(name_parts):
            #     part = part.strip()
            #     if i > 0 and part.startswith("("):
            #         name_parts = [name_parts[i - 1] + name_parts[i]] + name_parts[i + 1:]
            #         new_original_names = " ".join(part for part in name_parts)
            #         return parse_names(new_original_names)
            #     elif any(key in part for key in SPECIAL_LAST_NAMES_MAP.values()):
            #         continue
            #     elif "-" in part:
            #         continue

            logger.warning(f"Could not parse name: {original_names}")
            separated_names.last_names = original_names

    return separated_names
