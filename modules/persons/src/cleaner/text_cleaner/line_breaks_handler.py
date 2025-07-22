import re


ENDS_WITH_DASH_OR_DIGIT = re.compile(r"[-\d]$")
STARTS_WITH_DIGIT = re.compile(r"^\s*\d")


def has_line_break(line: str, previous_line: str) -> bool:
    return bool(line) and (
        ENDS_WITH_DASH_OR_DIGIT.search(previous_line) or STARTS_WITH_DIGIT.match(line)
    )


def merge_line_break(line: str, previous_line: str) -> str:
    if line.lower().startswith("und"):
        line = " und" + line[3:]

    line = previous_line + " " + line

    return line.replace("- ", "")
