"""
Extract prefix symbols and title prefixes from address book entry lines.

Entry symbols (●/‡) encode categorical data:
- ● = postcheck account holder
- ‡ = telephone subscriber

Title prefixes (Dr., Wwe., Frau, etc.) are extracted from first_names
after name separation so they can be stored in a separate field.
"""
import re

# Matches ● and/or ‡ at line start, with optional trailing whitespace
_SYMBOL_PREFIX = re.compile(r"^([●‡]+)\s*")

_TITLE_KEYWORDS = {
    "dr.", "dr", "wwe.", "wwe", "ww.", "frau", "frl.", "prof.", "gent.", "wittwe",
}

_DR_SPECIALIZATIONS = {
    "med.", "phil.", "jur.", "theol.", "rer.", "ing.", "sc.",
}


def extract_entry_symbols(line: str) -> tuple[bool, bool, str]:
    """Extract ● and ‡ from line start.

    Returns (telephone, postcheck, cleaned_line).
    """
    m = _SYMBOL_PREFIX.match(line)
    if not m:
        return False, False, line
    symbols = m.group(1)
    return "\u2021" in symbols, "\u25cf" in symbols, line[m.end():]


def extract_title_prefix(first_names: str) -> tuple[str, str]:
    """Extract title prefix (Dr., Wwe., Frau, etc.) from first_names.

    Returns (prefix, cleaned_first_names).
    """
    parts = first_names.split()
    if not parts:
        return "", first_names

    first_lower = parts[0].lower().rstrip(".")
    keyword_match = any(k.rstrip(".") == first_lower for k in _TITLE_KEYWORDS)

    if not keyword_match:
        return "", first_names

    prefix = parts[0]
    rest_start = 1

    if first_lower.startswith("dr") and len(parts) > 1:
        spec_lower = parts[1].lower().rstrip(".")
        if any(s.rstrip(".") == spec_lower for s in _DR_SPECIALIZATIONS):
            prefix = f"{parts[0]} {parts[1]}"
            rest_start = 2

    return prefix, " ".join(parts[rest_start:])
