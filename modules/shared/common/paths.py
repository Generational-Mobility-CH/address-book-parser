from pathlib import Path


PROJECT_ROOT_PATH = Path(__file__).resolve().parents[3]


CITY = "Basel"

DATA_PATH = PROJECT_ROOT_PATH / "data" / CITY
INPUT_PATH = DATA_PATH / "transcriptions" / "legacy_json"
OUTPUT_PATH = DATA_PATH / "db"
