import csv
import json
import os
import re
from logging import getLogger
from pathlib import Path

from openai import OpenAI
from pydantic import ValidationError

from modules.shared.common.config import config_instance
from modules.shared.constants.paths import DATA_PATH, CITY
from modules.transcriptor.src.api_openai.create_batch_jobs import create_batch_jobs
from modules.transcriptor.src.api_openai.retrieve_batch_response import (
    retrieve_batch_response,
)
from modules.transcriptor.src.api_openai.write_batch_files import write_batch_files
from modules.transcriptor.src.data_convertors.to_batch_api_request import (
    to_batch_api_request,
)
from modules.transcriptor.src.model.BacthRequest import BatchRequest
from modules.transcriptor.src.model.BatchResponse import BatchResponse
from modules.transcriptor.src.setup import setup

_logger = getLogger(__name__)


def extract_relevant_text(data_input_dir: Path, data_output_dir: Path) -> None:
    for file in data_input_dir.glob("*.jsonl"):
        with open(file, "r") as f:
            lines = f.readlines()

        for line in lines:
            obj = json.loads(line)
            try:
                obj = BatchResponse.model_validate(obj)

                match = re.search(r"-(\d{4})-", obj.custom_id)
                year = match.group(1) if match else "NO_YEAR_FOUND"
                out_dir = data_output_dir / f"{CITY}_{year}"
                out_dir.mkdir(parents=True, exist_ok=True)

                if obj.response.body.status == "completed":
                    for o in obj.response.body.output:
                        if o.type == "message":
                            file_name_without_timestamp = re.sub(
                                r"-[^-]*$", "", obj.custom_id
                            )
                            output_file = out_dir / f"{file_name_without_timestamp}.txt"
                            with open(
                                output_file, mode="w", newline="", encoding="utf-8"
                            ) as text_output_file:
                                text_output_file.write(o.content[0].text)
                                _logger.info(f"Wrote '{output_file}'")

            except ValidationError as e:
                _logger.error(f"Validation error: '{e} 'for line '{line}'")


def extract_persons(data_input_dir: Path, data_output_dir: Path) -> None:
    for file in data_input_dir.glob("**/*.txt"):
        with open(file, "r") as f:
            lines = f.readlines()

        persons = []
        for line in lines:
            row = line.strip().split(";")
            persons.append(row)

        match = re.search(r"\d{4}", file.parent.name)
        year = match.group(0) if match else "NO_YEAR_FOUND"
        out_dir = data_output_dir / f"{CITY}_{year}"
        out_dir.mkdir(parents=True, exist_ok=True)

        file_name = out_dir / f"{file.stem}.csv"
        with open(file_name, "w", encoding="utf-8") as f:
            writer = csv.writer(f, delimiter=";")
            for person in persons:
                writer.writerow(person)
        _logger.info(f"Wrote persons to {file_name}")


if __name__ == "__main__":
    base64_dir = DATA_PATH / "base64"
    jsonl_dir = DATA_PATH / "jsonl"
    transcriptions_dir = DATA_PATH / "transcriptions"

    setup([DATA_PATH, base64_dir, jsonl_dir, transcriptions_dir])

    client = OpenAI()
    os.environ["OPENAI_API_KEY"] = config_instance.openai_api_key

    # base64 -> jsonl
    for book in base64_dir.iterdir():
        all_requests: list[BatchRequest] = []
        year = (
            re.search(r"\d{4}", book.name).group(0)
            if re.search(r"\d{4}", book.name)
            else None
        )

        if year and int(year) in range(1922, 1950):
            for page in book.iterdir():
                base64_image = page.open().read()
                all_requests.append(
                    to_batch_api_request(base64_image, f"{CITY}-{year}-{page.stem}")
                )

        write_batch_files(all_requests, jsonl_dir, year)

    for batch in jsonl_dir.glob("*.jsonl"):
        create_batch_jobs(batch, client)

    # get responses
    batch_ids_file = (
        DATA_PATH / "transcriptions" / "batch_ids" / "batch_ids-1922-1949.txt"
    )
    for batch_id in batch_ids_file.open("r").readlines():
        if response := retrieve_batch_response(batch_id, client):
            (transcriptions_dir / "jsonl" / f"output-{batch_id}.jsonl").open("w").write(
                response.text
            )
            _logger.info(
                f"Successfully wrote output for batch with id='{batch_id}' under f'{transcriptions_dir}'"
            )

    extract_relevant_text(transcriptions_dir / "jsonl", transcriptions_dir / "text")
    extract_persons(transcriptions_dir / "text", transcriptions_dir / "persons")
