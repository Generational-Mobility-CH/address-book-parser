from modules.panel_data.src.models.panel_data_entry import PanelDataEntry


def separate_partner_last_name(persons: list[PanelDataEntry]) -> list[PanelDataEntry]:
    for person in persons:
        if "-" in person.last_names:  # TODO: make better
            splitted = person.last_names.split(r"[-\s]+", 1)
            if len(splitted) > 1:
                person.last_names, person.partner_last_names = splitted[0], splitted[1]

    return persons
