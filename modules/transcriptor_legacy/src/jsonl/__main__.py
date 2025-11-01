import re
from datetime import datetime
from pathlib import Path

from modules.shared.common.logger import setup_logging
from modules.shared.constants.paths import DATA_PATH
from modules.transcriptor_legacy.src.jsonl.jsonl_creator import create_jsonl


def main(input_path: Path, output_path: Path) -> None:
    """
    max_file_size:
        Batch upload limit: https://platform.openai.com/docs/guides/batch/batch-api
        max_file_size = 200 MB (200 * 1024 * 1024) * 90% (reduce max size so we don't go over)
    """
    max_file_size = 188743680

    for address_book_dir in input_path.iterdir():
        year_match = re.search(r"\d{4}$", address_book_dir.name)

        if address_book_dir.is_dir() and year_match:
            year = year_match.group(0)
            if year not in done_books_str:
                current_file = None
                file_counter = 0
                for book_page_file in address_book_dir.iterdir():
                    next_page_size = book_page_file.stat().st_size

                    if current_file is None or (
                        current_file.stat().st_size + next_page_size > max_file_size
                    ):
                        file_counter += 1
                        current_file = (
                            output_path / f"Basel_{year}-{file_counter}.jsonl"
                        )

                    create_jsonl(
                        current_file,
                        book_page_file,
                        f"Basel_{year}-{book_page_file.stem}",
                    )


if __name__ == "__main__":
    input_dir = DATA_PATH / "base64"
    output_dir = DATA_PATH / "jsonl"
    setup_logging(f"{datetime.now():%b_%d_%H%M}-jsonl", output_dir / "logs")

    done_books = [1877, 1880, 1883, 1884, 1885, 1910, 1911]
    done_books_str = [str(year) for year in done_books]

    main(input_dir, output_dir)
