class Address:
    def __init__(
        self,
        street_name: str,
        house_number: str,
        city: str = "Basel",
        postal_code: int = None,
        country: str = "Schweiz",
    ) -> None:
        self.street_name = street_name
        self.house_number = house_number
        self.postal_code = postal_code
        self.city = city
        self.country = country

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
    def postal_code(self) -> int:
        return self._postal_code

    @postal_code.setter
    def postal_code(self, value: int) -> None:
        self._postal_code = value

    @property
    def city(self) -> str:
        return self._city

    @city.setter
    def city(self, value: str) -> None:
        self._city = value

    @property
    def country(self) -> str:
        return self._country

    @country.setter
    def country(self, value: str) -> None:
        self._country = value

    def __repr__(self) -> str:
        return (
            f"Address(street_name={self.street_name}, house_number={self.house_number}, "
            f"city={self.city}, postal_code={self.postal_code}, country={self.country})"
        )

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Address):
            return (
                self.street_name == other.street_name
                and self.house_number == other.house_number
                and self.city == other.city
                and self.postal_code == other.postal_code
                and self.country == other.country
            )
        return False

    def __str__(self) -> str:
        return f"{self.street_name} {self.house_number}"
