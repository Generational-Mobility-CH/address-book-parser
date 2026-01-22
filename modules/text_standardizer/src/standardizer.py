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


def standardize_first_names(persons: list[PanelDataEntry]) -> list[PanelDataEntry]:
    for entry in persons:
        first_names = entry.first_names.lower()
        if "." in first_names:
            if entry.gender == GENDER_FEMALE:
                cleaned_first_names = substitute_with_map(
                    first_names,
                    FIRST_NAME_ABBREVIATIONS_MAP_FEMALE,
                    ABBREVIATED_NAME_PATTERN,
                )
            else:
                cleaned_first_names = substitute_with_map(
                    first_names,
                    FIRST_NAME_ABBREVIATIONS_MAP_MALE,
                    ABBREVIATED_NAME_PATTERN,
                )
            entry.first_names = cleaned_first_names.title()

    return persons


def standardize_job(persons: list[PanelDataEntry]) -> list[PanelDataEntry]:
    for entry in persons:
        job = entry.job.lower()
        if "." in job:
            cleaned_job = substitute_with_map(
                job, JOBS_SUBSTITUTION_MAP, r"{PLACEHOLDER}"
            )
            entry.job = cleaned_job.title()
    return persons


def standardize_information(persons: list[PanelDataEntry]) -> list[PanelDataEntry]:
    persons = standardize_first_names(persons)
    persons = standardize_job(persons)

    return persons
