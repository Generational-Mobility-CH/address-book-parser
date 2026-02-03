from abc import abstractmethod, ABC
from pathlib import Path
from typing import TypeVar, Optional

T = TypeVar("T")


class Repository(ABC):
    @abstractmethod
    def save(self, data: list[T], output_path: Path) -> None:
        pass

    @abstractmethod
    def get_table_entries(
        self, db_path: Path, table_name: str, entries_filter: Optional[str] = None
    ) -> list[T]:
        pass
