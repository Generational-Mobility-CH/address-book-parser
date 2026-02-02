import json
import re
from pathlib import Path

import requests

from modules.pages_downloader.Basel.constants.paths import (
    PDF_OUTPUT_PATH,
    ALL_BOOK_LINKS_FILE,
    PDF_INPUT_PATH,
)
from modules.pages_downloader.Basel.constants.urls import (
    PDF_DOWNLOAD_BASE_URL,
)


def download_one_pdf(year: int, book_id: str) -> None:
    book_id = book_id.replace("/", "-")
    book_download_url = f"{PDF_DOWNLOAD_BASE_URL}/{book_id}.pdf"
    output_path = PDF_INPUT_PATH / f"Basel_{year}.pdf"

    response = requests.get(book_download_url)

    if response.status_code == 200:
        with open(output_path, "wb") as output_file:
            output_file.write(response.content)
    else:
        print(
            f"Failed to download PDF file from {year} {book_download_url}. Status code: {response.status_code}"
        )


def get_book_id_from_url(text: str) -> str:
    result = re.search(r"\d+/\d+", text).group()

    if not result:
        raise ValueError(f"Couldn't find a match for text: {text}")

    return result


def download_all_pdfs(list_of_urls: Path = ALL_BOOK_LINKS_FILE) -> None:
    with open(list_of_urls, "r", encoding="utf-8") as f:
        books_urls = json.load(f)

    for item in books_urls:
        book_year = item[0][0]
        book_url = item[1]

        if not (PDF_OUTPUT_PATH / f"Basel_{book_year}.pdf").exists():
            book_id = get_book_id_from_url(book_url)
            download_one_pdf(book_year, book_id)
