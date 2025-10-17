from typing import Optional

from modules.persons_data_processor.src.repository.csv_person_repository import (
    CsvRepository,
)
from modules.persons_data_processor.src.repository.db_person_repository import (
    DbRepository,
)
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
            return DbRepository()
        case SupportedFileTypes.CSV.value:
            return CsvRepository(csv_column_names)
