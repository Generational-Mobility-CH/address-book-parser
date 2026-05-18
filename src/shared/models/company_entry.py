"""Company entry extracted from address book pages."""
import re
from dataclasses import dataclass

_TELEPHON_PATTERN = re.compile(r"Telephon\s+([\d\s]+)")
_POSTCHECK_PATTERN = re.compile(r"Postcheck\s+([VI\d\s]+)")


@dataclass
class CompanyEntry:
    company_name: str
    full_text: str
    original_entry: str
    year: int
    pdf_page_number: int
    telephone_number: str = ""
    postcheck_number: str = ""

    @property
    def __dict__(self):
        return {
            "company_name": self.company_name,
            "full_text": self.full_text,
            "original_entry": self.original_entry,
            "telephone_number": self.telephone_number,
            "postcheck_number": self.postcheck_number,
            "year": self.year,
            "pdf_page_number": self.pdf_page_number,
        }


def extract_company_info(text: str) -> tuple[str, str]:
    """Extract telephone and postcheck numbers from company text.

    Returns (telephone_number, postcheck_number).
    """
    tel = ""
    post = ""
    if m := _TELEPHON_PATTERN.search(text):
        tel = m.group(1).strip()
    if m := _POSTCHECK_PATTERN.search(text):
        post = m.group(1).strip()
    return tel, post
