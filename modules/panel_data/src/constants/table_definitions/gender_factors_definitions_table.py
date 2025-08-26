GENDER_FACTORS_DEFINITIONS_TABLE_NAME = "gender_factors_definitions"
GENDER_FACTORS_DEFINITIONS_COLUMNS_NAMES = ["id", "factor_name", "weight"]
GENDER_FACTORS_DEFINITIONS_TABLE_COLUMNS = """
    id INTEGER PRIMARY KEY,
    factor_name TEXT,
    weight REAL
"""
# TODO: replace placeholder values with actual values:
GENDER_FACTORS_DEFINITIONS = [
    (1, "first_name", 0.5),
    (2, "job", 0.3),
    (3, "widow", 0.2),
    (4, "keyword", 0.1),
]
