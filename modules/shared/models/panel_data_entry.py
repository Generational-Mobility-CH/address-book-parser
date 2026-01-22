import logging
from typing import Optional

from modules.shared.models.address import Address
from modules.text_parser.src.constants.gender_descriptors import GENDER_UNKNOWN
from modules.shared.models.address_book.address_book_entry import AddressBookEntry

logger = logging.getLogger(__name__)


class PanelDataEntry(AddressBookEntry):
    def __init__(
        self,
        first_names: str,
        last_names: str,
        job: str,
        street_name: str,
        house_number: str,
        year: int,
        pdf_page_number: int,
        original_entry: str,
        partner_last_names: Optional[str] = "",
        gender: str = GENDER_UNKNOWN,
        gender_from: Optional[str] = "",
    ) -> None:
        super().__init__(
            original_names=original_entry,
            job=job,
            address=Address(street_name=street_name, house_number=house_number),
            year=year,
            pdf_page_number=pdf_page_number,
        )
        self._first_names = first_names
        self._last_names = last_names
        self._partner_last_names = partner_last_names
        self._gender = gender
        self._gender_confidence = gender_from
        self._original_entry = f"{self._last_names} {self._partner_last_names} {self._first_names}, {self.address}, {self.job}"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(first_names='{self.first_names}', last_names='{self.last_names}', partner_last_names='{self.partner_last_names}, gender='{self.gender}', gender_confidence={self.gender_confidence}, year={self.year}, {super().__repr__()}"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, PanelDataEntry):
            return NotImplemented
        return (
            self.first_names == other.first_names
            and self.last_names == other.last_names
            and self.partner_last_names == other.partner_last_names
            and self.original_names == other.original_names
            and self.job == other.job
            and self.address == other.address
            and self.gender == other.gender
            and self.gender_confidence == other.gender_confidence
            and self.year == other.year
            and self.pdf_page_number == other.pdf_page_number
        )

    def __str__(self) -> str:
        return (
            f"{self.first_names} {self.last_names}, {self.job}, "
            f"Address: {self.address.street_name} {self.address.house_number}, Gender: {self.gender}"
        )

    @property
    def first_names(self) -> str:
        return self._first_names

    @first_names.setter
    def first_names(self, value: str) -> None:
        self._first_names = value

    @property
    def last_names(self) -> str:
        return self._last_names

    @last_names.setter
    def last_names(self, value: str) -> None:
        self._last_names = value

    @property
    def partner_last_names(self) -> str:
        return self._partner_last_names

    @partner_last_names.setter
    def partner_last_names(self, value: str) -> None:
        self._partner_last_names = value

    @property
    def gender(self) -> str:
        return self._gender

    @gender.setter
    def gender(self, value: str) -> None:
        self._gender = value

    @property
    def gender_confidence(self) -> str:
        return self._gender_confidence

    @gender_confidence.setter
    def gender_confidence(self, value: str) -> None:
        self._gender_confidence = value
