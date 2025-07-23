import re
from logging import getLogger

from modules.persons.src.util.regex.build_regex_pattern_from_map import (
    build_regex_pattern_from_map,
)


logger = getLogger(__name__)


def substitute_with_map(
    text: str,
    mapping: dict[str, str],
    pat_format: str,
    sub_pattern_add: str = "",
    repl_add: str = "",
) -> str:
    pattern = build_regex_pattern_from_map(mapping, pat_format)
    matches = set(pattern.findall(text))

    if matches:
        for match in matches:
            key = match.strip().lower()
            if key in mapping:
                repl = mapping[key]
                text = re.sub(f"{match}{sub_pattern_add}", rf"{repl}{repl_add}", text)
            else:
                logger.error(f"Could not find key {key} in mapping {mapping}")

    return text
