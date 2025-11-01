import json
from dataclasses import asdict
from logging import getLogger
from pathlib import Path

from modules.transcriptor.src.constants import INPUT_PROMPT
from modules.transcriptor_legacy.src.jsonl.models.BatchRequest import (
    BatchRequest,
    BatchRequestBody,
)

logger = getLogger(__name__)


def create_jsonl(output_file: Path, image_data_path: Path, custom_id: str) -> None:
    logger.info(f"Reading data from {image_data_path}...")

    with open(image_data_path, "r") as f:
        base64_image = f.read().strip()

    messages = INPUT_PROMPT
    messages[0]["content"][1]["image_url"] = f"data:image/jpeg;base64,{base64_image}"
    request = BatchRequest(custom_id=custom_id, body=BatchRequestBody(input=messages))
    mode = "a" if output_file.exists() else "w"

    with open(output_file, mode) as jsonl_file:
        jsonl_file.write(json.dumps(asdict(request)) + "\n")

    logger.info(f"Wrote data to {output_file}.")
