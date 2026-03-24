from dataclasses import dataclass
from typing import Optional


@dataclass
class AddressBookEntry:
    own_last_name: str
    partner_last_name: str
    first_names: str
    gender: str
    street_name: str
    house_number: str
    job: str
    year: int
    page_reference: str
    original_entry: str
    remarks: Optional[str] = ""
