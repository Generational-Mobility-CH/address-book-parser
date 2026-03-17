from dataclasses import dataclass
from typing import Optional

from modules.shared.models.address import Address
from modules.text_parser.src.constants.gender_descriptors import GENDER_UNKNOWN


@dataclass
class PanelDataEntry:
    first_names: str
    last_names: str
    job: str
    address: Address
    year: int
    pdf_page_number: int
    original_entry: str
    gender: str = GENDER_UNKNOWN
    partner_last_names: Optional[str] = ""
    gender_confidence: Optional[str] = ""
    original_names: Optional[str] = ""

    @property
    def __dict__(self):
        base_dict = {
            "first_names": self.first_names,
            "last_names": self.last_names,
            "partner_last_names": self.partner_last_names,
            "job": self.job,
            "gender": self.gender,
            "gender_confidence": self.gender_confidence,
            "street_name": self.address.street_name,
            "house_number": self.address.house_number,
            "year": self.year,
            "pdf_page_number": self.pdf_page_number,
            "original_entry": self.original_entry,
            "coordinates": f"{self.address.coordinates.latitude}, {self.address.coordinates.longitude} ({self.address.coordinates.coordinates_system.value})"
            if self.address.coordinates
            else "",
            "original_names": self.original_names,
        }

        return base_dict
