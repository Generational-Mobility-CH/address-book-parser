import re
from pathlib import Path


def get_year_from_file_name(file_name: Path) -> int:
    match = re.search(r"([19|20]\d{3})", file_name.name)
    year = match.group(0) if match else "0"

    return int(year) if year and year.isdigit() else 0
