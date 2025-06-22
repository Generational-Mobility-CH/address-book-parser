import logging
import os
from enum import Enum
from typing import List, TypeVar

from modules.persons_cleaner.src.load.db.to_db import save_to_db
from modules.persons_cleaner.src.load.to_csv import save_to_csv

T = TypeVar("T")

class SupportedOutputFileTypes(Enum):
    CSV = "csv"
    DB = "db"


logger = logging.getLogger(__name__)


def save_data(
    input_data: List[T],
    output_file_path: str,
    output_file_type: SupportedOutputFileTypes,
) -> None:
    if not input_data:
        logger.error("Input data list is empty.")
        return

    os.makedirs(os.path.dirname(output_file_path), exist_ok=True)

    match output_file_type:
        case SupportedOutputFileTypes.CSV:
            save_to_csv(input_data, output_file_path)
        case SupportedOutputFileTypes.DB:
            save_to_db(input_data, output_file_path)
        case _:
            logger.error(f"Unsupported output file type: {output_file_type}")