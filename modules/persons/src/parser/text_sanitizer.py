import re

from modules.persons.src.common.special_chars import (
    ALLOWED_SPECIAL_CHARS,
    UNALLOWED_STRINGS,
    UNALLOWED_AT_START_OF_STRING,
)


def clean_text_lines(text: list[str]) -> list[str]:
    result = []

    for i, line in enumerate(text):
        line = sanitize_line(line)

        if i + 1 < len(text):
            next_line = sanitize_line(text[i + 1])
            if has_line_break(line, next_line):
                line = merge_line_break(line, next_line)
                text[i + 1] = ""

        if line.strip():
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
    line = clean_up_white_space(line)
    line = remove_unallowed_strings(line)
    line = clean_up_parenthesis(line)
    line = clean_up_dashes(line)
    line = clean_up_white_space(line)

    if not any(
        char.isalpha() for char in line
    ):  # TODO: check whats better isalpha() or isalnum()
        return ""

    return line


def clean_up_white_space(line: str) -> str:
    return " ".join(line.strip().split())


def remove_unallowed_strings(line: str) -> str:
    for prefix in UNALLOWED_AT_START_OF_STRING:
        if line.startswith(prefix):
            line = line[len(prefix) :]

    line = remove_partial_matches(line)

    line = "".join(
        char for char in line if char in ALLOWED_SPECIAL_CHARS or char.isalnum()
    )

    return line


def remove_partial_matches(line: str) -> str:
    for keyword in UNALLOWED_STRINGS:
        line = line.replace(keyword, "")

    return line.strip()


def clean_up_parenthesis(line: str) -> str:
    line = remove_empty_parenthesis(line)
    line = remove_unmatched_parenthesis(line)
    line = clean_whitespace_inside_parentheses(line)

    return line.strip()


def clean_whitespace_inside_parentheses(line: str) -> str:
    line = line.replace("(- ", "(-")

    return re.sub(r"\(\s*(.*?)\s*\)", r"(\1)", line)


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


def clean_up_dashes(line: str) -> str:
    line = line.replace("—", "-")
    line = line.replace(" - ", "-")
    line = line.replace("- ", "-")
    line = line.replace(" -", "-")

    result = ""
    previous_was_dash = False

    for char in line:
        if char == "-":
            if not previous_was_dash:
                result += "-"
                previous_was_dash = True
            # else: skip repeated dash
        else:
            result += char
            previous_was_dash = False

    return result
