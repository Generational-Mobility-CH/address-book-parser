from selenium.webdriver.common.by import By
import time
import json
import re

from modules.address_books.pages_downloader.src.common.driver import get_web_driver
from modules.address_books.pages_downloader.src.constants.paths import (
    ALL_BOOK_LINKS_FILE,
)


overview_urls = [
    "https://dls.staatsarchiv.bs.ch/records/1225908",
    "https://dls.staatsarchiv.bs.ch/records/1225909",
    "https://dls.staatsarchiv.bs.ch/records/1231853",
    "https://dls.staatsarchiv.bs.ch/records/1231854",
]
# TODO: Delete if not needed, else use it. Either way remove comment.
# overview_urls = ["https://dls.staatsarchiv.bs.ch/records/1225908","https://dls.staatsarchiv.bs.ch/records/1225909"]

driver = get_web_driver()

book_urls = []
for overview_url in overview_urls:
    # navigate to page and give it time to render
    driver.get(overview_url)
    time.sleep(5)
    # find all the buttons that can be clicked
    buttons = driver.find_elements(By.CSS_SELECTOR, "button.v-expansion-panel-header")

    for button in buttons:
        if "Child records" in button.text:
            time.sleep(1)
            button.click()
            break
    # give it time to render the content
    time.sleep(5)

    # identify all child elements
    elements = driver.find_elements(By.CSS_SELECTOR, "a.v-list-item--link")

    # extract urls of records from each element
    urls = []
    for element in elements:
        href = element.get_attribute("href")
        if "/records/" in href:
            urls.append(href)

    book_urls.extend(urls)

# navigate to each book url and open the preview
first_page_urls = []
for book_url in book_urls:
    # navigate to url and give it time to render
    driver.get(book_url)
    time.sleep(5)
    # extract title of the book
    title_element = driver.find_element(
        By.CSS_SELECTOR, '[data-testid="archive-record-title"]'
    )
    title = title_element.text
    year = re.findall(r"\d+", title)
    # identify all hyperlinks on the page
    all_links = driver.find_elements(By.TAG_NAME, "a")
    # iterate through each link and select the one to the preview
    for link in all_links:
        if "/preview" in str(link.get_attribute("href")):
            hyperlink = link.get_attribute("href")
            first_page_urls.append([year, hyperlink])
            break

driver.quit()

with open(ALL_BOOK_LINKS_FILE, "w", encoding="utf-8") as f:
    json.dump(first_page_urls, f, ensure_ascii=False, indent=4)
