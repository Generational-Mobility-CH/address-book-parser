from dataclasses import dataclass, field

from modules.persons.src.models.address_book.addressBookPage import AddressBookPage


@dataclass
class AddressBook:
    year: int = None
    pages: list[AddressBookPage] = field(default_factory=list)
