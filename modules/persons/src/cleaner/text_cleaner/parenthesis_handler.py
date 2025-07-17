import re


def _clean_whitespace_inside_parentheses(line: str) -> str:
    line = line.replace("(- ", "(-")

    return re.sub(r"\(\s*(.*?)\s*\)", r"(\1)", line)


def _remove_empty_parenthesis(line: str) -> str:
    return re.sub(r"\(\s*\)", "", line)


def _remove_unmatched_parenthesis(line: str) -> str:
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


def clean_up_parenthesis(line: str) -> str:
    line = _remove_empty_parenthesis(line)
    line = _remove_unmatched_parenthesis(line)
    line = _clean_whitespace_inside_parentheses(line)

    return line.strip()
