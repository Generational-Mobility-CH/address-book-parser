import re


GERMAN_ALPHABET = "a-zA-ZäöüÄÖÜß"

LOWER_CASE_FOLLOWED_BY_UPPER_CASE = re.compile(r"([a-zäöü])([A-ZÄÖÜ])")
DOT_FOLLOWED_BY_LETTER = re.compile(rf"([{GERMAN_ALPHABET}]\.)([{GERMAN_ALPHABET}])")
NO_SPACE_BEFORE_PARENTHESIS = re.compile(rf"([{GERMAN_ALPHABET}^-])(\()")
NO_SPACE_AFTER_PARENTHESIS = re.compile(rf"(\))([{GERMAN_ALPHABET}^-])")

PATTERNS = (
    LOWER_CASE_FOLLOWED_BY_UPPER_CASE,
    DOT_FOLLOWED_BY_LETTER,
    NO_SPACE_BEFORE_PARENTHESIS,
    NO_SPACE_AFTER_PARENTHESIS,
)


def separate_words(text: str) -> str:
    for p in PATTERNS:
        text = re.sub(p, r"\1 \2", text)

    return text
