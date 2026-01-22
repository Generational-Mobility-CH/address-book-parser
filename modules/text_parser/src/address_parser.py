import re

from modules.shared.models.address import Address
from modules.text_parser.src.constants.street_name_keywords import (
    KEYWORDS_STREET_NAME,
)
from modules.text_parser.src.constants.tags import TAG_NONE_FOUND


def is_address(text: str) -> bool:
    return any(char.isdigit() for char in text) or any(
        keyword.lower() in text for keyword in KEYWORDS_STREET_NAME
    )


def extract_address(content: str) -> Address:
    house_number = TAG_NONE_FOUND
    street_name = TAG_NONE_FOUND

    house_number_match = re.search(r"([a-zA-Z]*\d+[a-zA-Z]*)", content)

    if house_number_match:
        house_number = house_number_match.group(1).strip()
        street_name = content.replace(house_number, "").strip()

    return Address(street_name=street_name, house_number=house_number)
