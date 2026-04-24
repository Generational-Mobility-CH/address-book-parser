# Use this file to download all residents registry from the Bern city archive website
import re
from datetime import datetime
from logging import getLogger

from src.pages_downloader.Bern.constants import (
    URL_ARCHIVE_BERN,
    URL_BASE,
    IS_ADDRESS_BOOK_LINK,
    IS_YEAR_OR_YEAR_RANGE,
)
from src.pages_downloader.Bern.download_file import download_file
from src.pages_downloader.Bern.get_all_page_links import get_all_links
from src.pages_downloader.Bern.model.BookLink import BookLink
from src.setup import setup
from src.shared.common.paths import DATA_PATH

_logger = getLogger(__name__)


if __name__ == "__main__":
    book_links: list[BookLink] = []
    output_dir = DATA_PATH / "pdf"
    already_downloaded = [file.name for file in output_dir.glob("*.pdf")]

    setup(f"{datetime.now():%b %d - %H%M}", [output_dir])

    for link in get_all_links(URL_ARCHIVE_BERN):
        address_book_url = link.get("href")
        link_text = link.text.lower()

        if not re.search(IS_ADDRESS_BOOK_LINK, link_text):
            continue

        found_year = re.search(IS_YEAR_OR_YEAR_RANGE, link_text)
        if not found_year:
            continue

        year = found_year.group()

        if any(year in name for name in already_downloaded):
            _logger.info(f"Skipping year '{year}' (already downloaded)...")
            continue

        _logger.info(f"Searching for download link for year '{year}'...")

        for next_link in get_all_links(address_book_url):
            if "einwohner" not in next_link.text.lower():
                continue

            residents_register_url = f"{URL_BASE}{next_link.get('href')}"
            for pdf_link in get_all_links(residents_register_url):
                if pdf_link.get("title") == "PDF":
                    book_links.append(
                        BookLink(
                            year=year,
                            residents_register_pdf_url=f"{URL_BASE}{pdf_link.get('href')}",
                        )
                    )
                    _logger.info(
                        f"Found download link for year '{year}' and added it to the list"
                    )
                    break

    for book in book_links:
        pdf_name = f"Bern-{book.year}.pdf"
        download_file(book.residents_register_pdf_url, output_dir / pdf_name)
        _logger.info(f"Downloaded file '{output_dir / pdf_name}'")

    _logger.info("Finished downloading files.")
