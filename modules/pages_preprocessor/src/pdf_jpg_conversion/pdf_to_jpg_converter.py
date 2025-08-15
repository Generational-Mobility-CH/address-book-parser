import os
import re

from pdf2image import convert_from_path

from modules.pages_preprocessor.src.constants import GENERAL_INPUT_PATH
from modules.pages_preprocessor.src.pdf_jpg_conversion.find_pagerange_in_table_of_content import (
    get_register_range,
)


def pdf_to_jpg_converter(pdf_path: str, table_of_content_path: str) -> None:
    start_page, end_page = get_register_range(
        table_of_content_path,
        "Verzeichnis.*Einwohner|Basel",
        "^Z|Y / Z|X / Y / Z",
        1,
        1,
    )
    year = re.findall(r"\d+", table_of_content_path)[0]

    if int(year) > 1876:
        for page in range(start_page, end_page + 1):
            page_jpg_path = (
                f"{GENERAL_INPUT_PATH}/jpg/person_register/Basel_{year}/page{page}.jpg"
            )
            if not os.path.exists(page_jpg_path):
                page_jpg = convert_from_path(
                    f"{pdf_path}", 200, first_page=page, last_page=page
                )[0]
                page_jpg.save(page_jpg_path, "JPEG")
