import logging


from modules.common.special_chars import TAG_NONE_FOUND, PLACEHOLDER_WIDOW
from modules.models.raw_person import RawPerson
from modules.persons_parser.src.parser.address_parser import extract_address, is_address

logger = logging.getLogger(__name__)


def extract_widow(content: list[str]) -> RawPerson | None:
    if len(content) not in (2, 3):
        logger.error(f"Could not parse widow: {content}")
        return None

    names = content[0]
    candidates = content[1:]
    widow_address = TAG_NONE_FOUND
    widow_job = TAG_NONE_FOUND

    for field in candidates:
        if is_address(field.lower()):
            widow_address = extract_address(field)
        else:
            widow_job = field

    return RawPerson(
        names=names,
        job=widow_job.strip(),
        address=widow_address,
    )


def is_widow(content: list[str]) -> bool:
    return any(item.lower().__contains__(PLACEHOLDER_WIDOW) for item in content)
