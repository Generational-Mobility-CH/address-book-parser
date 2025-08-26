import re
import sqlite3
from pathlib import Path

import pandas as pd
from pandas import DataFrame

from modules.panel_data.src.constants.table_definitions.gender_factors_table import (
    GENDER_FACTORS_TABLE_NAME,
)
from modules.panel_data.src.constants.table_definitions.panel_data_table import (
    PANEL_DATA_TABLE_NAME,
)
from modules.panel_data.src.names_handler.first_names_cleaner import clean_first_names
from modules.panel_data.src.names_handler.last_and_first_names_separator import (
    separate_names_legacy,
)
from modules.panel_data.src.names_handler.last_names_separator import (
    separate_last_names,
)

WIDOW_PATTERN = re.compile(r"\b(?:wwe\.|ww\.|wwe|wittwe)\b\.?\s?", re.IGNORECASE)
WIDOWER_PATTERN = re.compile(r"\(-|[()]", re.IGNORECASE)


def separate_last_and_first_names(df: DataFrame) -> DataFrame:
    for index, og_name in enumerate(df["original_names"]):
        separated_names = separate_names_legacy(og_name)
        cleaned_names = clean_first_names(separated_names)

        df.at[index, "first_names"] = cleaned_names.first_names
        df.at[index, "last_names"] = cleaned_names.last_names

    return df


def identify_widow_and_widower(df: DataFrame, db_path: Path) -> DataFrame:
    with sqlite3.connect(db_path) as conn:
        gender_factors_to_insert = []

        for _, row in df.iterrows():
            person_key = (
                f"{row['year']}-{row['pdf_page_number']}-TODO_add_row_nr_to_key"
            )

            if re.search(WIDOW_PATTERN, row["first_names"]):
                df.at[_, "first_names"] = re.sub(WIDOW_PATTERN, "", row["first_names"])
                gender_factors_to_insert.append((person_key, "widow", "F"))
            elif re.search(WIDOWER_PATTERN, row["partner_last_name"]):
                df.at[_, "partner_last_name"] = re.sub(
                    WIDOWER_PATTERN, "", row["partner_last_name"]
                )
                gender_factors_to_insert.append((person_key, "widower", "M"))

        conn.executemany(
            f"""
            INSERT INTO {GENDER_FACTORS_TABLE_NAME} (address_book_entry_key, factor_name, gender_from_factor)
            VALUES (?, ?, ?)
        """,
            gender_factors_to_insert,
        )

    return df


def calculate_gender(gender_factors: list) -> tuple[str, float]:
    # TODO: implement gender factors calculation
    return "TODO", 1.0


def calculate_gender_factors(df: DataFrame, db_path: Path) -> DataFrame:
    with sqlite3.connect(db_path) as conn:
        query = f"SELECT * FROM {GENDER_FACTORS_TABLE_NAME}"
        table_data = pd.read_sql_query(query, conn)
        all_gender_factors = table_data.to_dict(orient="records")
        result = []

        for _, row in df.iterrows():
            person_key = (
                f"{row['year']}-{row['pdf_page_number']}-TODO_add_row_nr_to_key"
            )
            found_persons_gender_factors = [
                factor
                for factor in all_gender_factors
                if factor.get("key") == person_key
            ]
            gender, probability = calculate_gender(found_persons_gender_factors)

            result.append(
                (
                    row["first_names"],
                    row["own_last_name"],
                    row["partner_last_name"],
                    gender,
                    probability,
                    row["street_name"],
                    row["house_number"],
                    row["job"],
                    row["original_names"],
                    row["last_names"],
                    row["year"],
                    row["pdf_page_number"],
                )
            )

        conn.executemany(
            f"""
                    INSERT INTO {PANEL_DATA_TABLE_NAME} (first_names, own_last_name, partner_last_name, gender, gender_confidence, street_name, house_number, job, original_names, last_names, year, pdf_page_number)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
            result,
        )

        return pd.DataFrame(
            result,
            columns=[
                "first_names",
                "own_last_name",
                "partner_last_name",
                "gender",
                "gender_confidence",
                "street_name",
                "house_number",
                "job",
                "original_names",
                "last_names",
                "year",
                "pdf_page_number",
            ],
        )


def wrangle_dataset(df: DataFrame, db_path: Path) -> DataFrame:
    # TODO: delete the cases with "KEINE ANGABE"
    # TODO: identify family names that occur > 500 times
    # TODO: from names with more than two: move names that do not occur > 500 times to first name

    df = separate_last_and_first_names(df)
    df = separate_last_names(df)
    df = identify_widow_and_widower(df, db_path)
    df = calculate_gender_factors(df, db_path)

    return df
