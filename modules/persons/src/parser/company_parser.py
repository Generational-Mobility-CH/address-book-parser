from modules.persons.src.common.special_chars import COMPANY_KEYWORDS
from modules.persons.src.models.person.person_data_parts import PersonDataParts
from modules.persons.src.parser.address_parser import is_address


def is_company(data: PersonDataParts) -> bool:
    for element in data:
        if any(key in element.lower() for key in COMPANY_KEYWORDS):
            return True

        if is_address(element):
            # Bei Firmen: 1. Strassenname, 2. Hausnummer -> bei Personen umgekehrt.
            if not element.strip()[0].isnumeric():
                return True

    return False
