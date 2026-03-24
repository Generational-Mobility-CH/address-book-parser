import re
from re import Pattern


def build_regex_pattern_from_map(
    mapping: dict[str, str], pattern_template: str, flags: int = re.IGNORECASE
) -> Pattern:
    pattern = "|".join(
        pattern_template.format(PLACEHOLDER=rf"{k}")
        for k in sorted(mapping, key=len, reverse=True)
    )

    return re.compile(pattern, flags=flags)
