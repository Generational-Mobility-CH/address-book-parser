from dataclasses import dataclass, field

from modules.persons.models.addressBookPage import AddressBookPage


@dataclass
class AddressBook:
    year: int
    pages: list[AddressBookPage] = field(default_factory=list)
