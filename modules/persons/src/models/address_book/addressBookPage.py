from dataclasses import dataclass


@dataclass
class AddressBookPage:
    surname_range: list[str]
    text_columns: dict
    pdf_page_number: int = 0
