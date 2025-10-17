GENDER_FACTORS_DEFINITIONS_TABLE_NAME = "gender_factors_definitions"
GENDER_FACTORS_DEFINITIONS_COLUMNS_NAMES = ["factor_id", "factor_name", "factor_weight"]
GENDER_FACTORS_DEFINITIONS_TABLE_COLUMNS = """
    factor_id INTEGER PRIMARY KEY,
    factor_name TEXT,
    factor_weight REAL
"""
# TODO: replace placeholder values with actual values:
GENDER_FACTORS_DEFINITIONS = [
    (1, "keyword", 0.5),
    (2, "first_name", 0.3),
    (3, "job", 0.2),
]
