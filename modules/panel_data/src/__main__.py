from datetime import datetime
from logging import getLogger
from pathlib import Path

from libs.db_handler.src.open_db import get_table_entries, get_latest_db_file
from modules.panel_data.src.constants.paths import (
    PANEL_DATA_OUTPUT_PATH,
    PANEL_DATA_INPUT_PATH,
)
from modules.panel_data.src.gender_calculator.gender_calculator import identify_females
from modules.panel_data.src.models.new_person import NewPerson
from modules.panel_data.src.repository.panel_data_repository import PanelDataRepository
from modules.panel_data.src.separator.separator import separate_information
from modules.panel_data.src.setup import setup
from modules.persons_data_processor.src.constants.database_table_names import (
    PERSONS_ENTRIES_TABLE_NAME,
)
from modules.persons_data_processor.src.models.person.address import Address
from modules.persons_data_processor.src.models.person.person import Person
from modules.persons_data_processor.src.repository.constants.db_column_names import (
    DB_COLUMN_NAMES,
)
from modules.shared.constants.years_range import YEARS_RANGE

logger = getLogger(__name__)


# TODO: move Persons+Address classes into /shared
def main(input_path: Path, output_path: Path) -> None:
    logger.info(f"Reading data from {input_path}")

    for year in YEARS_RANGE:
        entries = get_table_entries(
            input_path, PERSONS_ENTRIES_TABLE_NAME, f" WHERE year LIKE {year}"
        )

        persons = []
        for row in entries:
            person_data = dict(zip(DB_COLUMN_NAMES, row))
            address = Address(
                street_name=person_data.pop("street_name"),
                house_number=person_data.pop("house_number"),
            )
            person = Person(address=address, **person_data)
            persons.append(person)

        logger.info(f"Parsing persons from year {year}")
        persons = parse_panel_data_set(persons, output_path)

        PanelDataRepository().save(persons, output_path)
        logger.info(f"Saved persons to '{output_path}'")


def parse_panel_data_set(persons: list[Person], db_path: Path) -> list[NewPerson]:
    persons = separate_information(persons)
    persons = identify_females(persons, db_path)
    # persons = standardize_information(persons)

    return persons


if __name__ == "__main__":
    demo_input_path = get_latest_db_file(PANEL_DATA_INPUT_PATH)
    time_stamp = f"{datetime.now():%b %d - %H%M%S}"
    demo_output_path = PANEL_DATA_OUTPUT_PATH / "db" / f"{time_stamp}.db"

    setup(time_stamp)
    main(demo_input_path, demo_output_path)
