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
