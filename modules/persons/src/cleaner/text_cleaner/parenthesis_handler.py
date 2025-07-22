import re


from modules.persons.src.models.pattern_and_replacement import PatternAndReplacement

REMOVE_EMPTY_PARENTHESIS = re.compile(r"\(\s*\)")
CLEAN_WHITESPACE_INSIDE_PARENTHESIS = re.compile(r"(\()\s*(-?)\s*(.*?)\s*(-?)\s*(\))")

PARENTHESIS_PATTERNS_AND_REPLACEMENT: list[PatternAndReplacement] = [
    PatternAndReplacement(pattern=REMOVE_EMPTY_PARENTHESIS, replacement=""),
    PatternAndReplacement(
        pattern=CLEAN_WHITESPACE_INSIDE_PARENTHESIS, replacement=r"\1\2\3\4\5"
    ),
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
