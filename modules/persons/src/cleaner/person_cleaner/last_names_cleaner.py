from modules.persons.src.parser.names_parser.special_last_names_parser import (
    find_multi_part_last_names_keyword,
    handle_multi_part_last_names,
)


def clean_last_names(text: str) -> str:
    if special_last_name_keyword := find_multi_part_last_names_keyword(text):
        text = handle_multi_part_last_names(text, special_last_name_keyword)

    return text
