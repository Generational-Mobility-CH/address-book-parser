from pathlib import Path

from jsonschema import validate, ValidationError
from dacite import from_dict, Config

from libs.file_handler.src.json.reader import read_json
from modules.persons.models.address_book.addressBookPage import AddressBookPage


PROJECT_ROOT = Path(__file__).resolve().parents[4]


def deserialize_book_page(data: dict) -> AddressBookPage:
    schema_file_path = (
        PROJECT_ROOT
        / "libs"
        / "file_handler"
        / "src"
        / "json"
        / "schemas"
        / "book_page_schema.json"
    )
    schema = read_json(schema_file_path)

    try:
        validate(instance=data, schema=schema)
    except ValidationError as e:
        raise ValueError(f"Invalid input data: {e.message}\ndata: {data}")

    return from_dict(AddressBookPage, data, Config(convert_key=to_camel_case))


def to_camel_case(key: str) -> str:
    first_part, *remaining_parts = key.split("_")
    return first_part + "".join(part.title() for part in remaining_parts)
