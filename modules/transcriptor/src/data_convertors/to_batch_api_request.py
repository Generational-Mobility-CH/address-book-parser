import base64
import binascii
from datetime import datetime

from modules.transcriptor.src.constants.prompt import INPUT_PROMPT
from modules.transcriptor.src.data_convertors.exceptions.data_convertor_exception import (
    DataConvertorException,
)
from modules.transcriptor.src.model.BacthRequest import BatchRequest, BatchRequestBody


def _is_base_64_encoded(data: str) -> bool:
    try:
        base64.b64decode(data, validate=True)
    except binascii.Error:
        return False

    return True


def to_batch_api_request(base64_image: str, custom_id: str) -> BatchRequest:
    if not _is_base_64_encoded(base64_image):
        raise DataConvertorException(
            "Error: the provided string is not a valid base64 encoded image"
        )

    custom_id = f"{custom_id}-<{datetime.now():%b%d%H%M%S}>"
    messages = INPUT_PROMPT
    messages[0]["content"][1]["image_url"] = f"data:image/jpeg;base64,{base64_image}"
    request = BatchRequest(custom_id=custom_id, body=BatchRequestBody(input=messages))

    return request
