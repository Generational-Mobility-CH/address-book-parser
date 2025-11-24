import json
import os
from dataclasses import asdict
from pathlib import Path

from modules.transcriptor_legacy.src.jsonl.models.BatchRequest import BatchRequest


def write_jsonl_batch_files(input_data: list[BatchRequest], output_dir: Path) -> None:
    """
    max_file_size:
        Batch upload limit: https://platform.openai.com/docs/guides/batch/batch-api
        max_file_size = 200 MB (200 * 1024 * 1024) * 90% (reduce max size so we don't go over)
    """
    max_file_size = 188743680
    file_number = 1
    base_filename = "TODO"
    current_filename = f"{base_filename}-{file_number}.jsonl"

    for data in input_data:
        if os.path.exists(current_filename):
            file_number += 1
            current_filename = f"{base_filename}-{file_number}.jsonl"

        with open(current_filename, "a+") as file:
            file.write(json.dumps(asdict(data)) + "\n")

        if os.path.getsize(current_filename) > max_file_size:
            previous_file_number = file_number - 1
            if previous_file_number > 0:
                previous_filename = f"{base_filename}-{previous_file_number}.jsonl"
                with open(previous_filename, "r") as previous_file:
                    previous_data = previous_file.read()

                new_filename = f"{base_filename}-{file_number}.jsonl"
                with open(new_filename, "w") as new_file:
                    new_file.write(previous_data)
