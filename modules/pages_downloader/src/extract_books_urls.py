from selenium.webdriver.chrome import webdriver
from selenium.webdriver.common.by import By
import time
import json
import re

from modules.pages_downloader.src.common.driver import get_web_driver
from modules.pages_downloader.src.constants.paths import (
    ALL_BOOK_LINKS_FILE,
)


RENDERING_WAIT_TIME = 5

overview_urls = [
    "https://dls.staatsarchiv.bs.ch/records/1225908",
    "https://dls.staatsarchiv.bs.ch/records/1225909",
    "https://dls.staatsarchiv.bs.ch/records/1231853",
    "https://dls.staatsarchiv.bs.ch/records/1231854",
]

# TODO: store output in list for quicker access. If they're always the same - remove get_book_urls() ?
basel_staatsarchiv_book_urls = [
    "https://dls.staatsarchiv.bs.ch/records/79643",
    "https://dls.staatsarchiv.bs.ch/records/79643",
    "https://dls.staatsarchiv.bs.ch/records/79643",
    "https://dls.staatsarchiv.bs.ch/records/79643",
]


def get_book_urls(urls_collection: list[str], driver: webdriver) -> list[str]:
    book_urls = []

    for url in urls_collection:
        driver.get(url)
        time.sleep(RENDERING_WAIT_TIME)
        clickable_buttons = driver.find_elements(
            By.CSS_SELECTOR, "button.v-expansion-panel-header"
        )

        for button in clickable_buttons:
            if "Child records" in button.text:
                time.sleep(1)
                button.click()
                print(
                    "Clicked button!"
                )  # TODO: this button is never clicked, remove this part?
                break

        time.sleep(RENDERING_WAIT_TIME)

        child_elements = driver.find_elements(By.CSS_SELECTOR, "a.v-list-item--link")

        for element in child_elements:
            href = element.get_attribute("href")
            if "/records/" in href:
                book_urls.extend(href)

    return book_urls


def save_first_page_preview_links(
    urls_collection: list[str], driver: webdriver
) -> None:
    first_page_urls = []

    for url in urls_collection:
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
                first_page_urls.append([year, hyperlink])
                break

    with open(ALL_BOOK_LINKS_FILE, "w", encoding="utf-8") as f:
        json.dump(first_page_urls, f, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    demo_driver = get_web_driver()
    save_first_page_preview_links(basel_staatsarchiv_book_urls, demo_driver)
    demo_driver.quit()
