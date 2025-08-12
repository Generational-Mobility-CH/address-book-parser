from pathlib import Path


PROJECT_ROOT_PATH = Path(__file__).resolve().parents[4]
DATA_PATH = PROJECT_ROOT_PATH / "data"
PERSONS_INPUT_PATH = DATA_PATH / "address-books" / "basel"
PERSONS_OUTPUT_PATH = DATA_PATH / "parser"
