import logging
from typing import Optional

from modules.panel_data.src.models.gender import Gender

logger = logging.getLogger(__name__)


class NewPerson:  # TODO: pick better names for both persons classes
    def __init__(
        self,
        first_names: str,
        last_names: str,
        original_names: str,
        job: str,
        street_name: str,
        house_number: str,
        year: int,
        pdf_page_number: int,
        partner_last_names: Optional[str] = "",
        gender: Gender = Gender.MALE,
        gender_confidence: Optional[float] = 0.0,
    ) -> None:
        self._first_names = first_names
        self._last_names = last_names
        self._partner_last_names = partner_last_names
        self._original_names = original_names
        self._job = job
        self._street_name = street_name
        self._house_number = house_number
        self._gender = gender
        self._gender_confidence = gender_confidence
        self._year = year
        self._pdf_page_number = pdf_page_number

    def __repr__(self) -> str:
        return (
            f"NewPerson(first_names='{self.first_names}', last_names='{self.last_names}', "
            f"partner_last_names='{self.partner_last_names}', original_names='{self.original_names}', "
            f"job='{self.job}', street_name='{self.street_name}', house_number={self.house_number}, "
            f"gender='{self.gender}', gender_confidence={self.gender_confidence}, year={self.year}, "
            f"pdf_page_number={self.pdf_page_number})"
        )

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, NewPerson):
            return NotImplemented
        return (
            self.first_names == other.first_names
            and self.last_names == other.last_names
            and self.partner_last_names == other.partner_last_names
            and self.original_names == other.original_names
            and self.job == other.job
            and self.street_name == other.street_name
            and self.house_number == other.house_number
            and self.gender == other.gender
            and self.gender_confidence == other.gender_confidence
            and self.year == other.year
            and self.pdf_page_number == other.pdf_page_number
        )

    def __str__(self) -> str:
        return (
            f"{self.first_names} {self.last_names}, {self.job}, "
            f"Address: {self.street_name} {self.house_number}, Gender: {self.gender}"
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
    def original_names(self) -> str:
        return self._original_names

    @original_names.setter
    def original_names(self, value: str) -> None:
        self._original_names = value

    @property
    def job(self) -> str:
        return self._job

    @job.setter
    def job(self, value: str) -> None:
        self._job = value

    @property
    def street_name(self) -> str:
        return self._street_name

    @street_name.setter
    def street_name(self, value: str) -> None:
        self._street_name = value

    @property
    def house_number(self) -> str:
        return self._house_number

    @house_number.setter
    def house_number(self, value: str) -> None:
        self._house_number = value

    @property
    def gender(self) -> Gender:
        return self._gender

    @gender.setter
    def gender(self, value: Gender) -> None:
        self._gender = value

    @property
    def gender_confidence(self) -> float:
        return self._gender_confidence

    @gender_confidence.setter
    def gender_confidence(self, value: float) -> None:
        self._gender_confidence = value

    @property
    def year(self) -> int:
        return self._year

    @year.setter
    def year(self, value: int) -> None:
        self._year = value

    @property
    def pdf_page_number(self) -> int:
        return self._pdf_page_number

    @pdf_page_number.setter
    def pdf_page_number(self, value: int) -> None:
        self._pdf_page_number = value
