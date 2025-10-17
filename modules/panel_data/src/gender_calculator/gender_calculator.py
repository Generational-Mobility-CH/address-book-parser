import sqlite3
from pathlib import Path


from modules.panel_data.src.repository.constants.gender_factors_table import (
    GENDER_FACTORS_TABLE_NAME,
)
from modules.panel_data.src.models.gender import Gender
from modules.panel_data.src.models.new_person import NewPerson


def _add_gender_factor(
    db_path: Path, person_key: str, factor_name: str, gender: Gender
) -> None:
    with sqlite3.connect(db_path) as conn:
        conn.execute(
            f"""
            INSERT INTO {GENDER_FACTORS_TABLE_NAME} (person_key, factor_name, gender_from_factor)
            VALUES (?, ?, ?)
            """,
            (person_key, factor_name, gender.value),
        )


def found_female_keyword(data: str) -> bool:
    return data.startswith(
        "wwe. "
    )  # TODO: check if abbreviation is already normalized? Ww. wwe.??


def found_female_first_name(data: str) -> bool:
    return data.endswith("a")


def found_female_job(data: str) -> bool:
    return data.endswith("in")


def identify_females(
    persons_collection: list[NewPerson], db_path: Path
) -> list[NewPerson]:
    for person in persons_collection:
        first_names = person.first_names.lower().strip()
        person_key = (
            f"TODO-{person.first_names}-{person.last_names}-{person.street_name}"
        )

        if found_female_keyword(first_names):
            person.gender = Gender.FEMALE
            _add_gender_factor(db_path, person_key, "keyword", Gender.FEMALE)

        if found_female_first_name(first_names):
            person.gender = Gender.FEMALE
            _add_gender_factor(db_path, person_key, "first_name", Gender.FEMALE)

        if found_female_job(person.job):
            person.gender = Gender.FEMALE
            _add_gender_factor(db_path, person_key, "job", Gender.FEMALE)

    return persons_collection
