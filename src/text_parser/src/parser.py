from logging import getLogger

from src.shared.models.address_book.address_book import (
    AddressBook,
)
from src.shared.models.address_book.address_book_page import (
    AddressBookPage,
)
from src.shared.models.address_book.name_range import (
    NameRange,
)
from src.shared.models.company_entry import (
    CompanyEntry,
    extract_company_info,
)
from src.shared.models.panel_data_entry import PanelDataEntry
from src.shared.models.person_data_parts import (
    PersonDataParts,
)
from src.text_cleaner.src.line_breaks_cleaner import (
    has_line_break,
    merge_line_break,
)
from src.text_cleaner.src.text_cleaner import (
    _clean_line,
)
from src.text_parser.src.company_parser import (
    is_company,
)
from src.text_parser.src.last_name_parser import (
    get_next_last_name,
    get_next_last_name_without_range,
)
from src.text_parser.src.name_range_handler import (
    is_valid_last_name_range,
    find_next_valid_name_range_start_or_end,
    find_next_valid_name_range,
)
from src.text_parser.src.person_parser import (
    parse_person,
)
from src.text_parser.src.prefix_extractor import extract_entry_symbols
from src.text_parser.src.separator.separator import separate_information

_logger = getLogger(__name__)


def _clean_with_metadata(
    lines: list[str],
    metadata: list[tuple[bool, bool]],
) -> tuple[list[str], list[tuple[bool, bool]]]:
    """Run text cleaning while keeping metadata aligned with output lines."""
    paired = [(ln, m) for ln, m in zip(lines, metadata) if ln]

    result: list[tuple[str, tuple[bool, bool]]] = []
    for line, meta in paired:
        cleaned = _clean_line(line)
        if cleaned is None:
            continue

        if result and has_line_break(cleaned, result[-1][0]):
            merged = merge_line_break(cleaned, result[-1][0])
            prev_meta = result[-1][1]
            merged_meta = (prev_meta[0] or meta[0], prev_meta[1] or meta[1])
            result[-1] = (merged, merged_meta)
            continue

        result.append((cleaned, meta))

    return [r[0] for r in result], [r[1] for r in result]


def _group_data(
    data: list[str],
    metadata: list[tuple[bool, bool]],
) -> list[tuple[PersonDataParts, tuple[bool, bool]]]:
    result: list[tuple[PersonDataParts, tuple[bool, bool]]] = []

    for line, meta in zip(data, metadata):
        content = line.split(",")
        stripped_content = []
        for e in content:
            e = e.strip()
            if e and any(char.isalnum() for char in e):
                stripped_content.append(e)

        if len(stripped_content) in (2, 3):
            result.append((PersonDataParts.from_list(stripped_content), meta))

    return result


def _parse_address_book_page(
    page: AddressBookPage,
) -> tuple[list[PanelDataEntry], list[CompanyEntry]]:
    splitted_lines = [line for text in page.text_content for line in text.split("\n")]

    # Extract ●/‡ symbols before clean_text destroys them
    line_metadata = []
    stripped_lines = []
    for line in splitted_lines:
        tel, post, cleaned = extract_entry_symbols(line)
        line_metadata.append((tel, post))
        stripped_lines.append(cleaned)

    cleaned_lines, aligned_metadata = _clean_with_metadata(
        stripped_lines, line_metadata
    )
    page.text_content = cleaned_lines

    return _parse_persons(page, aligned_metadata)


def _parse_persons(
    page: AddressBookPage,
    metadata: list[tuple[bool, bool]],
) -> tuple[list[PanelDataEntry], list[CompanyEntry]]:
    output = []
    companies = []
    current_last_name = ""
    previous_last_name = ""
    grouped_information = _group_data(page.text_content, metadata)
    has_valid_last_names_range = is_valid_last_name_range(page.last_names_range)

    for group, meta in grouped_information:
        if is_company(group):
            full_text = f"{group.first}, {group.second}"
            if group.third:
                full_text += f", {group.third}"
            tel_num, post_num = extract_company_info(full_text)
            company = CompanyEntry(
                company_name=group.first.split(",")[0].strip(),
                full_text=full_text,
                original_entry=full_text,
                year=page.year,
                pdf_page_number=page.pdf_page_number,
                telephone_number=tel_num,
                postcheck_number=post_num,
            )
            companies.append(company)
            continue

        if len(group) in (2, 3):
            if has_valid_last_names_range:
                group.first, current_last_name = get_next_last_name(
                    group.first, current_last_name, page.last_names_range
                )
            else:
                group.first, current_last_name, previous_last_name = (
                    get_next_last_name_without_range(
                        group.first, current_last_name, previous_last_name
                    )
                )

            person = parse_person(group, current_last_name)
            person.year = page.year
            person.pdf_page_number = page.pdf_page_number
            person.telephone = meta[0]
            person.postcheck = meta[1]

            if person not in output:
                output.append(person)

    return output, companies


def parse_address_book(
    address_book: AddressBook,
) -> tuple[list[PanelDataEntry], list[CompanyEntry]]:
    persons_collection: list[PanelDataEntry] = []
    companies_collection: list[CompanyEntry] = []

    if len(address_book.pages) < 1:
        _logger.warning(f"No pages found. Skipping book for year {address_book.year}.")
        return [], []

    _logger.info(f"Parsing book from year {address_book.year}...")

    pages_collection = address_book.pages
    first_page = address_book.pages[0]

    first_page.last_names_range = NameRange(
        start="A", end=find_next_valid_name_range_start_or_end(pages_collection, 1)
    )

    persons, companies = _parse_address_book_page(first_page)
    persons_collection.extend(persons)
    companies_collection.extend(companies)

    for page_index in range(1, len(pages_collection)):
        page = address_book.pages[page_index]
        _logger.debug(f"Parsing page {page.pdf_page_number} from year {page.year}...")

        if not is_valid_last_name_range(page.last_names_range):
            if found_next_valid_range := find_next_valid_name_range(
                pages_collection, page_index
            ):
                page.last_names_range = found_next_valid_range
            else:
                _logger.warning(
                    f"Could not approximate 'NameRange' for {address_book.year}-page_{page.pdf_page_number}"
                )

        persons, companies = _parse_address_book_page(page)
        persons_collection.extend(persons)
        companies_collection.extend(companies)

    panel_data = separate_information(persons_collection)

    return panel_data, companies_collection
