from modules.persons.src.cleaner.text_cleaner.dashes_handler import clean_up_dashes
from modules.persons.src.cleaner.text_cleaner.line_breaks_handler import (
    has_line_break,
    merge_line_break,
)
from modules.persons.src.cleaner.text_cleaner.parenthesis_handler import (
    clean_up_parenthesis,
)
from modules.persons.src.cleaner.text_cleaner.unallowed_strings_remover import (
    remove_unallowed_strings,
)


def _clean_up_white_space(line: str) -> str:
    return " ".join(line.strip().split())


def _clean_line(line: str) -> str:
    line = _clean_up_white_space(line)
    line = remove_unallowed_strings(line)
    line = clean_up_dashes(line)
    line = clean_up_parenthesis(line)
    line = _clean_up_white_space(line)

    if not any(char.isalpha() for char in line):
        return ""

    return line


def clean_text_lines(text: list[str]) -> list[str]:
    result = []
    text = list(filter(None, text))

    for i, line in enumerate(text):
        line = _clean_line(line)

        if i + 1 < len(text):
            next_line = _clean_line(text[i + 1])
            if has_line_break(line, next_line):
                line = merge_line_break(line, next_line)
                text[i + 1] = ""

        if line.strip():
            result.append(line)

    return result
