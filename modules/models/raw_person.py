import uuid

from modules.models.address import Address


class RawPerson:
    def __init__(
        self, names: str, job: str, address: Address, year: int = 0
    ) -> None:
        self.names = names
        self.job = job
        self.address = address
        self.year = year
        self.pdf_page_number: int | None = None
        self.person_id = uuid.uuid4()

    @property
    def names(self) -> str:
        return self._names

    @names.setter
    def names(self, value: str) -> None:
        if not value:
            print("names cannot be empty.")
        self._names = value

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
    def pdf_page_number(self) -> int | None:
        return self._pdf_page_number

    @pdf_page_number.setter
    def pdf_page_number(self, value: int) -> None:
        self._pdf_page_number = value

    @property
    def year(self) -> int:
        return self._year

    @year.setter
    def year(self, value: int) -> None:
        self._year = value

    def get_person_id(self) -> uuid.UUID:
        return self.person_id

    def __repr__(self) -> str:
        return (
            f"Person(names={self.names}, job={self.job}, address={repr(self.address)}, year={self.year}, id={self.person_id})"
        )

    def __str__(self) -> str:
        return f"Vollständiger Name: {self.names}\nJob: {self.job}\nAddresse: {self.address}\nJahr: {self.year}"

    def __eq__(self, other: object) -> bool:
        if isinstance(other, RawPerson):
            return (
                self.names == other.names
                and self.job == other.job
                and self.address == other.address
                and self.year == other.year
                and self.person_id == other.person_id
            )
        return False
