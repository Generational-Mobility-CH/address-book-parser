import csv
import json
import os
import re
from datetime import datetime
from pathlib import Path

from openai import OpenAI
from pydantic import ValidationError
from structlog import getLogger
from tenacity import retry, stop_after_attempt, wait_exponential

from modules.shared.common.config import config_instance
from modules.shared.constants.paths import DATA_PATH, CITY
from modules.transcriptor.src.constants.openai_api import API_ENDPOINT
from modules.transcriptor.src.model.BacthRequest import BatchRequest
from modules.transcriptor_legacy.src.setup import setup

_logger = getLogger(__name__)


@retry(stop=stop_after_attempt(5), wait=wait_exponential(multiplier=1, min=2, max=10))
def upload_file(file: Path) -> str:
    with open(file, "rb") as f:
        batch_input_file = client.files.create(file=f, purpose="batch", timeout=3000)

    return batch_input_file.id


def create_batch_jobs(input_data: Path, output_file: Path) -> None:
    for file in input_data.iterdir():
        if file.suffix == ".jsonl":
            _logger.info(f"Uploading batch file '{file.name}'...")
            batch_input_file_id = upload_file(file)
            _logger.info(f"Finished uploading {file.name}.")

            _logger.info(f"Creating batch job for {file.name}...")
            batch = client.batches.create(
                input_file_id=batch_input_file_id,
                endpoint=API_ENDPOINT,
                completion_window="24h",
                metadata={"description": f"batch-basel-{datetime.now():%b_%d_%H%M%S}"},
            )
            _logger.info(f"Finished creating batch job for {file.name}.")

            with open(output_file, "a") as f:
                f.write(batch.id + "\n")
            _logger.info(f"Wrote 'batch_id'={batch.id} in {output_file}.")


def save_batch_output_file(data_input_dir: Path, data_output_dir: Path) -> None:
    with open(data_input_dir, "r") as f:
        for batch_id in f.readlines():
            batch_id = batch_id.strip()

            _logger.info(f"Retrieving batch file with id '{batch_id}'...")
            batch = client.batches.retrieve(batch_id)
            _logger.info(f"Successfully retrieved batch file with id '{batch_id}'")

            if not (file_id := batch.output_file_id):
                error_file_id = batch.error_file_id
                _logger.warning(
                    f"Batch '{batch_id}' was not processed. Error file id='{error_file_id}'"
                )
                continue

            _logger.info(f"Retrieving file with id '{file_id}'...")
            file_response = client.files.content(file_id)
            _logger.info(f"Successfully retrieved file with id '{file_id}'")

            batch_output_file = data_output_dir / f"batch_output-{batch_id}.jsonl"
            with open(batch_output_file, "w") as output_file:
                output_file.write(file_response.text)
            _logger.info(
                f"Successfully wrote batch file output to '{batch_output_file}'"
            )


def extract_relevant_text(data_input_dir: Path, data_output_dir: Path) -> None:
    for file in data_input_dir.iterdir():
        if file.suffix == ".jsonl":
            with open(file, "r") as f:
                lines = f.readlines()

            for line in lines:
                obj = json.loads(line)
                try:
                    obj = BatchRequest.model_validate(obj)

                    match = re.search(r"\d{4}", obj.custom_id)
                    year = match.group(0) if match else "NO_YEAR_FOUND"
                    out_dir = data_output_dir / f"{CITY}_{year}"
                    out_dir.mkdir(parents=True, exist_ok=True)

                    if obj.response.body.status == "completed":
                        for o in obj.response.body.output:
                            if o.type == "message":
                                output_file = out_dir / f"{obj.custom_id}.txt"
                                with open(
                                    output_file, mode="w", newline="", encoding="utf-8"
                                ) as file:
                                    file.write(o.content[0].text)

                except ValidationError as e:
                    _logger.error(f"Validation error: '{e} 'for line '{line}'")


def extract_persons(data_input_dir: Path, data_output_dir: Path) -> None:
    for file in data_input_dir.iterdir():
        if file.is_dir():
            txt_files = list(file.glob("*.txt"))
            for txt_file in txt_files:
                with open(txt_file, "r") as f:
                    lines = f.readlines()
                persons = []
                for line in lines:
                    try:
                        row = line.strip().split(";")
                        persons.append(row)
                    except SyntaxError:
                        _logger.error(f"Syntax error: '{line}'")
                    except ValueError:
                        _logger.error(f"Value error: '{line}'")

                match = re.search(r"\d{4}", file.name)
                year = match.group(0) if match else "NO_YEAR_FOUND"
                out_dir = data_output_dir / f"{CITY}_{year}"
                out_dir.mkdir(parents=True, exist_ok=True)

                file_name = out_dir / f"{txt_file.stem}.csv"
                with open(file_name, "w", encoding="utf-8") as f:
                    writer = csv.writer(f, delimiter=";")
                    for person in persons:
                        writer.writerow(person)


if __name__ == "__main__":
    client = OpenAI()
    os.environ["OPENAI_API_KEY"] = config_instance.openai_api_key
    setup(f"transcriptor-{datetime.now():%b_%d_%H%M%S}", [])

    # create_batch_jobs(DATA_PATH / "jsonl", DATA_PATH / "transcriptions" / "batch_ids" / "batch_ids.txt")
    # save_batch_output_file(DATA_PATH / "transcriptions" / "batch_ids" / "batch_ids.txt", DATA_PATH / "transcriptions" / "jsonl")
    extract_relevant_text(
        DATA_PATH / "transcriptions" / "jsonl", DATA_PATH / "transcriptions" / "text"
    )
    extract_persons(
        DATA_PATH / "transcriptions" / "text", DATA_PATH / "transcriptions" / "persons"
    )
