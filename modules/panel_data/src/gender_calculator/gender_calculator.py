import re
import sqlite3
from pathlib import Path

import pandas as pd

from modules.panel_data.src.constants.table_definitions.gender_factors_table import (
    GENDER_FACTORS_TABLE_NAME,
)
from modules.panel_data.src.constants.table_definitions.panel_data_table import (
    PANEL_DATA_TABLE_NAME,
)
from modules.panel_data.src.models.new_person import NewPerson

WIDOW_PATTERN = re.compile(r"\b(?:wwe\.|ww\.|wwe|wittwe)\b\.?\s?", re.IGNORECASE)
WIDOWER_PATTERN = re.compile(r"\(-|[()]", re.IGNORECASE)


def identify_widow_and_widower(
    persons_collection: list[NewPerson], db_path: Path
) -> list[NewPerson]:
    with sqlite3.connect(db_path) as conn:
        gender_factors_to_insert = []

        for person in persons_collection:
            person_key = (
                f"{person.year}-{person.pdf_page_number}-TODO_add_row_nr_to_key"
            )

            if re.search(WIDOW_PATTERN, person.first_names):
                person.first_names = re.sub(WIDOW_PATTERN, "", person.first_names)
                gender_factors_to_insert.append((person_key, "widow", "F"))
            elif re.search(WIDOWER_PATTERN, person.partner_last_names):
                person.partner_last_names = re.sub(
                    WIDOWER_PATTERN, "", person.partner_last_names
                )
                gender_factors_to_insert.append((person_key, "widower", "M"))

        conn.executemany(
            f"""
            INSERT INTO {GENDER_FACTORS_TABLE_NAME} (address_book_entry_key, factor_name, gender_from_factor)
            VALUES (?, ?, ?)
        """,
            gender_factors_to_insert,
        )

    return persons_collection


def calculate_gender(gender_factors: list) -> tuple[str, float]:
    # TODO: implement gender factors calculation
    return "TODO", 1.0


def calculate_gender_factors(
    persons_collection: list[NewPerson], db_path: Path
) -> list[NewPerson]:
    updated_persons = []

    with sqlite3.connect(db_path) as conn:
        query = f"SELECT * FROM {GENDER_FACTORS_TABLE_NAME}"
        table_data = pd.read_sql_query(query, conn)
        all_gender_factors = table_data.to_dict(orient="records")

        for person in persons_collection:
            person_key = (
                f"{person.year}-{person.pdf_page_number}-TODO_add_row_nr_to_key"
            )

            found_persons_gender_factors = [
                factor
                for factor in all_gender_factors
                if factor.get("key") == person_key
            ]
            person.gender, person.gender_confidence = calculate_gender(
                found_persons_gender_factors
            )

            updated_persons.append(person)

        conn.executemany(
            f"""
                    INSERT INTO {PANEL_DATA_TABLE_NAME} (first_names, last_names, partner_last_names, gender, gender_confidence, street_name, house_number, job, year, pdf_page_number, original_names)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
            updated_persons,
        )

        return updated_persons


def infer_gender(persons: list[NewPerson], db_path: Path) -> list[NewPerson]:
    persons = identify_widow_and_widower(persons, db_path)
    persons = calculate_gender_factors(persons, db_path)

    return persons
