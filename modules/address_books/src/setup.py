from modules.address_books.src.common.paths import ADDRESS_BOOK_ENTRIES_OUTPUT_PATH
from modules.shared.common.logger import setup_logging
from modules.shared.constants.paths import DATA_PATH


def setup(time_stamp: str) -> None:
    module_directories = [DATA_PATH, ADDRESS_BOOK_ENTRIES_OUTPUT_PATH]

    [directory.mkdir(parents=True, exist_ok=True) for directory in module_directories]

    setup_logging(time_stamp, ADDRESS_BOOK_ENTRIES_OUTPUT_PATH / "logs")
