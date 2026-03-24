from src.pages_downloader.Basel.constants.paths import (
    JSON_OUTPUT_PATH,
    JPG_OUTPUT_PATH,
    GENERAL_INPUT_PATH,
    GENERAL_OUTPUT_PATH,
    PDF_INPUT_PATH,
    JSON_INPUT_PATH,
)

from src.pages_preprocessor.src.paths import PDF_OUTPUT_PATH
from src.shared.common.paths import DATA_PATH
from src.shared.constants.years_range import YEARS_RANGE


def setup() -> None:
    module_directories = [
        DATA_PATH,
        GENERAL_INPUT_PATH,
        GENERAL_OUTPUT_PATH,
        PDF_INPUT_PATH,
        PDF_OUTPUT_PATH,
        JSON_INPUT_PATH,
        JSON_OUTPUT_PATH,
        JPG_OUTPUT_PATH,
        *((JSON_OUTPUT_PATH / f"Basel_{year}") for year in YEARS_RANGE),
        *((JPG_OUTPUT_PATH / f"Basel_{year}") for year in YEARS_RANGE),
        JSON_OUTPUT_PATH / "toc",
    ]

    [directory.mkdir(parents=True, exist_ok=True) for directory in module_directories]


if __name__ == "__main__":
    setup()
