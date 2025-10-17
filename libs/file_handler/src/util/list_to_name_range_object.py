from modules.address_books.src.models.address_book.name_range import (
    NameRange,
)


def list_to_name_range_object(data: list[str]) -> NameRange:
    return NameRange(*data) if bool(data) and len(data) == 2 else NameRange()
