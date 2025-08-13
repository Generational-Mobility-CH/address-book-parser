import json
import random
import time

from selenium.webdriver.support.ui import WebDriverWait

from modules.address_books.pages_downloader.src.common.driver import (
    get_web_driver,
    default_options,
)
from modules.address_books.pages_downloader.src.constants.paths import (
    PDF_OUTPUT_PATH,
    ALL_BOOK_LINKS_FILE,
)
from modules.address_books.pages_downloader.src.extract_content_tables import click_btn


def render_book_pdf(book_url: str) -> str | None:
    retries = 1
    wait_time = 30
    options = default_options.remove_argument(
        "--headless=new"
    )  # TODO: check if this remove method is really available

    for attempt in range(retries):
        driver = get_web_driver(options)
        try:
            driver.get(book_url)
            WebDriverWait(driver, wait_time)

            click_btn(driver, "-export")
            click_btn(driver, "Export as PDF")
            print("[✓] Successfully triggered PDF export")
            return "clicked"

        except Exception as e:
            print(f"[Attempt {attempt}] failed to get PDF from {book_url}: {e}")
            if attempt == retries - 1:
                return None
            time.sleep(random.uniform(2, 6))
        finally:
            time.sleep(3)  # give time to visually check in non-headless mode

    return None


if __name__ == "__main__":
    with open(ALL_BOOK_LINKS_FILE, "r", encoding="utf-8") as f:
        books_urls = json.load(f)

    for item in books_urls:
        book_year = item[0][0]
        book_url = item[1]

        if not (PDF_OUTPUT_PATH / f"Basel_{book_year}.pdf").exists():
            render_book_pdf(book_url)
