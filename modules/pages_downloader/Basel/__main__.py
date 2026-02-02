from pathlib import Path

from modules.pages_downloader.Basel.constants.paths import (
    ALL_BOOK_LINKS_FILE,
    TEST_BOOK_LINK_FILE,
)
from modules.pages_downloader.Basel.constants.urls import (
    BASEL_ADRESS_BOOKS_OVERVIEW_URLS,
)
from modules.pages_downloader.Basel.download_entire_book_pdfs import (
    download_all_pdfs,
)
from modules.pages_downloader.Basel.webscraper.extract_books_urls import (
    extract_books_urls_from_overview,
)
from modules.pages_downloader.Basel.webscraper.extract_content_tables import (
    write_jsons_with_table_of_content,
)
from modules.pages_downloader.Basel.setup import setup
from modules.pages_downloader.Basel.webscraper.render_book_pdfs import render_book_pdfs


def main(list_of_urls: Path = ALL_BOOK_LINKS_FILE) -> None:
    extract_books_urls_from_overview(
        urls_collection=BASEL_ADRESS_BOOKS_OVERVIEW_URLS, test_case=1917
    )
    write_jsons_with_table_of_content(list_of_urls)
    render_book_pdfs(list_of_urls)  ## rendering only needs to be run once
    download_all_pdfs(list_of_urls)


if __name__ == "__main__":
    setup()
    working_example = TEST_BOOK_LINK_FILE
    main(list_of_urls=working_example)
