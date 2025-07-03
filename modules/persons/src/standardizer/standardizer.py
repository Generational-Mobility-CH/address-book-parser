from abc import ABC, abstractmethod


class Standardizer(ABC):
    @abstractmethod
    def standardize(self, value: str) -> str:
        pass
