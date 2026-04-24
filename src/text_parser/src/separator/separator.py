from src.shared.models.panel_data_entry import PanelDataEntry
from src.text_parser.src.prefix_extractor import extract_title_prefix
from src.text_parser.src.separator.last_and_first_names_separator import (
    separate_last_and_first_names,
)
from src.text_parser.src.separator.partner_last_name_separator import (
    separate_partner_last_name,
)
from src.text_parser.src.separator.partner_separator import separate_partner


def _extract_title_prefixes(
    persons: list[PanelDataEntry],
) -> list[PanelDataEntry]:
    for person in persons:
        pfx, cleaned = extract_title_prefix(person.first_names)
        if pfx:
            person.pfx = pfx
            person.first_names = cleaned
    return persons


def separate_information(persons: list[PanelDataEntry]) -> list[PanelDataEntry]:
    persons = separate_last_and_first_names(persons)
    persons = _extract_title_prefixes(persons)
    persons = separate_partner_last_name(persons)
    persons = separate_partner(persons)

    return persons
