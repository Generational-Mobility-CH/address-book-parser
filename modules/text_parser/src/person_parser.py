from modules.shared.models.address import Address
from modules.shared.models.panel_data_entry import PanelDataEntry

from modules.shared.models.person_data_parts import (
    PersonDataParts,
)
from modules.text_cleaner.src.address_cleaner import clean_address
from modules.text_parser.src.address_parser import (
    is_address,
    extract_address,
)
from modules.text_parser.src.constants.gender_descriptors import GENDER_UNKNOWN
from modules.text_parser.src.constants.last_name_placeholders import (
    LAST_NAME_PLACEHOLDERS,
)
from modules.shared.constants.tags import TAG_NONE_FOUND, TAG_NO_JOB


def _is_name(text: str, last_name: str) -> bool:
    return last_name in text or any(
        placeholder in text for placeholder in LAST_NAME_PLACEHOLDERS
    )


def parse_person(data: PersonDataParts, current_last_name: str) -> PanelDataEntry:
    person: PanelDataEntry = PanelDataEntry(
        original_names=TAG_NONE_FOUND,
        first_names=TAG_NONE_FOUND,
        last_names=TAG_NONE_FOUND,
        partner_last_names=TAG_NONE_FOUND,
        address=Address(
            street_name=TAG_NONE_FOUND, house_number=TAG_NONE_FOUND, coordinates=None
        ),
        job=TAG_NO_JOB,
        gender=GENDER_UNKNOWN,
        gender_confidence="",
        original_entry=f"{data.first}, {data.second}, {data.third}",
        year=0,
        pdf_page_number=0,
    )

    if (all_names := data.first) and _is_name(all_names, current_last_name):
        person.original_names = all_names

    if len(data) == 2:
        is_address(data.second) and setattr(
            person, "address", extract_address(data.second)
        )
    elif len(data) == 3:
        is_address(data.third) and setattr(
            person, "address", extract_address(data.third)
        )
        person.job = data.second

    person.address = clean_address(person.address)

    return person
