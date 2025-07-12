from logging import getLogger

from modules.persons.src.parser.names_parser.constants.last_name_prefixes import (
    LAST_NAME_PREFIXES_MAP,
    SPECIAL_LAST_NAMES_MAP,
)

logger = getLogger(__name__)

# TODO: simplify handling of multi-part last names_parser


def _spaced_word_to_camel_case(data: str) -> str:
    return "".join(word.capitalize() for word in data.split(" "))


def _merge_multi_part_last_names(data: str, keyword: str) -> str:
    name_parts = data.lower().split(keyword, 1)
    name_parts = [part for part in name_parts if part != ""]

    return f"{name_parts[0].title()} {LAST_NAME_PREFIXES_MAP[keyword]}{name_parts[1].title()}"


def _merge_multi_part_last_names_with_dash(data: str, keyword: str) -> str:
    camel_cased_keyword = _spaced_word_to_camel_case(keyword)
    keyword = keyword.lstrip()
    data = data.strip()

    if data.startswith("-"):
        if data[1:].strip().startswith(keyword):
            data = data[1:].replace(keyword, "").strip()

            return f"-{camel_cased_keyword}{data.title()}"

    keyword_position = data.find(keyword)
    if keyword_position == -1:
        logger.warning(f"Keyword '{keyword}' not found in '{data}'")
        return data

    before = data[keyword_position - 1] if keyword_position > 0 else ""
    after = (
        data[keyword_position + len(keyword)]
        if keyword_position + len(keyword) < len(data)
        else ""
    )

    if before == "-" or after == "-":
        updated = (
            data[:keyword_position].title()
            + camel_cased_keyword
            + data[keyword_position + len(keyword) :].title()
        )
        return updated
    else:
        logger.warning(
            f"Problem while parsing special last name with dash for '{keyword}' in '{data}'"
        )
        return data


def _merge_multi_part_last_names_at_start(data: str, keyword: str) -> str:
    name_parts = data.lower().split(keyword[1:], 1)
    name_parts = [part.strip() for part in name_parts if part != ""]

    if len(keyword.strip().split(" ")) > 1:
        return f"{LAST_NAME_PREFIXES_MAP[keyword]} {name_parts[0].title()}"

    return f"{LAST_NAME_PREFIXES_MAP[keyword]}{name_parts[0].title()}"


def _merge_special_last_names(data: str, keyword: str) -> str:
    name_parts = [
        part.strip() for part in data.split(keyword.strip(), 1) if part.strip()
    ]

    if data.__contains__("-"):
        camel_cased_keyword = _spaced_word_to_camel_case(keyword)
        keyword = keyword.strip()
        data = data.strip()

        if data.startswith("-"):
            if data[1:].strip().startswith(keyword):
                data = data[1:].replace(keyword, "").strip()

                return f"-{camel_cased_keyword} {data.title()}"

        keyword_position = data.find(keyword)

        if data[keyword_position - 1] == "-":
            data = data.replace("-" + keyword, "-" + camel_cased_keyword)
            return (
                data[:keyword_position].title()
                + camel_cased_keyword
                + " "
                + data[keyword_position + len(keyword) - 1 :].strip().title()
            )
        else:
            return f"{camel_cased_keyword}{data[keyword_position + len(keyword) :].strip().title()}"

    if len(name_parts) == 1:
        return f"{SPECIAL_LAST_NAMES_MAP[keyword]} {name_parts[0].title()}"

    return f"{name_parts[0].title()} {SPECIAL_LAST_NAMES_MAP[keyword]} {name_parts[1].title()}"


def find_multi_part_last_names_keyword(data: str) -> str | None:
    data = data.lower()
    data = data.replace("-", " ")

    keywords_maps = list(SPECIAL_LAST_NAMES_MAP.keys()) + list(
        LAST_NAME_PREFIXES_MAP.keys()
    )

    for keyword in keywords_maps:
        if data.startswith(keyword[1:]) or keyword in data:
            return keyword

    return None


def handle_multi_part_last_names(data: str, keyword: str) -> str:
    data = data.lower()

    if keyword in SPECIAL_LAST_NAMES_MAP:
        return _merge_special_last_names(data, keyword)

    if keyword in data:
        return _merge_multi_part_last_names(data, keyword)

    if data.startswith(keyword[1:]):
        return _merge_multi_part_last_names_at_start(data, keyword)

    if data.__contains__("-") and data.replace("-", " ").__contains__(keyword.strip()):
        return _merge_multi_part_last_names_with_dash(data, keyword)

    logger.error(f"Could not find '{keyword}' in '{data}'")

    return data
