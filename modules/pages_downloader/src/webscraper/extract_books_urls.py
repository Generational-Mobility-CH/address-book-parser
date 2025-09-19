import json
import re
import time
from pathlib import Path

from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By

from modules.pages_downloader.src.common.driver import get_web_driver
from modules.pages_downloader.src.constants.paths import (
    ALL_BOOK_LINKS_FILE,
    TEST_BOOK_LINK_FILE,
)

RENDERING_WAIT_TIME = 5


def get_book_urls(urls_collection: list[str], driver: WebDriver) -> list[str]:
    book_urls = []

    for url in urls_collection:
        driver.get(url)
        time.sleep(RENDERING_WAIT_TIME)
        expansion_panels = driver.find_elements(
            By.CSS_SELECTOR, "button.v-expansion-panel-header"
        )

        for button in expansion_panels:
            if any(
                term in button.text
                for term in ["Child records", "Untergeordnete Verzeichnungseinheiten"]
            ):
                time.sleep(1)
                driver.execute_script("arguments[0].scrollIntoView();", button)
                button.click()
                break

        time.sleep(RENDERING_WAIT_TIME)
        child_elements = driver.find_elements(By.CSS_SELECTOR, "a.v-list-item--link")

        for element in child_elements:
            href = element.get_attribute("href")
            if "/records/" in href:
                book_urls.append(href)

    return book_urls


def save_first_page_preview_links(
    urls_collection: list[str], driver: WebDriver
) -> None:
    urls = get_book_urls(urls_collection, driver)
    first_page_urls = []

    for url in urls:
        driver.get(url)
        time.sleep(RENDERING_WAIT_TIME)

        title = driver.find_element(
            By.CSS_SELECTOR, '[data-testid="archive-record-title"]'
        ).text
        year = re.findall(r"\d+", title)
        all_page_links = driver.find_elements(By.TAG_NAME, "a")

        for link in all_page_links:
            if "/preview" in str(link.get_attribute("href")):
                hyperlink = link.get_attribute("href")
                print(hyperlink)
                first_page_urls.append([year, hyperlink])
                break

    with open(ALL_BOOK_LINKS_FILE, "w", encoding="utf-8") as f:
        json.dump(first_page_urls, f, ensure_ascii=False, indent=4)


def get_single_book_example(all_book_links_json: Path, chosen_year: int) -> None:
    with open(all_book_links_json, "r", encoding="utf-8") as f:
        all_book_links = json.load(f)

    single_link = [link for link in all_book_links if link[0][0] == str(chosen_year)]

    with open(TEST_BOOK_LINK_FILE, "w", encoding="utf-8") as f:
        json.dump(single_link, f, ensure_ascii=False, indent=4)


def extract_books_urls_from_overview(
    urls_collection: list[str], test_case: int = 1917
) -> None:
    if not ALL_BOOK_LINKS_FILE.exists():
        ALL_BOOK_LINKS_FILE.touch(exist_ok=True)
        demo_driver = get_web_driver()
        save_first_page_preview_links(urls_collection, demo_driver)
        demo_driver.quit()

    TEST_BOOK_LINK_FILE.touch(exist_ok=True)
    get_single_book_example(ALL_BOOK_LINKS_FILE, chosen_year=test_case)
