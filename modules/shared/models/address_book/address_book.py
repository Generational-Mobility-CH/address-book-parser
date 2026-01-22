from dataclasses import dataclass, field

from modules.shared.models.address_book.address_book_page import (
    AddressBookPage,
)


@dataclass
class AddressBook:
    year: int = None
    pages: list[AddressBookPage] = field(default_factory=list)
