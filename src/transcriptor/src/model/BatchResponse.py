from dataclasses import dataclass
from typing import Optional, Any, Union

from pydantic import BaseModel


@dataclass
class MessageOutputContent(BaseModel):
    type: str
    annotations: list[Any]
    logprobs: list[Any]
    text: str


@dataclass
class ReasoningOutput(BaseModel):
    id: str
    summary: list[Any]
    type: str = "reasoning"


@dataclass
class MessageOutput(BaseModel):
    id: str
    status: str
    content: list[MessageOutputContent]
    role: str
    type: str = "message"


OutputType = Union[ReasoningOutput, MessageOutput]


@dataclass
class Body(BaseModel):
    id: str
    object: str
    created_at: int
    status: str
    background: bool
    billing: Any
    error: Optional[Any]
    incomplete_details: Optional[Any]
    instructions: Optional[Any]
    max_output_tokens: Optional[int]
    max_tool_calls: Optional[int]
    model: str
    output: list[OutputType]
    parallel_tool_calls: bool
    previous_response_id: Optional[str]
    prompt_cache_key: Optional[str]
    prompt_cache_retention: Optional[Any]
    reasoning: Any
    safety_identifier: Optional[Any]
    service_tier: str
    store: bool
    temperature: float
    text: dict
    tool_choice: str
    tools: list[Any]
    top_logprobs: int
    top_p: float
    truncation: str
    usage: Any
    user: Optional[Any]
    metadata: dict


@dataclass
class Response(BaseModel):
    status_code: int
    request_id: str
    body: Body


@dataclass
class BatchResponse(BaseModel):
    id: str
    custom_id: str
    response: Response
    error: Optional[Any]
