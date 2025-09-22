from abc import abstractmethod, ABC
from pathlib import Path
from typing import List

from ..models.person.person import Person


class PersonRepository(ABC):
    @abstractmethod
    def save(self, persons: List[Person], output_path: Path) -> None:
        pass
