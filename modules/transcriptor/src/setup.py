from datetime import datetime
from pathlib import Path

from modules.shared.common.logger import setup_logging
from modules.shared.constants.paths import DATA_PATH


def setup(module_directories: list[Path]) -> None:
    [directory.mkdir(parents=True, exist_ok=True) for directory in module_directories]

    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    setup_logging(f"transcriptor-{timestamp}", DATA_PATH / "logs")
