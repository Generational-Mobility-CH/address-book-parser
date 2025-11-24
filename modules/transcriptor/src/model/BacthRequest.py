from dataclasses import dataclass

from modules.transcriptor.src.constants.openai_api import MODEL_NAME, API_ENDPOINT


@dataclass
class BatchRequestBody:
    input: list[dict]
    model: str = MODEL_NAME


@dataclass
class BatchRequest:
    custom_id: str
    body: BatchRequestBody
    method: str = "POST"
    url: str = API_ENDPOINT
