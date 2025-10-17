import sqlite3
from pathlib import Path

from modules.panel_data.src.gender_calculator.constants.female_names_not_ending_in_a import (
    FEMALE_NAMES_NOT_ENDING_IN_A,
)
from modules.panel_data.src.gender_calculator.constants.male_names_ending_in_a import (
    MALE_NAMES_ENDING_IN_A,
)
from modules.panel_data.src.repository.constants.gender_factors_table import (
    GENDER_FACTORS_TABLE_NAME,
)
from modules.panel_data.src.models.gender import Gender
from modules.panel_data.src.models.panel_data_entry import PanelDataEntry


def _add_gender_factor(
    db_path: Path, person_key: str, factor_name: str, gender: Gender
) -> None:
    with sqlite3.connect(db_path) as conn:
        gender_value = gender.value
        conn.execute(
            f"""
            INSERT INTO {GENDER_FACTORS_TABLE_NAME} (person_key, factor_name, gender_from_factor)
            VALUES (?, ?, ?)
            """,
            (person_key, factor_name, gender_value),
        )


def found_female_keyword(data: str) -> bool:
    data = data.lower().strip()

    return data.startswith(
        "wwe. "
    )  # TODO: check if abbreviation is already normalized? Ww. wwe.??


def found_female_first_name(data: str) -> bool:
    # TODO: make name checking case insensitive -> make names in list lower case
    data = data.strip()

    return (
        data.endswith("a") and data not in MALE_NAMES_ENDING_IN_A
    ) or data in FEMALE_NAMES_NOT_ENDING_IN_A


def found_female_job(data: str) -> bool:
    return data.strip().endswith("in")


def identify_females(
    persons_collection: list[PanelDataEntry], db_path: Path
) -> list[PanelDataEntry]:
    for person in persons_collection:
        person_key = f"TODO-{person.first_names}-{person.last_names}-{person.address.street_name}"

        if found_female_keyword(person.first_names):
            person.gender = Gender.FEMALE
            _add_gender_factor(db_path, person_key, "keyword", Gender.FEMALE)

        elif found_female_first_name(person.first_names):
            person.gender = Gender.FEMALE
            _add_gender_factor(db_path, person_key, "first_name", Gender.FEMALE)

        elif found_female_job(person.job):
            person.gender = Gender.FEMALE
            _add_gender_factor(db_path, person_key, "job", Gender.FEMALE)

    return persons_collection
