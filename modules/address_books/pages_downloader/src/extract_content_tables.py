import json
import random
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from modules.address_books.pages_downloader.src.common.driver import get_web_driver
from modules.address_books.pages_downloader.src.constants.paths import (
    GENERAL_INPUT_PATH,
    ALL_BOOK_LINKS_FILE,
)


WAIT_TIME = 5


def click_btn(driver, btn_string):
    wait = WebDriverWait(driver, WAIT_TIME)
    btn = wait.until(
        EC.presence_of_element_located(
            (
                By.XPATH,
                f"//button[contains(@class, 'tify-header-button') and contains(@aria-controls, '{btn_string}')]",
            )
        )
    )

    driver.execute_script("arguments[0].scrollIntoView(true);", btn)
    time.sleep(0.5)

    driver.execute_script("arguments[0].click();", btn)
    time.sleep(1)


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


if __name__ == "__main__":
    with open(ALL_BOOK_LINKS_FILE, "r", encoding="utf-8") as f:
        books_urls = json.load(f)

    for item in books_urls:
        book_year = item[0][0]
        book_url = item[1]

        extracted_toc = extract_content_table(book_url)
        with open(
            GENERAL_INPUT_PATH / "json" / "toc" / f"Basel_{book_year}_toc.json",
            "w",
            encoding="utf-8",
        ) as f:
            json.dump(extracted_toc, f, ensure_ascii=False, indent=4)
