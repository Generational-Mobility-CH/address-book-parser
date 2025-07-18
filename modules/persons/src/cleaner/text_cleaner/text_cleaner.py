from modules.persons.src.cleaner.text_cleaner.dashes_handler import (
    DASHES_PATTERNS_AND_REPLACEMENT,
)
from modules.persons.src.cleaner.text_cleaner.line_breaks_handler import (
    has_line_break,
    merge_line_break,
)
from modules.persons.src.cleaner.text_cleaner.parenthesis_handler import (
    PARENTHESIS_PATTERNS_AND_REPLACEMENT,
    remove_unmatched_parenthesis,
)
from modules.persons.src.cleaner.text_cleaner.unallowed_strings_remover import (
    UNALLOWED_STRINGS_PATTERNS_AND_REPLACEMENT,
)
from modules.persons.src.cleaner.text_cleaner.words_separator import (
    SEPARATE_WORDS_PATTERNS_AND_REPLACEMENT,
)
from modules.persons.src.models.pattern_and_replacement import PatternAndReplacement
from modules.persons.src.util.apply_regex_patterns import apply_regex_patterns


PATTERNS_AND_REPLACEMENTS: list[PatternAndReplacement] = []
PATTERNS_AND_REPLACEMENTS.extend(
    UNALLOWED_STRINGS_PATTERNS_AND_REPLACEMENT
    + PARENTHESIS_PATTERNS_AND_REPLACEMENT
    + DASHES_PATTERNS_AND_REPLACEMENT
    + SEPARATE_WORDS_PATTERNS_AND_REPLACEMENT
)


def _clean_line(text: str) -> str:
    text = remove_unmatched_parenthesis(text)
    text = apply_regex_patterns(text, PATTERNS_AND_REPLACEMENTS)
    text = " ".join(text.split()).strip()

    if not any(char.isalpha() for char in text):
        return ""

    return text


def clean_text(text: list[str]) -> list[str]:
    result = []
    text = list(filter(None, text))

    for i, line in enumerate(text):
        line = _clean_line(line)

        if i + 1 < len(text):
            next_line = _clean_line(text[i + 1])
            if has_line_break(line, next_line):
                line = merge_line_break(line, next_line)
                text[i + 1] = ""

        if line := line.strip():
            result.append(line)

    return result
