import csv
from pathlib import Path

from libs.file_handler.src.util.get_page_information_from_file import (
    get_page_info_from_file,
)
from libs.file_handler.src.util.get_year_from_file_name import get_year_from_file
from modules.text_standardizer.src.street_name_standardizer import (
    standardize_street_name,
)
from modules.utility import (
    substitute_with_map,
)
from modules.transcriptor.src.constants.csv_header import CSV_HEADER
from modules.text_standardizer.src.constants.name_abbreviations import (
    FIRST_NAME_ABBREVIATIONS_MAP_FEMALE,
    FIRST_NAME_ABBREVIATIONS_MAP_MALE,
)
from modules.transcriptor.src.model.AddressBookEntry import AddressBookEntry


def _handle_partner_last_name(data: list[str]) -> list[str]:
    if "-" in data[0]:
        own_last_name, partner_last_name = data[0].split("-", maxsplit=1)
        if len(data) >= 2 and "NONE" in data[1]:
            data[0] = own_last_name
            data[1] = partner_last_name
        elif len(data) == len(CSV_HEADER) - 1:
            data[0] = own_last_name
            data.insert(1, partner_last_name)

    return data


def _normalize_first_names(data: list[str]) -> list[str]:
    if len(data) >= 3:
        first_names = data[2].lower()

        if "." in first_names:
            abbreviated_name_pattern = r"\b{PLACEHOLDER}"
            if "f" in data[3].lower():
                cleaned_first_names = substitute_with_map(
                    first_names,
                    FIRST_NAME_ABBREVIATIONS_MAP_FEMALE,
                    abbreviated_name_pattern,
                )
            else:
                cleaned_first_names = substitute_with_map(
                    first_names,
                    FIRST_NAME_ABBREVIATIONS_MAP_MALE,
                    abbreviated_name_pattern,
                )
            data[2] = cleaned_first_names.title()

    return data


def _standardize_data(data: list[str]) -> list[str]:
    if len(data) >= 5:
        street_name = data[4]
        standardized_street_name = standardize_street_name(street_name)
        data[4] = standardized_street_name

    return data


def _clean_data(data: list[str]) -> list[str]:
    stripped_data = [item.strip().strip('"') for item in data]
    separated_data = _handle_partner_last_name(stripped_data)
    standardized_data = _standardize_data(separated_data)
    normalized_data = _normalize_first_names(standardized_data)

    return normalized_data


def _parse_row(data: list[str], year: int, page_info: str) -> AddressBookEntry | None:
    if len(data) <= 6:
        return None

    cleaned_data = _clean_data(data)

    entry = AddressBookEntry(
        own_last_name=cleaned_data[0],
        partner_last_name=cleaned_data[1],
        first_names=cleaned_data[2],
        gender=cleaned_data[3],
        street_name=cleaned_data[4],
        house_number=cleaned_data[5],
        job=cleaned_data[6],
        original_entry=cleaned_data[-1],
        year=year,
        page_reference=page_info,
    )

    if len(cleaned_data) == len(CSV_HEADER):
        entry.remarks = cleaned_data[7]

    return entry


def clean_persons_csv(data_dir: Path) -> list[AddressBookEntry]:
    # TODO: parallelize method
    address_book_entries = []

    for csv_file in data_dir.glob("**/*.csv"):
        year = get_year_from_file(csv_file)
        page_info = get_page_info_from_file(csv_file)
        csv_reader = csv.reader(csv_file.open("r", encoding="utf-8"), delimiter=";")

        for row in csv_reader:
            if entry := _parse_row(row, year, page_info):
                address_book_entries.append(entry)

    return address_book_entries
