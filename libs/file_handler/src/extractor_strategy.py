from abc import ABC, abstractmethod
from typing import TypeVar

from modules.models.person import Person


T = TypeVar('T')


class ExtractorStrategy(ABC):
    @abstractmethod
    def extract(self, data_paths: list[str]) -> list[T]:
        pass
