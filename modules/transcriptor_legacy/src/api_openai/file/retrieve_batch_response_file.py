from logging import getLogger

from openai import OpenAI

_logger = getLogger(__name__)


def retrieve_batch_response_file(id: str, api_client: OpenAI):  # TODO: add return type
    _logger.info(f"Retrieving batch file with id '{id}'...")
    batch = api_client.batches.retrieve(id)
    _logger.info(f"Successfully retrieved batch file with id '{id}'")

    file_id = batch.output_file_id
    _logger.info(f"Retrieving file with id '{file_id}'...")
    file_response = api_client.files.content(file_id)
    _logger.info(f"Successfully retrieved file with id '{file_id}'")

    return file_response
