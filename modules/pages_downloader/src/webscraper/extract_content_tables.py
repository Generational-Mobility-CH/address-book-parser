import json
import random
import time
from pathlib import Path

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from modules.pages_downloader.src.common.driver import get_web_driver
from modules.pages_downloader.src.common.web_navigation_tools import click_btn
from modules.pages_downloader.src.constants.paths import (
    GENERAL_OUTPUT_PATH,
)

WAIT_TIME = 5


def extract_content_table(preview_url: str) -> str | None:
    driver = get_web_driver()
    try:
        driver.get(preview_url)
        wait = WebDriverWait(driver, WAIT_TIME)

        click_btn(driver, "-toc")

        toc_section = wait.until(
            EC.presence_of_element_located((By.CLASS_NAME, "tify-toc-list"))
        )
        book_chapters = toc_section.find_elements(By.TAG_NAME, "a")

        toc = []
        for chapter in book_chapters:
            chapter_title = chapter.find_element(By.CLASS_NAME, "tify-toc-label").text
            chepter_page = chapter.find_element(By.CLASS_NAME, "tify-toc-page").text
            toc.append([chapter_title, chepter_page])
        return toc
    except Exception as e:
        print(f"Failed to get toc from {preview_url}: {e}")
        time.sleep(random.uniform(2, 6))
    finally:
        driver.quit()


def write_jsons_with_table_of_content(url_collection: Path) -> None:
    with open(url_collection, "r", encoding="utf-8") as f:
        book_urls = json.load(f)

    for item in book_urls:
        book_year = item[0][0]
        book_url = item[1]

        output_file = (
            GENERAL_OUTPUT_PATH / "json" / "toc" / f"Basel_{book_year}_toc.json"
        )

        if output_file.exists():
            continue

        extracted_toc = extract_content_table(book_url)
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(extracted_toc, f, ensure_ascii=False, indent=4)
