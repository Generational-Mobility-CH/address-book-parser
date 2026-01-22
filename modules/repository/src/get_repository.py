from typing import Optional

from modules.repository.src.csv_person_repository import CsvPersonRepository
from modules.repository.src.db_person_repository import DbPersonRepository
from modules.repository.src.repository import (
    Repository,
)
from modules.repository.src.supported_file_types import (
    SupportedFileTypes,
)


def get_person_repository(
    output_type: SupportedFileTypes,
    csv_column_names: Optional[list[str]] = None,
) -> Repository:
    match output_type.value:
        case SupportedFileTypes.DB.value:
            return DbPersonRepository()
        case SupportedFileTypes.CSV.value:
            return CsvPersonRepository(csv_column_names)
