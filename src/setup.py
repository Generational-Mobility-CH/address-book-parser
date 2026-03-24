from pathlib import Path

from src.shared.common.logger import setup_logging
from src.shared.common.paths import DATA_PATH


def setup(time_stamp: str, needed_directories: list[Path]) -> None:
    [directory.mkdir(parents=True, exist_ok=True) for directory in needed_directories]

    setup_logging(time_stamp, DATA_PATH / "logs")
