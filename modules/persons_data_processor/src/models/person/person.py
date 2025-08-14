import logging
from typing import Optional

from modules.persons_data_processor.src.models.person.address import (
    Address,
)

logger = logging.getLogger(__name__)


class Person:
    def __init__(self, original_names: str, job: str, address: Address) -> None:
        self.original_names = original_names
        self.job = job
        self.address = address
        self.year: int = 0
        self.pdf_page_number: Optional[int] = None

    @property
    def original_names(self) -> str:
        return self._original_names

    @original_names.setter
    def original_names(self, value: str) -> None:
        if not value:
            print("original_names cannot be empty.")
        self._original_names = value

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
        return f"Person(Name={self.original_names}, job={self.job}, address={repr(self.address)}, year={self.year})"

    def __str__(self) -> str:
        return f"Name: {self.original_names}\nJob: {self.job}\nAddresse: {self.address}\nJahr: {self.year}"

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Person):
            return (
                self.original_names == other.original_names
                and self.job == other.job
                and self.address == other.address
                and self.year == other.year
            )
        return False
