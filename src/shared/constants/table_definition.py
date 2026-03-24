PERSONS_TABLE_NAME = "persons"
PERSONS_TABLE_COLUMNS_DECLARATION = """
    last_name TEXT,
    partner_last_name TEXT, 
    first_names TEXT,
    gender TEXT, 
    street_name TEXT,
    house_number TEXT,
    job TEXT,
    remarks TEXT,
    year INTEGER,
    page_number TEXT,
    original_entry TEXT
"""
PERSONS_TABLE_COLUMNS_NAMES = [
    "last_name",
    "partner_last_name",
    "first_names",
    "gender",
    "street_name",
    "house_number",
    "job",
    "remarks",
    "year",
    "page_number",
    "original_entry",
]

FIELDS_DECLARATION = ", ".join(
    f"{field_name} TEXT" for field_name in PERSONS_TABLE_COLUMNS_NAMES
)
PLACEHOLDERS = ", ".join(["?"] * len(PERSONS_TABLE_COLUMNS_NAMES))
COLUMNS_STR = ", ".join(PERSONS_TABLE_COLUMNS_NAMES)
