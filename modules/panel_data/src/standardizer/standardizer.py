from modules.panel_data.src.models.panel_data_entry import PanelDataEntry


def standardize_first_names(persons: list[PanelDataEntry]) -> list[PanelDataEntry]:
    # TODO
    return persons


def standardize_job(persons: list[PanelDataEntry]) -> list[PanelDataEntry]:
    # TODO
    return persons


def standardize_information(persons: list[PanelDataEntry]) -> list[PanelDataEntry]:
    persons = standardize_first_names(persons)
    persons = standardize_job(persons)

    return persons
