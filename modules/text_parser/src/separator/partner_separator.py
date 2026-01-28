from modules.shared.constants.tags import TAG_NONE_FOUND, TAG_NO_JOB
from modules.shared.models.panel_data_entry import PanelDataEntry
from modules.text_parser.src.constants.gender_descriptors import GENDER_UNKNOWN


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
                original_entry=p.original_entry,
                job=TAG_NO_JOB,
                year=p.year,
                pdf_page_number=p.pdf_page_number,
                gender=GENDER_UNKNOWN,
            )
            result.append(partner)

    return result
