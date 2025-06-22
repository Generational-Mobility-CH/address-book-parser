import logging
from enum import Enum
from typing import List, TypeVar

from modules.persons_parser.src.load.to_csv import save_to_csv

T = TypeVar("T")

class OutputFileType(Enum):
    CSV = "csv"


logger = logging.getLogger(__name__)


def save_data(
    input_data: List[T],
    output_file_path: str,
    output_file_type: OutputFileType,
) -> None:
    if not input_data:
        logger.error(f"Input data list is empty for '{output_file_path}'")
        return

    if output_file_type == OutputFileType.CSV:
        save_to_csv(input_data, output_file_path)
    else:
        raise NotImplementedError(f"Unsupported output file type: {output_file_type}")
