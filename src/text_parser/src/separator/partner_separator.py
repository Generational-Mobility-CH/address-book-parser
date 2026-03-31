from src.shared.constants.tags import TAG_NONE_FOUND, TAG_PARTNER_ATTRIBUTE
from src.shared.models.panel_data_entry import PanelDataEntry
from src.text_parser.src.constants.gender_descriptors import GENDER_UNKNOWN


def separate_partner(persons: list[PanelDataEntry]) -> list[PanelDataEntry]:
    result = persons.copy()

    for p in persons:
        if p.partner_last_names != "" and p.partner_last_names != TAG_NONE_FOUND:
            partner = PanelDataEntry(
                first_names=TAG_PARTNER_ATTRIBUTE,
                last_names=p.partner_last_names,
                partner_last_names=p.last_names,
                address=p.address,
                original_entry=p.original_entry,
                job=TAG_PARTNER_ATTRIBUTE,
                year=p.year,
                pdf_page_number=p.pdf_page_number,
                gender=GENDER_UNKNOWN,
            )
            result.append(partner)

    return result
