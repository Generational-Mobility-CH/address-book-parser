import re

from modules.persons.src.cleaner.text_cleaner.types.pattern_and_repl_type import (
    PatternAndRepl,
)


REMOVE_EMPTY_PARENTHESIS_PATTERN = re.compile(r"\(\s*\)")
CLEAN_WHITESPACE_INSIDE_PARENTHESIS_PATTERN = re.compile(
    r"(\()\s*(-?)\s*(.*?)\s*(-?)\s*(\))"
)

PARENTHESIS_PATTERNS_AND_REPL: list[PatternAndRepl] = [
    (REMOVE_EMPTY_PARENTHESIS_PATTERN, ""),
    (CLEAN_WHITESPACE_INSIDE_PARENTHESIS_PATTERN, r"\1\2\3\4\5"),
]


def remove_unmatched_parenthesis(text: str) -> str:
    unmatched_parenthesis_positions = set()

    for index, char in enumerate(text):
        if char == "(":
            unmatched_parenthesis_positions.add(index)
        elif char == ")":
            if unmatched_parenthesis_positions:
                for i in unmatched_parenthesis_positions:
                    if text[i] == "(":
                        unmatched_parenthesis_positions.pop()
                        break
            else:
                unmatched_parenthesis_positions.add(index)

    if unmatched_parenthesis_positions:
        text = "".join(
            char
            for index, char in enumerate(text)
            if index not in unmatched_parenthesis_positions
        )

    return text
