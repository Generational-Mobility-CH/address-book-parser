import json
from logging import getLogger
from pathlib import Path

from pydantic import ValidationError

from modules.transcriptor_legacy.src.model.batch_response_jsonl import MessageOutput
from modules.transcriptor.src.model.BacthRequest import BatchRequest

_logger = getLogger(__name__)


def extract_response_text(file: Path) -> str | None:
    with open(file, "r") as f:
        lines = f.readlines()

    msg_output_collection: list[MessageOutput] = []
    for line in lines:
        obj = json.loads(line)
        try:
            obj = BatchRequest.model_validate(obj)
            if obj.response.body.status == "completed":
                msg_output_collection.extend(
                    o for o in obj.response.body.output if o.type == "message"
                )
        except ValidationError as e:
            _logger.error(f"Validation error: '{e} 'for line '{line}'")

        return "\n".join(msg.content[0].text for msg in msg_output_collection)
