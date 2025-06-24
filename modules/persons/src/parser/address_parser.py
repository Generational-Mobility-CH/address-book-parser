import re

from modules.persons.models.address import Address
from modules.persons.common.special_chars import KEYWORDS_STREET_NAME, TAG_NONE_FOUND


def extract_address(content: str) -> Address:
    house_number = street_name = TAG_NONE_FOUND

    house_number_match = re.search(r"([a-zA-Z]*\d+[a-zA-Z]*)", content)

    if house_number_match:
        house_number = house_number_match.group(1).strip()
        street_name = content.replace(house_number, "").strip() or TAG_NONE_FOUND

    return Address(street_name=street_name, house_number=house_number)


def is_address(text: str) -> bool:
    return any(char.isdigit() for char in text) or any(
        keyword.lower() in text for keyword in KEYWORDS_STREET_NAME
    )
