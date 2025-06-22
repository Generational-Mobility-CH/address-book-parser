from modules.common.special_chars import TAG_ANOMALY
from modules.models.raw_person import RawPerson
from modules.persons_parser.src.parser.address_parser import extract_address, is_address
from modules.persons_parser.src.parser.person_parser.names_parser import is_name


def extract_person_information(
    content: list[str], current_surname: str
) -> RawPerson | None:
    remaining_content = content
    names = address = TAG_ANOMALY

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

    return RawPerson(names=names, address=address, job=job)
