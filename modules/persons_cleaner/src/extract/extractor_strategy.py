from abc import ABC, abstractmethod

from modules.models.person import Person


class ExtractorStrategy(ABC):
    @abstractmethod
    def extract(self, data_paths: list[str]) -> list[Person]:
        pass
