import json
from dataclasses import asdict
from pathlib import Path
from typing import Optional

from charset_normalizer.md import getLogger

from modules.shared.common.paths import CITY
from modules.transcriptor.src.model.BacthRequest import BatchRequest

_logger = getLogger(__name__)


def write_batch_files(
    requests_collection: list[BatchRequest],
    output_dir: Path,
    year: Optional[str] = None,
) -> None:
    """
    max_file_size:
        Batch upload limit: https://platform.openai.com/docs/guides/batch/batch-api
        max_file_size = 200 MB (200 * 1024 * 1024) * 90% (reduce max size so we don't go over)
    """
    max_file_size = 188743680
    current_file = None
    file_counter = 0
    temp_file = Path(".") / "temp_file.jsonl"

    for request in requests_collection:
        temp_file.open("w").write(json.dumps(asdict(request)) + "\n")
        next_file_size = temp_file.stat().st_size

        if next_file_size > max_file_size:
            _logger.warning(
                f"Skipping file with custom_id={request.custom_id}. Reason: File size bigger than limit"
            )
            continue

        if current_file is None or (
            current_file.stat().st_size + next_file_size > max_file_size
        ):
            file_counter += 1
            current_file = output_dir / f"{CITY}_{year}-{file_counter}.jsonl"

        current_file.open("a+").write(json.dumps(asdict(request)) + "\n")

    temp_file.unlink(missing_ok=True)
