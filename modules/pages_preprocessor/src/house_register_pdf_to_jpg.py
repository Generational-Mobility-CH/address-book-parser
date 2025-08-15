import json

import pandas as pd
from pdf2image import convert_from_path
import os
import re

from modules.pages_preprocessor.src.paths import (
    GENERAL_INPUT_PATH,
    GENERAL_OUTPUT_PATH,
)
from modules.pages_preprocessor.src.pdf_jpg_conversion.find_pagerange_in_table_of_content import (
    get_register_range,
)

if __name__ == "__main__":
    all_tocs = os.listdir(f"{GENERAL_INPUT_PATH}/json/toc")
    index_file = pd.read_csv(
        f"{GENERAL_INPUT_PATH}/csv/250121-AdressbucherOverview.csv"
    )
    index_file = index_file[
        (index_file["Eigentümer"] == "ja") & (index_file["Jahr"] > 1876)
    ]
    years_with_home_register = index_file["Jahr"].values
    for toc in all_tocs[34:35]:
        with open(f"{GENERAL_INPUT_PATH}/json/toc/{toc}", "r", encoding="utf-8") as f:
            book_tocs = json.load(f)

        year = int(re.findall(r"\d+", toc)[0])

        if year in years_with_home_register:
            if year > 1914 and year != 1947:
                start_page, end_page = get_register_range(
                    book_tocs,
                    "Häuserverzeichnis.*Basel|Häuservezeichnis.*Basel",
                    "Häuserverzeichnis.*Basel|Häuservezeichnis.*Basel",
                    2,
                    2,
                )
            else:
                start_page, end_page = get_register_range(
                    book_tocs, "Häuserverzeichnis", "Häuserverzeichnis", 1, 1
                )

            print(year, start_page, end_page)
            pages = convert_from_path(
                f"{GENERAL_INPUT_PATH}/pdf/Basel_{year}.pdf",
                200,
                first_page=start_page,
                last_page=end_page,
            )
            for i, page in enumerate(pages):
                page.save(
                    f"{GENERAL_OUTPUT_PATH}/jpg/house_register/Basel_{year}/page{start_page + i + 1}.jpg",
                    "JPEG",
                )
