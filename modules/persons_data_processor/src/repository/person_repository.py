from abc import abstractmethod, ABC
from pathlib import Path

from ..models.person.person import Person


class PersonRepository(ABC):
    @abstractmethod
    def save(self, persons: list[Person], output_path: Path) -> None:
        pass
