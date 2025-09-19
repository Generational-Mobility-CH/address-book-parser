import json
from pathlib import Path

from modules.pages_downloader.src.common.driver import (
    get_web_driver,
)
from modules.pages_downloader.src.constants.paths import (
    PDF_OUTPUT_PATH,
    ALL_BOOK_LINKS_FILE,
)
from modules.pages_downloader.src.webscraper.extract_content_tables import click_btn
from typing import Optional, Literal
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


WAIT_TIME = 30
RENDER_SUCCESS_TIMEOUT = 900
ALREADY_READY_TIMEOUT = 15

SNACKBAR_ACTIVE = "[data-testid='snackbar-container'].v-snack--active"
SNACKBAR_SUCCESS = "[data-testid='snackbar-container'][data-severity='SUCCESS']"
SNACKBAR_CONTENT = f"{SNACKBAR_ACTIVE} .v-alert__content"
SNACKBAR_PDF_LINK = f"{SNACKBAR_CONTENT} a[href*='iiif-pdf-derivatives']"


def trigger_pdf_export_button(
    book_url: str,
) -> Optional[Literal["rendering", "already-ready"]]:
    driver = get_web_driver(headless=False)
    try:
        driver.get(book_url)

        WebDriverWait(driver, WAIT_TIME).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "button.tify-header-button")
            )
        )

        click_btn(driver, "-export")
        before_handles = driver.window_handles[:]  # for new-window detection
        old_url = driver.current_url

        click_btn(driver, "Export als PDF")

        try:
            WebDriverWait(driver, 12).until(
                EC.any_of(
                    EC.visibility_of_element_located(
                        (By.CSS_SELECTOR, SNACKBAR_ACTIVE)
                    ),
                    EC.new_window_is_opened(before_handles),
                    EC.url_changes(old_url),
                )
            )
        except TimeoutException:
            pass

        already_ready = (
            len(driver.window_handles) > len(before_handles)
            or driver.current_url != old_url
        )

        if not already_ready and driver.find_elements(By.CSS_SELECTOR, SNACKBAR_ACTIVE):
            WebDriverWait(driver, RENDER_SUCCESS_TIMEOUT).until(
                EC.any_of(
                    EC.visibility_of_element_located(
                        (By.CSS_SELECTOR, SNACKBAR_PDF_LINK)
                    ),
                    EC.visibility_of_element_located(
                        (By.CSS_SELECTOR, SNACKBAR_SUCCESS)
                    ),
                )
            )
            outcome = "rendering"
        else:
            outcome = "already-ready"

        return outcome  # type: ignore

    except Exception as e:
        print(f"[!] Export flow failed: {e}")
        return None
    finally:
        try:
            driver.close()
        finally:
            driver.quit()


def render_book_pdfs(list_of_urls: Path = ALL_BOOK_LINKS_FILE) -> None:
    with open(list_of_urls, "r", encoding="utf-8") as f:
        books_urls = json.load(f)

    for item in books_urls:
        book_year = item[0][0]
        book_url = item[1]

        if not (PDF_OUTPUT_PATH / f"Basel_{book_year}.pdf").exists():
            trigger_pdf_export_button(book_url)
