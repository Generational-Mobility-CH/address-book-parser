from abc import ABC, abstractmethod
from typing import TypeVar

T = TypeVar("T")


class ExtractorStrategy(ABC):
    @abstractmethod
    def extract(self, data_paths: list[str]) -> list[T]:
        pass
