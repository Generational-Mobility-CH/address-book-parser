"""Company entry extracted from address book pages."""
import re
from dataclasses import dataclass

from src.shared.models.address import Address

_TELEPHON_PATTERN = re.compile(r"\bTel(?:ephon)?\.?\s*([\d\s]+)", re.IGNORECASE)
_POSTCHECK_PATTERN = re.compile(r"Postcheck\s+([VI\d\s]+)", re.IGNORECASE)


@dataclass
class CompanyEntry:
    company_name: str
    activity: str
    address: Address
    year: int
    pdf_page_number: int
    original_entry: str
    full_text: str
    telephone: bool = False
    postcheck: bool = False
    telephone_number: str = ""
    postcheck_number: str = ""

    @property
    def __dict__(self):
        return {
            "company_name": self.company_name,
            "activity": self.activity,
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
            "telephone_number": self.telephone_number,
            "postcheck_number": self.postcheck_number,
            "year": self.year,
            "pdf_page_number": self.pdf_page_number,
            "original_entry": self.original_entry,
            "full_text": self.full_text,
        }


def extract_company_info(text: str) -> tuple[bool, str, bool, str]:
    """Extract telephone and postcheck flags + numbers from company text.

    Returns (has_telephone, telephone_number, has_postcheck, postcheck_number).
    """
    has_tel = False
    tel_num = ""
    has_post = False
    post_num = ""
    if m := _TELEPHON_PATTERN.search(text):
        has_tel = True
        tel_num = m.group(1).strip()
    if m := _POSTCHECK_PATTERN.search(text):
        has_post = True
        post_num = m.group(1).strip()
    return has_tel, tel_num, has_post, post_num
