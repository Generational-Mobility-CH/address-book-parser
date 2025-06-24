from modules.persons.src.parser.address_parser import is_address


def is_company(line: list[str]) -> bool:
    for element in line:
        if is_address(element):
            # Bei Firmen: 1. Strassenname, 2. Hausnummer - bei Personen umgekehrt.
            if not element.strip()[0].isnumeric():
                return True
    return False
