import re
from pathlib import Path


def get_year_from_file(file: Path) -> int:
    match = re.search(r"([18|19]\d{3})", file.name)
    year = match.group(0) if match else "0"

    return int(year) if year and year.isdigit() else 0
