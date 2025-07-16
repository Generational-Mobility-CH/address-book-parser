from modules.persons.src.models.person.person_data_parts import PersonDataParts
from modules.persons.src.parser.address_parser import is_address
from modules.persons.src.parser.constants.company_keywords import COMPANY_KEYWORDS


def is_company(data: PersonDataParts) -> bool:
    for element in data:
        element = element.lower().strip()

        if any(keyword in element for keyword in COMPANY_KEYWORDS):
            return True

        if is_address(element) and not element[0].isnumeric():
            # Info: For persons, house number precedes street; for firms, it's reversed.
            return True

    return False
