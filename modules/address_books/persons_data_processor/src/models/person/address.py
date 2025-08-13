class Address:
    def __init__(
        self,
        street_name: str,
        house_number: str,
    ) -> None:
        self.street_name = street_name
        self.house_number = house_number

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

    def __repr__(self) -> str:
        return (
            f"Address(street_name={self.street_name}, house_number={self.house_number}"
        )

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Address):
            return (
                self.street_name == other.street_name
                and self.house_number == other.house_number
            )
        return False

    def __str__(self) -> str:
        return f"{self.street_name} {self.house_number}"
