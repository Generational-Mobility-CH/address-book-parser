from modules.shared.models.person_data_parts import (
    PersonDataParts,
)
from modules.text_parser.src.address_parser import (
    is_address,
)
from modules.text_parser.src.constants.company_keywords import COMPANY_KEYWORDS


def is_company(data: PersonDataParts) -> bool:
    for element in data:
        element = element.lower().strip()

        if any(keyword in element for keyword in COMPANY_KEYWORDS):
            return True

        if is_address(element) and not element[0].isnumeric():
            # Info: In the address books when the street name precedes the house number it's a company entry (instead of a person).
            return True

    return False
