from typing import Optional

from modules.address_books.src.repository.csv_person_repository import (
    CsvPersonRepository,
)
from modules.address_books.src.repository.db_person_repository import DbPersonRepository
from modules.shared.repository.repository import (
    Repository,
)
from modules.shared.repository.supported_file_types import (
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
