from modules.persons.src.common.special_chars import SPECIAL_LAST_NAMES_MAP


def handle_special_last_names_if_present(names: str) -> str:
    for key in SPECIAL_LAST_NAMES_MAP:
        if key in names.lower():
            return merge_special_last_names(names, key)
        if names.lower().startswith(key[1:]):
            return merge_special_last_names_at_start(names, key)

    return names


def merge_special_last_names(original_names: str, keyword: str) -> str:
    name_parts = original_names.lower().split(keyword, 1)
    name_parts = [part for part in name_parts if part != ""]

    if len(name_parts) == 1:
        return f"{SPECIAL_LAST_NAMES_MAP[keyword]}{name_parts[0].title()}"

    return f"{name_parts[0].title()} {SPECIAL_LAST_NAMES_MAP[keyword]}{name_parts[1].title()}"


def merge_special_last_names_at_start(names: str, keyword: str) -> str:
    name_parts = names.lower().split(keyword[1:], 1)
    name_parts = [part.strip() for part in name_parts if part != ""]

    return f"{SPECIAL_LAST_NAMES_MAP[keyword]}{name_parts[0].title()}"


def spaced_word_to_came_case(s: str) -> str:
    return " ".join(word.capitalize() for word in s.split(" "))
