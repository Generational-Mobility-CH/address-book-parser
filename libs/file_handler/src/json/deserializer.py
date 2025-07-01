from logging import getLogger
from pathlib import Path

from jsonschema import validate, ValidationError

from libs.file_handler.src.json.reader import read_json
from libs.file_handler.src.util.list_to_name_range_object import (
    list_to_name_range_object,
)
from modules.persons.src.models.address_book.address_book_page import AddressBookPage

PROJECT_ROOT = Path(__file__).resolve().parents[4]

logger = getLogger(__name__)


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

    if "surnameRange" not in data:
        logger.error("Missing 'surnameRange' in data")
    if "textColumns" not in data:
        logger.error("Missing 'textColumns' in data")
    if "pdfPageNumber" not in data:
        logger.error("Missing 'pdfPageNumber' in data")

    return AddressBookPage(
        surname_range=list_to_name_range_object(data.get("surnameRange", [])),
        text_content=list(data.get("textColumns", {}).values()),
        pdf_page_number=data.get("pdfPageNumber", 0),
    )
