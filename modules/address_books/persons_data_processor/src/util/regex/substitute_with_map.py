import re
from logging import getLogger

from modules.address_books.persons_data_processor.src.util.regex.build_regex_pattern_from_map import (
    build_regex_pattern_from_map,
)

logger = getLogger(__name__)


def substitute_with_map(
    text: str,
    mapping: dict[str, str],
    pattern_template: str,
    substitution_suffix: str = "",
    replacement_suffix: str = "",
) -> str:
    pattern = build_regex_pattern_from_map(mapping, pattern_template)
    matches = set(pattern.findall(text))

    if matches:
        for match in matches:
            key = match.strip().lower()
            if key in mapping:
                repl = mapping[key]
                text = re.sub(
                    f"{match}{substitution_suffix}",
                    rf"{repl}{replacement_suffix}",
                    text,
                )
            else:
                logger.error(f"Could not find key {key} in mapping {mapping}")

    return text
