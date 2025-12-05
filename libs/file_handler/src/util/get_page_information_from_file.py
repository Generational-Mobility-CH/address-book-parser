from pathlib import Path


def get_page_info_from_file(file: Path) -> str:
    """
    Find information about the book page based on current file naming convention:
    CITY-YEAR-PAGE_INFO (e.g.: Basel-1977-rcol_page88.csv)
    """
    file_name_parts = file.stem.split("-")
    if len(file_name_parts) == 3:
        return file_name_parts[2]

    return ""
