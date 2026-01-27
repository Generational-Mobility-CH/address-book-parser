import re

from modules.shared.constants.tags import TAG_NONE_FOUND
from modules.shared.models.panel_data_entry import PanelDataEntry


def separate_partner_last_name(persons: list[PanelDataEntry]) -> list[PanelDataEntry]:
    for person in persons:
        if person.last_names.lower() == TAG_NONE_FOUND.lower():
            continue

        separator = None

        if "(" in person.last_names:
            separator = "("
        if "-" in person.last_names:
            separator = "-"
        elif " " in person.last_names:
            separator = " "

        splitted = person.last_names.split(separator, 1)

        if len(splitted) > 1:
            own_last_names = re.sub(r"[-()]", "", splitted[0])
            partner_last_names = re.sub(r"[-()]", "", splitted[1])
            person.last_names, person.partner_last_names = (
                own_last_names,
                partner_last_names,
            )

    return persons
