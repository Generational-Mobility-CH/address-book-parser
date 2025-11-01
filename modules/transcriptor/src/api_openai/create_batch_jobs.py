from datetime import datetime
from logging import getLogger
from pathlib import Path

from openai import OpenAI
from tenacity import retry, stop_after_attempt, wait_exponential

from modules.shared.constants.paths import CITY
from modules.transcriptor.src.constants.openai_api import API_ENDPOINT

_logger = getLogger(__name__)


@retry(stop=stop_after_attempt(5), wait=wait_exponential(multiplier=1, min=2, max=10))
def _upload_file(file: Path, api_client: OpenAI) -> str:
    with open(file, "rb") as f:
        _logger.info(f"Uploading batch file '{file.name}'...")
        batch_input_file = api_client.files.create(
            file=f, purpose="batch", timeout=3000
        )
    _logger.info(f"Finished uploading {file.name}.")

    return batch_input_file.id


def create_batch_jobs(file: Path, api_client: OpenAI) -> None:
    batch_input_file_id = _upload_file(file, api_client)
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")

    _logger.info(f"Creating batch job for {file.name}...")
    batch = api_client.batches.create(
        input_file_id=batch_input_file_id,
        endpoint=API_ENDPOINT,
        completion_window="24h",
        metadata={"description": f"batch-{CITY}-{timestamp}"},
    )
    _logger.info(f"Finished creating batch job for {file.name}.")
    # TODO: change file name after testing
    batch_ids_file = (
        file.parent.parent / "transcriptions" / "batch_ids" / "batch_ids-1922-1949.txt"
    )
    batch_ids_file.open("a+").write(batch.id + "\n")
    _logger.info(f"Stored batch_id='{batch.id}' in file='{batch_ids_file}'")
