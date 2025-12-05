from modules.panel_data.src.constants.gender_descriptors import GENDER_FEMALE
from modules.panel_data.src.models.panel_data_entry import PanelDataEntry
from modules.panel_data.src.separator.last_and_first_names_separator import (
    separate_last_and_first_names,
)
from modules.panel_data.src.separator.partner_last_name_separator import (
    separate_partner_last_name,
)
from modules.address_books.src.models.address_book.address_book_entry import (
    AddressBookEntry,
)


def separate_information(persons: list[AddressBookEntry]) -> list[PanelDataEntry]:
    persons = separate_last_and_first_names(persons)
    persons = separate_partner_last_name(persons)

    return persons


def separate_partner(persons: list[PanelDataEntry]) -> list[PanelDataEntry]:
    result = persons.copy()

    for p in persons:
        if p.partner_last_names != "":
            partner = PanelDataEntry(
                first_names="N/A",
                last_names=p.partner_last_names,
                partner_last_names=p.last_names,
                street_name=p.address.street_name,
                house_number=p.address.house_number,
                original_entry=p.original_names,
                job="N/A",
                year=p.year,
                pdf_page_number=p.pdf_page_number,
                gender=GENDER_FEMALE,
            )
            result.append(partner)

    return result
