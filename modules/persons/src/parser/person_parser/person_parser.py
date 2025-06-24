from modules.persons.common.special_chars import TAG_NONE_FOUND
from modules.persons.models.address import Address
from modules.persons.models.person import Person
from modules.persons.src.parser.address_parser import is_address, extract_address
from modules.persons.src.parser.person_parser.names_parser import is_name


def extract_person_information(
    content: list[str], current_surname: str
) -> Person | None:
    remaining_content = content
    names = TAG_NONE_FOUND
    address = Address(street_name=TAG_NONE_FOUND, house_number=TAG_NONE_FOUND)

    for e in content:
        if is_name(e, current_surname):
            names = e
        elif is_address(e):
            address = extract_address(e)
        else:
            continue
        remaining_content.remove(e)

    remaining_content = list(filter(lambda x: x != "", remaining_content))

    if len(remaining_content) == 1:
        job = remaining_content[0].strip()
    else:
        return None

    return Person(original_names=names, address=address, job=job)
