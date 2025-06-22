import os
from enum import Enum

from modules.models.person import Person
from modules.persons_cleaner.src.extract.csv.extractor import CsvExtractor
from modules.persons_cleaner.src.extract.extractor_strategy import ExtractorStrategy


class SupportedFileTypes(Enum):
    CSV = ".csv"


EXTRACTORS: dict[SupportedFileTypes, ExtractorStrategy] = {
    SupportedFileTypes.CSV: CsvExtractor(),
}


def extract_data(data_path: str) -> list[Person]:
    all_books_paths = get_sub_paths(data_path)
    extractor = get_extractor_strategy(all_books_paths[0])

    return extractor.extract(all_books_paths)


def get_extractor_strategy(book_path: str) -> ExtractorStrategy:
    if os.path.isdir(book_path):
        for file in os.listdir(book_path):
            file_type = file.split(".")[-1].upper()
            if file_type in SupportedFileTypes.__members__:
                return EXTRACTORS[SupportedFileTypes[file_type]]
    else:
        file_type = book_path.split(".")[-1].upper()
        if file_type in SupportedFileTypes.__members__:
            return EXTRACTORS[SupportedFileTypes[file_type]]

    raise Exception(f"Unsupported file type for book: {book_path}")


def get_sub_paths(path: str) -> list[str]:
    """
    Returns a list of paths for file(s) or subfolder(s) in the given path.
    Info: 1 .json file = 1 book page; 1 .txt file = 1 entire book.
    """
    paths: list[str] = []

    if os.path.isfile(path):
        paths.append(path)
    elif os.path.isdir(path):
        dir_content = os.listdir(path)
        for item in dir_content:
            if item.endswith(".json"):
                paths = [path]
                break
            item_path = os.path.join(path, item)
            if os.path.isfile(item_path):
                paths.append(item_path)
            elif os.path.isdir(item_path):
                paths.extend(get_sub_paths(item_path))

    return paths
