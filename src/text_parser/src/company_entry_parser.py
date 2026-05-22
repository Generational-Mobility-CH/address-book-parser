"""Parse structured company entries from grouped data parts."""
import re

from src.shared.constants.tags import TAG_NONE_FOUND
from src.shared.models.address import Address
from src.shared.models.company_entry import CompanyEntry, extract_company_info
from src.shared.models.person_data_parts import PersonDataParts
from src.text_cleaner.src.address_cleaner import clean_address
from src.text_parser.src.address_parser import is_address, extract_address

# Patterns for continuation fragments (telephone/postcheck data belonging to previous entry)
_CONTINUATION_PATTERNS = [
    re.compile(r"^Tel\.?\s+\d", re.IGNORECASE),
    re.compile(r"^Postcheck\s+[VI\d]", re.IGNORECASE),
]

# Patterns for junk entries (page headers, instructions — no useful data)
_JUNK_PATTERNS = [
    re.compile(r"^Die Telephonabonnenten", re.IGNORECASE),
]


def is_continuation_fragment(full_text: str) -> bool:
    """Detect entries that are telephone/postcheck data belonging to the entry above."""
    text = full_text.strip()
    return any(p.match(text) for p in _CONTINUATION_PATTERNS)


def is_junk_entry(full_text: str) -> bool:
    """Detect page headers and other meaningless entries to discard."""
    text = full_text.strip()
    return any(p.match(text) for p in _JUNK_PATTERNS)


def merge_fragment_into_company(company: CompanyEntry, fragment_text: str) -> None:
    """Merge telephone/postcheck info from a continuation fragment into a company."""
    has_tel, tel_num, has_post, post_num = extract_company_info(fragment_text)
    if has_tel and not company.telephone:
        company.telephone = True
        company.telephone_number = tel_num
    if has_post and not company.postcheck:
        company.postcheck = True
        company.postcheck_number = post_num
    # Append fragment to full_text for traceability
    company.full_text += " " + fragment_text.strip()


def parse_company(
    data: PersonDataParts,
    current_last_name: str,
) -> CompanyEntry:
    """Parse a company entry from grouped data parts.

    Company format varies:
      - 2 parts: [name, address] or [name, activity]
      - 3 parts: [name, address, activity] or [name, activity, address]
    """
    full_text = f"{data.first}, {data.second}"
    if data.third:
        full_text += f", {data.third}"

    company_name = data.first.strip()

    # Handle "-" prefix: prepend current last name
    if company_name.startswith("-"):
        if current_last_name:
            company_name = current_last_name + company_name

    # Extract telephone/postcheck from full text
    has_tel, tel_num, has_post, post_num = extract_company_info(full_text)

    # Find address and activity from the parts
    address = Address(
        street_name=TAG_NONE_FOUND, house_number=TAG_NONE_FOUND, coordinates=None
    )
    activity = ""

    if len(data) == 2:
        if is_address(data.second):
            address = extract_address(data.second)
        else:
            activity = data.second.strip()
    elif len(data) == 3:
        second_is_address = is_address(data.second)
        third_is_address = is_address(data.third) if data.third else False

        if third_is_address:
            address = extract_address(data.third)
            activity = data.second.strip()
        elif second_is_address:
            address = extract_address(data.second)
            activity = data.third.strip() if data.third else ""
        else:
            activity = data.second.strip()

    address = clean_address(address)

    return CompanyEntry(
        company_name=company_name,
        activity=activity,
        address=address,
        year=0,
        pdf_page_number=0,
        original_entry=full_text,
        full_text=full_text,
        telephone=has_tel,
        postcheck=has_post,
        telephone_number=tel_num,
        postcheck_number=post_num,
    )
