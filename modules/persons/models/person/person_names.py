class PersonNames:
    def __init__(self, first_names: str, last_names: str) -> None:
        self._first_names = first_names
        self._last_names = last_names

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

    def __eq__(self, other: object) -> bool:
        if isinstance(other, PersonNames):
            return (
                self.first_names == other.first_names
                and self.last_names == other.last_names
            )
        return False

    def __repr__(self) -> str:
        return (
            f"PersonNames(Last Names={self.last_names}, First Names={self.first_names})"
        )

    def __str__(self) -> str:
        return f"Last Names={self.last_names}, First Names={self.first_names}"
