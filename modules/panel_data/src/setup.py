from modules.panel_data.src.common.paths import PANEL_DATA_OUTPUT_PATH
from modules.shared.common.logger import setup_logging
from modules.shared.constants.paths import DATA_PATH


def setup(time_stamp: str) -> None:
    module_directories = [
        DATA_PATH,
        PANEL_DATA_OUTPUT_PATH,
        PANEL_DATA_OUTPUT_PATH / "db",
    ]

    [directory.mkdir(parents=True, exist_ok=True) for directory in module_directories]

    setup_logging(time_stamp, PANEL_DATA_OUTPUT_PATH / "logs")
