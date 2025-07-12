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
