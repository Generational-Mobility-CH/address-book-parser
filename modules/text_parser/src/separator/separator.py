from modules.shared.models.address_book.address_book_entry import AddressBookEntry
from modules.shared.models.panel_data_entry import PanelDataEntry
from modules.text_parser.src.constants.gender_descriptors import GENDER_UNKNOWN
from modules.shared.constants.tags import TAG_NO_JOB, TAG_NONE_FOUND
from modules.text_parser.src.separator.last_and_first_names_separator import (
    separate_last_and_first_names,
)
from modules.text_parser.src.separator.partner_last_name_separator import (
    separate_partner_last_name,
)


def separate_information(persons: list[AddressBookEntry]) -> list[PanelDataEntry]:
    persons = separate_last_and_first_names(persons)
    persons = separate_partner_last_name(persons)
    persons = separate_partner(persons)

    return persons


def separate_partner(persons: list[PanelDataEntry]) -> list[PanelDataEntry]:
    result = persons.copy()

    for p in persons:
        if p.partner_last_names != "":
            partner = PanelDataEntry(
                first_names=TAG_NONE_FOUND,
                last_names=p.partner_last_names,
                partner_last_names=p.last_names,
                street_name=p.address.street_name,
                house_number=p.address.house_number,
                original_entry=p.original_names,
                job=TAG_NO_JOB,
                year=p.year,
                pdf_page_number=p.pdf_page_number,
                gender=GENDER_UNKNOWN,
            )
            result.append(partner)

    return result
