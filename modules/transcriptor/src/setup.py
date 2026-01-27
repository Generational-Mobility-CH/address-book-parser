from pathlib import Path

from modules.shared.common.logger import setup_logging
from modules.shared.common.paths import DATA_PATH


def setup(module_directories: list[Path], timestamp: str) -> None:
    [directory.mkdir(parents=True, exist_ok=True) for directory in module_directories]

    setup_logging(f"transcriptor-{timestamp}", DATA_PATH / "logs")
