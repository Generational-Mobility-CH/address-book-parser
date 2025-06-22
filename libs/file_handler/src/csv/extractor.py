import re
import uuid

from libs.file_handler.src.csv.reader import read_csv
from libs.file_handler.src.extractor_strategy import ExtractorStrategy
from modules.common.csv_column_names import COLUMN_NAMES
from modules.common.special_chars import TAG_NONE_FOUND
from modules.models.address import Address
from modules.models.person import Person


class CsvExtractor(ExtractorStrategy):
    def extract(self, data_paths: list[str]) -> list[Person]:
        persons_collection: list[Person] = []

        for path in data_paths:
            content = read_csv(path)
            if all(col in content[0] for col in COLUMN_NAMES):
                for row in content[1:]:
                    information = row.split(',')
                    person = Person(
                        original_names=information[0],
                        job=information[1],
                        address=parse_address(information[2]),
                        year=int(information[3]),
                        person_id=uuid.UUID((information[5])),
                    )
                    persons_collection.append(person)
            else:
                raise ValueError(
                    "Missing one or more required columns in CSV file."
                )

        only_complete_persons = get_only_complete_persons(persons_collection)

        # TODO: Handle persons with missing attributes
        incomplete_persons = get_incomplete_persons(persons_collection)

        return only_complete_persons


def get_only_complete_persons(persons: list[Person]) -> list[Person]:
    result = [
        person
        for person in persons
        if all(value is not TAG_NONE_FOUND for value in vars(person).values())
    ]
    return result


def get_incomplete_persons(persons: list[Person]) -> list[Person]:
    incomplete_persons = [
        person
        for person in persons
        if any(value is TAG_NONE_FOUND for value in vars(person).values())
    ]
    return incomplete_persons


def parse_address(address_str: str) -> Address | str:
    pattern = re.compile(r'(?i)^(\d+\w*)\s+(.*)$|^(.*\D)\s+(\d+\w*)$')

    match = pattern.match(address_str.strip())
    if not match:
        return TAG_NONE_FOUND

    if match.group(1) and match.group(2):  # z.B.: "32a gehweg"
        nr, street = match.group(1), match.group(2)
    else:  # z.B.: "bahnhofstr. 101"
        street, nr = match.group(3), match.group(4)

    return Address(street_name=street.strip(), house_number=nr.strip())
