import logging
import re
import uuid

from modules.persons.common.special_chars import (
    TAG_NONE_FOUND,
    KEYWORDS_SPECIAL_LAST_NAMES,
    KEYWORDS_NAMES_SPLITTING,
)
from modules.persons.models.address import Address
from modules.persons.models.person_names import PersonNames
from modules.persons.src.standardizer.first_names_standardizer import FirstNamesStandardizer
from modules.persons.src.standardizer.job_standardizer import JobStandardizer
from modules.persons.src.standardizer.last_names_standardizer import LastNamesStandardizer
from modules.persons.src.standardizer.street_name_standardizer import StreetNameStandardizer

logger = logging.getLogger(__name__)


class Person:
    def __init__(
        self, original_names: str, job: str, address: Address
    ) -> None:
        self.last_names: str = ""
        self.first_names: str = ""
        self.original_names = original_names
        self.job = job
        self.address = address
        self.year: int = 0
        self.pdf_page_number: int | None = None
        self.person_id = uuid.uuid4()

    @property
    def original_names(self) -> str:
        return self._original_names

    @original_names.setter
    def original_names(self, value: str) -> None:
        if not value:
            print("original_names cannot be empty.")
        self._original_names = value

    @property
    def last_names(self) -> str:
        return self._last_names

    @last_names.setter
    def last_names(self, value: str) -> None:
        self._last_names = value

    @property
    def first_names(self) -> str:
        return self._first_names

    @first_names.setter
    def first_names(self, value: str) -> None:
        self._first_names = value

    @property
    def job(self) -> str:
        return self._job

    @job.setter
    def job(self, value: str) -> None:
        self._job = value

    @property
    def address(self) -> Address:
        return self._address

    @address.setter
    def address(self, value: Address) -> None:
        self._address = value

    @property
    def year(self) -> int:
        return self._year

    @year.setter
    def year(self, value: int) -> None:
        self._year = value

    @property
    def person_id(self) -> uuid.uuid4():
        return self._person_id

    @person_id.setter
    def person_id(self, value: uuid.uuid4()) -> None:
        self._person_id = value

    @property
    def pdf_page_number(self) -> int | None:
        return self._pdf_page_number

    @pdf_page_number.setter
    def pdf_page_number(self, value: int) -> None:
        self._pdf_page_number = value

    def __repr__(self) -> str:
        return (
            f"Person(Full name={self.last_names} {self.first_names}, job={self.job}, address={repr(self.address)}, year={self.year}, id={self.person_id})"
        )

    def __str__(self) -> str:
        return f"Vollständiger Name: {self.last_names} {self.first_names}\nJob: {self.job}\nAddresse: {self.address}\nJahr: {self.year}"

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Person):
            return (
                self.last_names == other.last_names
                and self.first_names == other.first_names
                and self.job == other.job
                and self.address == other.address
                and self.year == other.year
                and self.person_id == other.person_id
            )
        return False

    def standardize_attributes(self) -> "Person":
        self.separate_names()
        self.last_names = LastNamesStandardizer().standardize(self.last_names)
        self.first_names = FirstNamesStandardizer().standardize(self.first_names)
        self.job = JobStandardizer().standardize(self.job)
        self.address.street_name = StreetNameStandardizer().standardize(self.address.street_name)

        return self


    def separate_names(self) -> None:
        found_marker = get_splitting_marker_if_present(self.original_names)
        if found_marker:
            name_parts = split_at_marker(self.original_names, found_marker)
            self.last_names, self.first_names = name_parts.last_names, name_parts.first_names

        elif any(substr in self.original_names.lower() for substr in KEYWORDS_SPECIAL_LAST_NAMES):
            name_parts = extract_special_last_names(self.original_names)
            self.last_names, self.first_names = name_parts.last_names, name_parts.first_names

        else:
            parts = self.original_names.split(" ")

            match len(parts):
                case 1:
                    self.original_names = unmerge_name_parts(parts[0])

                    if len(self.original_names.split(" ")) == 1:
                        # TODO: how sure are we that it's the first name?
                        self.first_names = self.original_names.strip()
                        self.last_names = TAG_NONE_FOUND
                    else:
                        self.separate_names()
                        return
                case 2:
                    self.last_names = parts[0]
                    self.first_names = parts[1]
                case 3:
                    # TODO: refine this case ???
                    self.last_names = f"{parts[0]} {parts[1]}"
                    self.first_names = parts[2]
                case 4:
                    # TODO: refine this case ???
                    self.last_names = f"{parts[0]} {parts[1]}"
                    self.first_names = f"{parts[2]} {parts[3]}"
                case _:
                    # TODO: add AI request here to handle this case ???
                    logger.error(f"Could not parse name: {self.original_names}")
                    self.last_names = self.original_names
                    self.first_names = "<TODO>"


def get_splitting_marker_if_present(data: str) -> str | None:
    found_marker = None

    for marker in KEYWORDS_NAMES_SPLITTING:
        if marker in data.lower():
            found_marker = marker
            break

    if found_marker is None:
        first_name_abbreviation_pattern = r"\b\w{1,3}\."
        match = re.search(first_name_abbreviation_pattern, data.lower())
        if match:
            found_marker = match.group(0)

    return found_marker


def split_at_marker(data: str, marker: str) -> PersonNames:
    s = data.lower()
    parts = s.split(marker, 1)

    name_parts = PersonNames(
        last_names="",
        first_names=marker.strip().capitalize()
    )
    name_parts.last_names += " ".join(word.capitalize().strip() for word in parts[0].split(" "))
    name_parts.first_names += " ".join(word.capitalize().strip() for word in parts[1].split(" "))

    return name_parts


def extract_special_last_names(data: str) -> PersonNames:
    # TODO
    return PersonNames(last_names=data, first_names=data)


def unmerge_name_parts(data: str) -> str:
    marker = "|"

    s = re.split(r"(?<![ -])(?=[A-ZÄÖÜẞ])", data)
    s = " ".join([part.strip() for part in s if part.strip()])

    s = s.replace(")", f"){marker}")
    s = s.replace("(", " (")

    s = s.replace("—", marker)
    s = s.replace("-", marker)

    return s.replace(marker, " ").strip()
