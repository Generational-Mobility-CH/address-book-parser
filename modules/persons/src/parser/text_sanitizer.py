import re

from modules.persons.src.common.special_chars import (
    ALLOWED_SPECIAL_CHARS,
    UNALLOWED_STRINGS,
    UNALLOWED_AT_START_OF_STRING,
    UNALLOWED_WORDS,
)
from modules.persons.src.models.address_book.addressBookPage import AddressBookPage


def clean_text_columns_and_split_into_lines(page: AddressBookPage) -> AddressBookPage:
    page.text_columns = {
        col_id: clean_text_lines(col_text.split("\n"))
        for col_id, col_text in page.text_columns.items()
    }

    return page


def clean_text_lines(text: list[str]) -> list[str]:
    result = []

    for i, line in enumerate(text):
        if i + 1 < len(text):
            if has_line_break(line, text[i + 1]):
                line = merge_line_break(line, text[i + 1].strip())
                text[i + 1] = ""

        line = sanitize_line(line)

        if any(char.isalnum() for char in line):
            result.append(line)

    return result


def has_line_break(line: str, next_line: str) -> bool:
    ends_with_dash_or_number = bool(line) and (
        line.endswith("-") or line[-1].isnumeric()
    )
    next_line_starts_with_number = next_line.strip()[:1].isdigit()

    return ends_with_dash_or_number or next_line_starts_with_number


def merge_line_break(current_line: str, next_line: str) -> str:
    if next_line.lower().startswith("und"):
        next_line = " und" + next_line[3:]

    line = current_line + " " + next_line

    return line.replace("- ", "")


def sanitize_line(line: str) -> str:
    line = remove_unallowed_keywords(line)
    line = clean_up_parenthesis(line)

    return line.strip()


def remove_unallowed_keywords(
    line: str,
    allowed_chars: list = ALLOWED_SPECIAL_CHARS,
    disallowed_strings: list = UNALLOWED_STRINGS,
    disallowed_prefixes: list = UNALLOWED_AT_START_OF_STRING,
    disallowed_words: list = UNALLOWED_WORDS,
) -> str:
    for prefix in disallowed_prefixes:
        if line.startswith(prefix):
            line = line[len(prefix) :].lstrip()

    for substring in disallowed_strings:
        line = line.replace(substring, "")

    line = " ".join(word for word in line.split() if word not in disallowed_words)

    line = "".join(char for char in line if char in allowed_chars or char.isalnum())

    return line.strip()


def clean_up_parenthesis(line: str) -> str:
    line = remove_empty_parenthesis(line)
    line = remove_unmatched_parenthesis(line)

    return line.strip()


def remove_empty_parenthesis(line: str) -> str:
    return re.sub(r"\(\s*\)", "", line)


def remove_unmatched_parenthesis(line: str) -> str:
    unmatched_parenthesis_positions = set()

    for index, char in enumerate(line):
        if char == "(":
            unmatched_parenthesis_positions.add(index)
        elif char == ")":
            if unmatched_parenthesis_positions:
                for i in unmatched_parenthesis_positions:
                    if line[i] == "(":
                        unmatched_parenthesis_positions.remove(i)
                        break
            else:
                unmatched_parenthesis_positions.add(index)

    if unmatched_parenthesis_positions:
        line = "".join(
            char
            for index, char in enumerate(line)
            if index not in unmatched_parenthesis_positions
        )

    return line
