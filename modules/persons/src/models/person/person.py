import logging


from modules.persons.src.models.person.address import Address
from modules.persons.src.standardizer.first_names_standardizer import (
    FirstNamesStandardizer,
)
from modules.persons.src.standardizer.job_standardizer import JobStandardizer
from modules.persons.src.standardizer.last_names_standardizer import (
    LastNamesStandardizer,
)
from modules.persons.src.standardizer.street_name_standardizer import (
    StreetNameStandardizer,
)


logger = logging.getLogger(__name__)


class Person:
    def __init__(self, original_names: str, job: str, address: Address) -> None:
        self.last_names: str = ""
        self.first_names: str = ""
        self.original_names = original_names
        self.job = job
        self.address = address
        self.year: int = 0
        self.pdf_page_number: int | None = None

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
    def pdf_page_number(self) -> int | None:
        return self._pdf_page_number

    @pdf_page_number.setter
    def pdf_page_number(self, value: int) -> None:
        self._pdf_page_number = value

    def __repr__(self) -> str:
        return f"Person(Full name={self.last_names} {self.first_names}, job={self.job}, address={repr(self.address)}, year={self.year})"

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
            )
        return False

    def standardize_attributes(self) -> "Person":
        self.last_names = LastNamesStandardizer().standardize(self.last_names)
        self.first_names = FirstNamesStandardizer().standardize(self.first_names)
        self.job = JobStandardizer().standardize(self.job)
        self.address.street_name = StreetNameStandardizer().standardize(
            self.address.street_name
        )

        return self
