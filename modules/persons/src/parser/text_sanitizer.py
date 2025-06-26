import re

from modules.persons.models.address_book.addressBookPage import AddressBookPage
from modules.persons.common.special_chars import (
    ALLOWED_SPECIAL_CHARS,
    UNALLOWED_STRINGS,
    UNALLOWED_AT_START_OF_STRING,
    UNALLOWED_WORDS,
)


def clean_text_columns_and_split_into_lines(page: AddressBookPage) -> AddressBookPage:
    page.text_columns = {
        col_id: clean_text_lines(col_text.split("\n"))
        for col_id, col_text in page.text_columns.items()
    }
    return page


def clean_text_lines(text: list[str]) -> list[str]:
    result = []

    for i, line in enumerate(text):
        if has_line_break(line) and i + 1 < len(text):
            line = merge_line_break(line, text[i + 1].strip())
            text[i + 1] = ""

        line = sanitize_line(line)

        if any(char.isalnum() for char in line):
            result.append(line)

    return result


def has_line_break(line: str) -> bool:
    return bool(line) and (line.endswith("-") or line[-1].isnumeric())


def sanitize_line(line: str) -> str:
    line = clean_line(line)
    line = clean_up_parenthesis(line)
    return line.strip()


def clean_line(
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
    line = re.sub(r"\(\s*\)", "", line)

    unmatched_opening_parenthesis_positions = set()

    for index, char in enumerate(line):
        if char == "(":
            unmatched_opening_parenthesis_positions.add(index)
        elif char == ")":
            if unmatched_opening_parenthesis_positions:
                unmatched_opening_parenthesis_positions.pop()
            else:
                pass

    if unmatched_opening_parenthesis_positions:
        line = "".join(
            char
            for index, char in enumerate(line)
            if index not in unmatched_opening_parenthesis_positions
        )

    return line


def merge_line_break(current_line: str, next_line: str) -> str:
    if next_line.lower().startswith("und"):
        next_line = next_line.replace("und", " und")

    line = current_line + " " + next_line

    return line.replace("- ", "")
