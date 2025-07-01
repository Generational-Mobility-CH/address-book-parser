from dataclasses import dataclass

from modules.persons.src.models.address_book.name_range import NameRange


@dataclass
class AddressBookPage:
    surname_range: NameRange
    text_content: list[str]
    pdf_page_number: int = None
    year: int = None

    def __repr__(self):
        return f"\nYear={self.year}, Pdf page number={self.pdf_page_number} Name range={self.surname_range},\nText columns={self.text_content}"
