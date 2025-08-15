import json


def read_json(file_path: str) -> list[dict] | dict:
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)
