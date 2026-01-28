from modules.pages_preprocessor.src.paths import JPG_INPUT_PATH, JPG_OUTPUT_PATH
from modules.shared.common.paths import DATA_PATH
from modules.shared.constants.years_range import YEARS_RANGE


def setup() -> None:
    years: list = [1877, 1880] + list(YEARS_RANGE)

    module_directories = [
        DATA_PATH,
        *(JPG_INPUT_PATH / "person_register" / f"Basel_{year}" for year in years),
        *(JPG_OUTPUT_PATH / "person_register" / f"Basel_{year}" for year in years),
    ]

    [directory.mkdir(parents=True, exist_ok=True) for directory in module_directories]
