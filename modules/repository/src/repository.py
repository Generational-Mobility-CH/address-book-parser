from abc import abstractmethod, ABC
from pathlib import Path
from typing import TypeVar

T = TypeVar("T")


class Repository(ABC):
    @abstractmethod
    def save(self, data: list[T], output_path: Path) -> None:
        pass
