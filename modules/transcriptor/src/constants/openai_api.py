from typing import Literal


Endpoint = Literal[
    "/v1/responses",
    "/v1/chat/completions",
    "/v1/embeddings",
    "/v1/completions",
]

API_ENDPOINT: Endpoint = "/v1/responses"

MODEL_NAME = "gpt-5-mini"
