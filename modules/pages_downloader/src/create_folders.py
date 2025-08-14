from modules.pages_downloader.src.constants.paths import (
    JSON_OUTPUT_PATH,
    JPG_OUTPUT_PATH,
)


def create_folders() -> None:
    for year in range(1883, 1954):
        (JSON_OUTPUT_PATH / f"Basel_{year}").mkdir(parents=True, exist_ok=True)
        (JPG_OUTPUT_PATH / f"Basel_{year}").mkdir(parents=True, exist_ok=True)
