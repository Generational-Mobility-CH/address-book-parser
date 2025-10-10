from typing import Optional

from modules.persons_data_processor.src.repository.csv_person_repository import (
    CsvPersonRepository,
)
from modules.persons_data_processor.src.repository.db_person_repository import (
    DbPersonRepository,
)
from modules.persons_data_processor.src.repository.person_repository import (
    PersonRepository,
)
from modules.persons_data_processor.src.repository.supported_file_types import (
    SupportedFileTypes,
)


def get_person_repository(
    output_type: SupportedFileTypes,
    csv_column_names: Optional[list[str]] = None,
) -> PersonRepository:
    match output_type.value:
        case SupportedFileTypes.DB.value:
            return DbPersonRepository()
        case SupportedFileTypes.CSV.value:
            return CsvPersonRepository(csv_column_names)
