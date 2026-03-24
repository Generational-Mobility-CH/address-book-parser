from src.shared.models.panel_data_entry import PanelDataEntry
from src.text_parser.src.separator.last_and_first_names_separator import (
    separate_last_and_first_names,
)
from src.text_parser.src.separator.partner_last_name_separator import (
    separate_partner_last_name,
)
from src.text_parser.src.separator.partner_separator import separate_partner


def separate_information(persons: list[PanelDataEntry]) -> list[PanelDataEntry]:
    persons = separate_last_and_first_names(persons)
    persons = separate_partner_last_name(persons)
    persons = separate_partner(persons)

    return persons
