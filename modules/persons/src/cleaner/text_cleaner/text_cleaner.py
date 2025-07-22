from modules.persons.src.cleaner.text_cleaner.dashes_cleaner import (
    DASHES_PATTERNS_AND_REPL,
)
from modules.persons.src.cleaner.text_cleaner.line_breaks_cleaner import (
    has_line_break,
    merge_line_break,
)
from modules.persons.src.cleaner.text_cleaner.parenthesis_cleaner import (
    PARENTHESIS_PATTERNS_AND_REPL,
    remove_unmatched_parenthesis,
)
from modules.persons.src.cleaner.text_cleaner.types.pattern_and_repl_type import (
    PatternAndRepl,
)
from modules.persons.src.cleaner.text_cleaner.unallowed_strings_remover import (
    UNALLOWED_STRINGS_PATTERNS_AND_REPL,
)
from modules.persons.src.cleaner.text_cleaner.whitespace_cleaner import (
    WHITESPACE_PATTERNS_AND_REPL,
)
from modules.persons.src.cleaner.text_cleaner.words_separator import (
    SEPARATE_WORDS_PATTERNS_AND_REPL,
)
from modules.persons.src.util.apply_regex_patterns import apply_regex_patterns


PATTERNS_AND_REPLACEMENTS: list[PatternAndRepl] = []
PATTERNS_AND_REPLACEMENTS.extend(
    UNALLOWED_STRINGS_PATTERNS_AND_REPL
    + PARENTHESIS_PATTERNS_AND_REPL
    + DASHES_PATTERNS_AND_REPL
    + SEPARATE_WORDS_PATTERNS_AND_REPL
    + WHITESPACE_PATTERNS_AND_REPL
)


def _clean_line(text: str) -> str | None:
    text = remove_unmatched_parenthesis(text)
    text = apply_regex_patterns(text, PATTERNS_AND_REPLACEMENTS)

    if not any(char.isalpha() for char in text):
        return None

    return text


def clean_text(text: list[str]) -> list[str]:
    cleaned_text = []
    previous_line = None
    text = list(filter(None, text))

    for line in text:
        if not (line := _clean_line(line).strip()):
            continue

        if previous_line and has_line_break(line, previous_line):
            line = merge_line_break(line, previous_line)
            cleaned_text[-1] = line
            previous_line = None
            continue

        previous_line = line
        cleaned_text.append(line)

    return cleaned_text
