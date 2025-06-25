import logging


from modules.persons.common.special_chars import TAG_NONE_FOUND, PLACEHOLDER_WIDOW
from modules.persons.models.address import Address
from modules.persons.models.person import Person
from modules.persons.src.parser.address_parser import extract_address, is_address


logger = logging.getLogger(__name__)


def extract_widow(content: list[str]) -> Person | None:
    if len(content) not in (2, 3):
        logger.error(f"Could not parse widow: {content}")
        return None

    names = content[0]
    candidates = content[1:]
    address = Address(street_name=TAG_NONE_FOUND, house_number=TAG_NONE_FOUND)
    widow_job = TAG_NONE_FOUND

    for field in candidates:
        if is_address(field.lower()):
            address = extract_address(field)
        else:
            widow_job = field

    return Person(
        original_names=names,
        job=widow_job.strip(),
        address=address,
    )


def is_widow(content: list[str]) -> bool:
    return any(item.lower().__contains__(PLACEHOLDER_WIDOW) for item in content)
