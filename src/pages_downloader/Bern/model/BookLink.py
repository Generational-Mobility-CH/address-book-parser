from dataclasses import dataclass


@dataclass
class BookLink:
    year: str  # Info: The year can also be a range like '1880-1883'
    residents_register_pdf_url: str
