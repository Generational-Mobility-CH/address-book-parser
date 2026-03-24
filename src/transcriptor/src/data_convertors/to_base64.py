from base64 import b64encode
from pathlib import Path


def to_base64(image_path: Path) -> str:
    with open(image_path, "rb") as image_file:
        return b64encode(image_file.read()).decode("utf-8")
