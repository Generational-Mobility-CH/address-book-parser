from dataclasses import dataclass
from typing import Optional

from src.shared.models.address import Address
from src.text_parser.src.constants.gender_descriptors import GENDER_UNKNOWN


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
    prefix: Optional[str] = ""
    telephone: bool = False
    postcheck: bool = False

    @property
    def __dict__(self):
        base_dict = {
            "prefix": self.prefix,
            "first_names": self.first_names,
            "last_names": self.last_names,
            "partner_last_names": self.partner_last_names,
            "job": self.job,
            "gender": self.gender,
            "gender_confidence": self.gender_confidence,
            "street_name": self.address.street_name,
            "house_number": self.address.house_number,
            "latitude_wgs84": self.address.coordinates.latitude_wgs84
            if self.address.coordinates
            else "",
            "longitude_wgs84": self.address.coordinates.longitude_wgs84
            if self.address.coordinates
            else "",
            "easting_lv95": self.address.coordinates.easting_lv95
            if self.address.coordinates
            else "",
            "northing_lv95": self.address.coordinates.northing_lv95
            if self.address.coordinates
            else "",
            "telephone": self.telephone,
            "postcheck": self.postcheck,
            "year": self.year,
            "pdf_page_number": self.pdf_page_number,
            "original_entry": self.original_entry,
        }

        return base_dict
