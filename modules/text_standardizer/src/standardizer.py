from modules.shared.models.panel_data_entry import PanelDataEntry
from modules.text_standardizer.src.first_names_standardizer import (
    standardize_first_names,
)
from modules.text_standardizer.src.job_standardizer import standardize_job
from modules.text_standardizer.src.street_name_standardizer import (
    standardize_street_name,
)


def standardize_information(persons: list[PanelDataEntry]) -> list[PanelDataEntry]:
    standardized_persons = []

    for p in persons:
        standardized_person = standardize_first_names(p)
        standardized_person = standardize_job(standardized_person)
        standardized_person.address.street_name = standardize_street_name(
            standardized_person.address.street_name
        )
        standardized_persons.append(standardized_person)

    return standardized_persons
