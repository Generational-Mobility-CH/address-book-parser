GERMAN_UMLAUTS_MAP = {"ä": "ae", "ö": "oe", "ü": "ue"}


def _contains_umlauts(input_string: str) -> bool:
    return any(char in GERMAN_UMLAUTS_MAP for char in input_string.lower())


def _replace_umlauts(text: str) -> str:
    return "".join(GERMAN_UMLAUTS_MAP.get(char, char) for char in text.lower()).title()


def prepare_str_for_comparison(text: str) -> str:
    text = text.strip()
    text = _replace_umlauts(text) if _contains_umlauts(text) else text
    text = text.lower()

    return text
