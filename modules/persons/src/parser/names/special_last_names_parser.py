from logging import getLogger

from modules.persons.src.common.special_chars import SPECIAL_LAST_NAMES_MAP


logger = getLogger(__name__)


def find_special_last_name_keyword(data: str) -> str | None:
    for keyword in SPECIAL_LAST_NAMES_MAP:
        if keyword in data.lower():
            return keyword

        if data.lower().startswith(keyword[1:]):
            return keyword

    return None


def handle_special_last_names(data: str, keyword: str) -> str:
    if keyword in data.lower():
        return merge_special_last_names(data, keyword)

    if data.lower().startswith(keyword[1:]):
        return merge_special_last_names_at_start(data, keyword)

    logger.error(f"Could not find '{keyword}' in '{data.lower()}'")

    return data


def merge_special_last_names(original_names: str, keyword: str) -> str:
    name_parts = original_names.lower().split(keyword, 1)
    name_parts = [part for part in name_parts if part != ""]

    if len(name_parts) == 1:
        return f"{SPECIAL_LAST_NAMES_MAP[keyword]}{name_parts[0].title()}"

    if keyword.__contains__("roche"):
        return f"{name_parts[0].title()} {SPECIAL_LAST_NAMES_MAP[keyword]} {name_parts[1].title()}"

    return f"{name_parts[0].title()} {SPECIAL_LAST_NAMES_MAP[keyword]}{name_parts[1].title()}"


def merge_special_last_names_at_start(names: str, keyword: str) -> str:
    name_parts = names.lower().split(keyword[1:], 1)
    name_parts = [part.strip() for part in name_parts if part != ""]

    if len(keyword.strip().split(" ")) > 1:
        return f"{SPECIAL_LAST_NAMES_MAP[keyword]} {name_parts[0].title()}"

    return f"{SPECIAL_LAST_NAMES_MAP[keyword]}{name_parts[0].title()}"


def spaced_word_to_came_case(s: str) -> str:
    return " ".join(word.capitalize() for word in s.split(" "))
