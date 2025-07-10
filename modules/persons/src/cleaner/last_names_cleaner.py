from modules.persons.src.parser.names.special_last_names_parser import (
    find_special_last_name_keyword,
    handle_special_last_names,
)


def clean_last_names(text: str) -> str:
    if special_last_name_keyword := find_special_last_name_keyword(text):
        text = handle_special_last_names(text, special_last_name_keyword)

    return text
