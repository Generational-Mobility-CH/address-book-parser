from modules.common.special_chars import ALLOWED_SPECIAL_CHARS
from modules.models.addressBookPage import AddressBookPage
from modules.persons_parser.src.text_sanitizer.line_breaks_merger import (
    has_line_break,
    merge_line_break,
    ends_with_number,
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
        line = remove_unallowed_characters(line.strip())

        if (
            line
            and (has_line_break(line) or ends_with_number(line))
            and i + 1 < len(text)
        ):
            line = merge_line_break(line, text[i + 1].strip())
            text[i + 1] = ""

        line = line.strip()

        if line:
            result.append(line)

    return result


def remove_unallowed_characters(line: str) -> str:
    output_line = ""
    for char in line:
        if char.isalnum() or char in ALLOWED_SPECIAL_CHARS:
            output_line = output_line + char

    return output_line
