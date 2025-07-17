from logging import getLogger

from modules.persons.src.parser.names_parser.constants.last_name_prefixes import (
    LAST_NAME_PREFIXES_MAP,
    SPECIAL_LAST_NAMES_MAP,
)

logger = getLogger(__name__)

# TODO: simplify handling of multi-part last names_parser


def _spaced_word_to_camel_case(text: str) -> str:
    return "".join(word.capitalize() for word in text.split(" "))


def _merge_multi_part_last_names(text: str, keyword: str) -> str:
    name_parts = text.lower().split(keyword, 1)
    name_parts = [part for part in name_parts if part != ""]

    return f"{name_parts[0].title()} {LAST_NAME_PREFIXES_MAP[keyword]}{name_parts[1].title()}"


def _merge_multi_part_last_names_with_dash(text: str, keyword: str) -> str:
    camel_cased_keyword = _spaced_word_to_camel_case(keyword)
    keyword = keyword.lstrip()
    text = text.strip()

    if text.startswith("-"):
        if text[1:].strip().startswith(keyword):
            text = text[1:].replace(keyword, "").strip()

            return f"-{camel_cased_keyword}{text.title()}"

    keyword_position = text.find(keyword)
    if keyword_position == -1:
        logger.warning(f"Keyword '{keyword}' not found in '{text}'")
        return text

    before = text[keyword_position - 1] if keyword_position > 0 else ""
    after = (
        text[keyword_position + len(keyword)]
        if keyword_position + len(keyword) < len(text)
        else ""
    )

    if before == "-" or after == "-":
        updated = (
            text[:keyword_position].title()
            + camel_cased_keyword
            + text[keyword_position + len(keyword) :].title()
        )
        return updated
    else:
        logger.warning(
            f"Problem while parsing special last name with dash for '{keyword}' in '{text}'"
        )
        return text


def _merge_multi_part_last_names_at_start(text: str, keyword: str) -> str:
    name_parts = text.lower().split(keyword[1:], 1)
    name_parts = [part.strip() for part in name_parts if part != ""]

    if len(keyword.strip().split(" ")) > 1:
        return f"{LAST_NAME_PREFIXES_MAP[keyword]} {name_parts[0].title()}"

    return f"{LAST_NAME_PREFIXES_MAP[keyword]}{name_parts[0].title()}"


def _merge_special_last_names(text: str, keyword: str) -> str:
    name_parts = [
        part.strip() for part in text.split(keyword.strip(), 1) if part.strip()
    ]

    if "-" in text:
        camel_cased_keyword = _spaced_word_to_camel_case(keyword)
        keyword = keyword.strip()
        text = text.strip()

        if text.startswith("-"):
            if text[1:].strip().startswith(keyword):
                text = text[1:].replace(keyword, "").strip()

                return f"-{camel_cased_keyword} {text.title()}"

        keyword_position = text.find(keyword)

        if text[keyword_position - 1] == "-":
            text = text.replace("-" + keyword, "-" + camel_cased_keyword)
            return (
                text[:keyword_position].title()
                + camel_cased_keyword
                + " "
                + text[keyword_position + len(keyword) - 1 :].strip().title()
            )
        else:
            return f"{camel_cased_keyword}{text[keyword_position + len(keyword) :].strip().title()}"

    if len(name_parts) == 1:
        return f"{SPECIAL_LAST_NAMES_MAP[keyword]} {name_parts[0].title()}"

    return f"{name_parts[0].title()} {SPECIAL_LAST_NAMES_MAP[keyword]} {name_parts[1].title()}"


def find_multi_part_last_names_keyword(text: str) -> str | None:
    text = text.lower()
    text = text.replace("-", " ")

    keywords_maps = list(SPECIAL_LAST_NAMES_MAP.keys()) + list(
        LAST_NAME_PREFIXES_MAP.keys()
    )

    for keyword in keywords_maps:
        if text.startswith(keyword[1:]) or keyword in text:
            return keyword

    return None


def handle_multi_part_last_names(text: str, keyword: str) -> str:
    text = text.lower()

    if keyword in SPECIAL_LAST_NAMES_MAP:
        return _merge_special_last_names(text, keyword)

    if keyword in text:
        return _merge_multi_part_last_names(text, keyword)

    if text.startswith(keyword[1:]):
        return _merge_multi_part_last_names_at_start(text, keyword)

    if "-" in text and text.replace("-", " ").__contains__(keyword.strip()):
        return _merge_multi_part_last_names_with_dash(text, keyword)

    logger.error(f"Could not find '{keyword}' in '{text}'")

    return text
