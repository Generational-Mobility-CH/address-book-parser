from modules.persons_data_processor.src.text_cleaner.dashes_cleaner import (
    DASHES_PATTERNS_AND_REPL,
)
from modules.persons_data_processor.src.text_cleaner.line_breaks_cleaner import (
    has_line_break,
    merge_line_break,
)
from modules.persons_data_processor.src.text_cleaner.parenthesis_cleaner import (
    PARENTHESIS_PATTERNS_AND_REPL,
    remove_unmatched_parenthesis,
)
from modules.persons_data_processor.src.text_cleaner.types.pattern_and_repl_type import (
    PatternAndRepl,
)
from modules.persons_data_processor.src.text_cleaner.unallowed_strings_remover import (
    UNALLOWED_STRINGS_PATTERNS_AND_REPL,
)
from modules.persons_data_processor.src.text_cleaner.whitespace_cleaner import (
    WHITESPACE_PATTERNS_AND_REPL,
)
from modules.persons_data_processor.src.text_cleaner.words_separator import (
    SEPARATE_WORDS_PATTERNS_AND_REPL,
)
from modules.persons_data_processor.src.utility.regex.apply_regex_patterns import (
    apply_regex_patterns,
)

PATTERNS_AND_REPLACEMENTS: list[PatternAndRepl] = []
PATTERNS_AND_REPLACEMENTS.extend(
    UNALLOWED_STRINGS_PATTERNS_AND_REPL
    + PARENTHESIS_PATTERNS_AND_REPL
    + DASHES_PATTERNS_AND_REPL
    + SEPARATE_WORDS_PATTERNS_AND_REPL
    + WHITESPACE_PATTERNS_AND_REPL
)


def _clean_line(line: str) -> str | None:
    line = remove_unmatched_parenthesis(line)
    line = apply_regex_patterns(line, PATTERNS_AND_REPLACEMENTS)

    if not any(char.isalpha() for char in line):
        return None

    return line


def clean_text(text: list[str]) -> list[str]:
    cleaned_text = []
    previous_line = None
    text = list(filter(None, text))

    for line in text:
        if not (line := _clean_line(line)):
            continue

        if previous_line and has_line_break(line, previous_line):
            line = merge_line_break(line, previous_line)
            cleaned_text[-1] = line
            previous_line = None
            continue

        previous_line = line
        cleaned_text.append(line)

    return cleaned_text
