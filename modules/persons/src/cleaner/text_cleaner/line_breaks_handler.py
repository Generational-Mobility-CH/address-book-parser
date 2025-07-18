import re


ENDS_WITH_DASH_OR_DIGIT = re.compile(r"[-\d]$")
STARTS_WITH_DIGIT = re.compile(r"^\s*\d")


def has_line_break(line: str, next_line: str) -> bool:
    return (
        bool(line) and ENDS_WITH_DASH_OR_DIGIT.search(line)
    ) or STARTS_WITH_DIGIT.match(next_line)


def merge_line_break(current_line: str, next_line: str) -> str:
    if next_line.lower().startswith("und"):
        next_line = " und" + next_line[3:]

    line = current_line + " " + next_line

    return line.replace("- ", "")
