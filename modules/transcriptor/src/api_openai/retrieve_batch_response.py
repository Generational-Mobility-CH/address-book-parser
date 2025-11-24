from logging import getLogger

from openai import OpenAI

from modules.transcriptor.src.model.BatchResponse import BatchResponse

_logger = getLogger(__name__)


def retrieve_batch_response(batch_id: str, client: OpenAI) -> BatchResponse | None:
    batch_id = batch_id.strip()

    _logger.info(f"Retrieving batch file with id '{batch_id}'...")
    batch = client.batches.retrieve(batch_id)
    _logger.info(f"Successfully retrieved batch file with id '{batch_id}'")

    if not (file_id := batch.output_file_id):
        _logger.error(
            f"Batch '{batch_id}' was not processed. Error file id='{batch.error_file_id}'"
        )
        return None

    _logger.info(f"Retrieving file with id '{file_id}'...")
    file_response = client.files.content(file_id)
    _logger.info(f"Successfully retrieved file with id '{file_id}'")

    return file_response
