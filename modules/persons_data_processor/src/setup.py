from modules.persons_data_processor.src.common.paths import PERSONS_OUTPUT_PATH
from modules.shared.common.logger import setup_logging
from modules.shared.constants.paths import DATA_PATH


def setup(time_stamp: str) -> None:
    module_directories = [DATA_PATH, PERSONS_OUTPUT_PATH]

    [directory.mkdir(parents=True, exist_ok=True) for directory in module_directories]

    setup_logging(time_stamp, PERSONS_OUTPUT_PATH / "logs")
