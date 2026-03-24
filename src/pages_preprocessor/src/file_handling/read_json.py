import json
from pathlib import Path


def read_json(file_path: Path) -> list[dict] | dict:
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)
