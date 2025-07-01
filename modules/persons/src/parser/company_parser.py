from modules.persons.src.models.person.person_data_parts import PersonDataParts
from modules.persons.src.parser.address_parser import is_address


def is_company(data: PersonDataParts) -> bool:
    for element in data:
        if is_address(element):
            # Bei Firmen: 1. Strassenname, 2. Hausnummer -> bei Personen umgekehrt.
            if not element.strip()[0].isnumeric():
                return True
    return False
