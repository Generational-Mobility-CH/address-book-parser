from libs.regex.src.substitute_with_map import substitute_with_map
from modules.text_parser.src.constants.gender_descriptors import GENDER_FEMALE
from modules.shared.models.panel_data_entry import PanelDataEntry
from modules.text_standardizer.src.constants.job_substitutions import (
    JOBS_SUBSTITUTION_MAP,
)
from modules.text_standardizer.src.constants.name_abbreviations import (
    FIRST_NAME_ABBREVIATIONS_MAP_MALE,
    FIRST_NAME_ABBREVIATIONS_MAP_FEMALE,
)

ABBREVIATED_NAME_PATTERN = r"\b{PLACEHOLDER}"


def standardize_first_names(person: PanelDataEntry) -> PanelDataEntry:
    """
    Info: The person is assumed to be male unless explicitly marked as female, since males are overrepresented in the data.
    In the future, a cleaner implementation would be desirable (i.e. take the variable "GENDER_UNKNOWN" into consideration).
    """
    first_names = person.first_names.lower()

    if "." in first_names:
        map_to_use = (
            FIRST_NAME_ABBREVIATIONS_MAP_FEMALE
            if person.gender == GENDER_FEMALE
            else FIRST_NAME_ABBREVIATIONS_MAP_MALE
        )
        cleaned_first_names = substitute_with_map(
            first_names,
            map_to_use,
            ABBREVIATED_NAME_PATTERN,
        )
        person.first_names = cleaned_first_names

    return person


def standardize_job(person: PanelDataEntry) -> PanelDataEntry:
    job = person.job.lower()

    if "." in job:
        cleaned_job = substitute_with_map(job, JOBS_SUBSTITUTION_MAP, r"{PLACEHOLDER}")
        person.job = cleaned_job

    return person


def standardize_information(persons: list[PanelDataEntry]) -> list[PanelDataEntry]:
    standardized_persons = []

    for p in persons:
        standardized_person = standardize_first_names(p)
        standardized_person = standardize_job(standardized_person)
        # TODO: standardized_person.address.street_name = standardize_street_name(standardized_person.address.street_name)
        standardized_persons.append(standardized_person)

    return standardized_persons
