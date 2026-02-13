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


def prepare_data(data: list) -> list:
    return [
        {
            key: " ".join(val.strip().split()).title() if isinstance(val, str) else val
            for key, val in entry.__dict__.items()
        }
        if hasattr(entry, "__dict__")
        else entry
        for entry in data
    ]
