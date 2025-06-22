import os

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", ".."))

# TODO: improve import of schema file
def get_project_file(*relative_parts: str) -> str:
    """
    Construct an absolute file path relative to the current module's directory.

    Args:
        *relative_parts (str): One or more parts of the relative path to join.

    Returns:
        str: The absolute path to the file.

    Example:
        get_file_path("json", "schemas", "my_test_schema.json")
        -> "/full/path/to/current/module/schemas/transcribed_address_book_schema.json"
    """
    return os.path.join(PROJECT_ROOT, *relative_parts)
