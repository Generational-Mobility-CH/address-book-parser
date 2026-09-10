"""
Transcribe address book column images using dots.ocr-1.5.

Uses year-specific tuned prompts, applies postprocessing for known
character substitutions, then converts numbered output to raw line
format compatible with the text_cleaner/text_parser pipeline.
"""
import base64
import logging
import time
from pathlib import Path

import requests

from src.transcriptor.src.api_dots_ocr.format_converter import convert_to_raw_lines
from src.transcriptor.src.api_dots_ocr.postprocessing import postprocess_raw

logger = logging.getLogger(__name__)

DOTS_OCR_MODEL = "kristaller486/dots.ocr-1.5"
_MAX_RETRIES = 3


def _encode_image(image_path: Path) -> str:
    """Base64-encode a JPEG image for the API."""
    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")


def _call_api(
    image_b64: str,
    prompt: str,
    api_key: str,
    base_url: str,
) -> str:
    """Call dots.ocr-1.5 via OpenAI-compatible chat completions API.

    Retries up to 3 times with exponential backoff on transient errors.
    Returns raw model output text.
    """
    url = f"{base_url}/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": DOTS_OCR_MODEL,
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{image_b64}"
                        },
                    },
                    {"type": "text", "text": prompt},
                ],
            }
        ],
        "max_tokens": 4096,
        "temperature": 0.0,
        "mm_processor_kwargs": {"max_pixels": 11289600},
    }

    for attempt in range(_MAX_RETRIES):
        try:
            resp = requests.post(
                url, headers=headers, json=payload, timeout=300
            )
            if resp.status_code != 200:
                error_text = resp.text
                # Some endpoints reject the temperature parameter
                if "temperature" in error_text and "temperature" in payload:
                    del payload["temperature"]
                    continue
                resp.raise_for_status()
            return resp.json()["choices"][0]["message"]["content"]
        except (
            requests.exceptions.ConnectionError,
            requests.exceptions.Timeout,
            requests.exceptions.ChunkedEncodingError,
            ConnectionResetError,
            OSError,
        ) as e:
            if attempt < _MAX_RETRIES - 1:
                wait = 2 ** (attempt + 1)
                logger.warning(
                    "API call failed (attempt %d/%d): %s. Retrying in %ds...",
                    attempt + 1,
                    _MAX_RETRIES,
                    e,
                    wait,
                )
                time.sleep(wait)
            else:
                raise

    raise RuntimeError("Unreachable: retry loop exhausted")


def transcribe_image(
    image_path: Path,
    api_key: str,
    base_url: str,
    prompt: str,
) -> str:
    """Transcribe a column image using dots.ocr-1.5.

    Returns raw text (one entry per line) ready for legacy JSON storage.
    The text has been postprocessed (character fixes) and converted
    from numbered format to raw line format.
    """
    image_b64 = _encode_image(image_path)
    raw_output = _call_api(image_b64, prompt, api_key, base_url)
    postprocessed = postprocess_raw(raw_output)
    converted = convert_to_raw_lines(postprocessed)
    return converted


def transcribe_image_raw(
    image_path: Path,
    api_key: str,
    base_url: str,
    prompt: str,
) -> tuple[str, str]:
    """Transcribe and return both raw (numbered) and converted text.

    Used by the benchmark to evaluate against GT (needs numbered format)
    while also verifying pipeline compatibility (needs converted format).

    Returns (postprocessed_numbered, converted_raw).
    """
    image_b64 = _encode_image(image_path)
    raw_output = _call_api(image_b64, prompt, api_key, base_url)
    postprocessed = postprocess_raw(raw_output)
    converted = convert_to_raw_lines(postprocessed)
    return postprocessed, converted
