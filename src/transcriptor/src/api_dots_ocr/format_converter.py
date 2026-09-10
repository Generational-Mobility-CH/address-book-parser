"""
Convert dots.ocr-1.5 P10v output to raw line format
compatible with the text_cleaner/text_parser pipeline.

P10v output:  "1. \u25cf\u2021\u2014 -Weber Richard, Redaktor, 89 Gotthardstr."
Pipeline expects: "\u25cf\u2021\u2014 -Weber Richard, Redaktor, 89 Gotthardstr."

Strips: entry numbering only.
Preserves: \u25cf (postcheck), \u2021 (telephone), \u2014 (em-dash), \u2014 - (partner dash).
"""
import re

# Matches leading entry number like "1. " or "12. "
_NUMBER_PREFIX = re.compile(r"^\d+\.\s*")


def convert_to_raw_lines(text: str) -> str:
    """Convert numbered P10v output to raw text for the pipeline.

    Applied after postprocess_raw(), so character substitutions are
    already normalized (\u25cf/\u2021 are canonical).

    Strips entry numbering only. Preserves \u25cf and \u2021 prefix symbols
    so the parser can extract telephone/postcheck booleans.
    """
    lines = text.splitlines()
    result = []
    for line in lines:
        stripped = line.strip()
        if not stripped:
            continue

        content = _NUMBER_PREFIX.sub("", stripped)
        if content:
            result.append(content)

    return "\n".join(result)


def count_entries(text: str) -> int:
    """Count non-empty entries in converted text."""
    if not text or not text.strip():
        return 0
    return len([line for line in text.splitlines() if line.strip()])
