from modules.persons.src.models.person.person_names import PersonNames
from modules.persons.src.parser.constants.tags import TAG_NONE_FOUND
from modules.persons.src.parser.names_parser.names_parser import parse_names
from modules.persons.src.parser.names_parser.special_last_names_parser import (
    find_multi_part_last_names_keyword,
    handle_multi_part_last_names,
)


def _safe_name(text: str) -> str:
    return text if text != TAG_NONE_FOUND else ""


def clean_last_names(all_names: PersonNames) -> PersonNames:
    if special_last_name_keyword := find_multi_part_last_names_keyword(
        all_names.last_names
    ):
        all_names.last_names = handle_multi_part_last_names(
            all_names.last_names, special_last_name_keyword
        )

        all_names = f"{_safe_name(all_names.last_names)} {_safe_name(all_names.first_names)}".strip()

        return parse_names(all_names)

    return all_names
