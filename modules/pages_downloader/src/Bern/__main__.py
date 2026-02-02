# Use this file to download all residents registry from the Bern city archive website

import re

from modules.pages_downloader.src.Bern.constants import (
    URL_ARCHIVE_BERN,
    URL_BASE,
    IS_ADDRESS_BOOK_LINK,
    IS_REGISTRY_LINK,
    IS_YEAR_OR_YEAR_RANGE,
)
from modules.pages_downloader.src.Bern.download_file import download_file
from modules.pages_downloader.src.Bern.get_all_page_links import get_all_links
from modules.pages_downloader.src.model.BookLink import BookLink
from modules.shared.common.paths import PROJECT_ROOT_PATH

if __name__ == "__main__":
    book_links: list[BookLink] = []
    output_dir_bern = PROJECT_ROOT_PATH / "Bern" / "pdf"

    for link in get_all_links(URL_ARCHIVE_BERN):
        link_text = link.text.lower()
        if not re.search(IS_ADDRESS_BOOK_LINK, link_text):
            continue

        found_year = re.search(IS_YEAR_OR_YEAR_RANGE, link_text)
        if not found_year:
            continue

        year = found_year.group()
        address_book_url = link.get("href")
        for next_link in get_all_links(address_book_url):
            if not re.search(IS_REGISTRY_LINK, next_link.text.lower()):
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
                    break

    for book in book_links:
        pdf_name = f"Bern-{book.year}.pdf"
        download_file(book.residents_register_pdf_url, output_dir_bern / pdf_name)
