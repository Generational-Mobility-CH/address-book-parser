import os

from modules.pages_preprocessor.src.constants import (
    GENERAL_INPUT_PATH,
    GENERAL_OUTPUT_PATH,
)

years = [1877, 1880]
years.extend(range(1883, 1955))

for year in years:
    jpg_input_path = f"{GENERAL_INPUT_PATH}/jpg/person_register/Basel_{year}"
    jpg_output_path = f"{GENERAL_OUTPUT_PATH}/jpg/person_register/Basel_{year}"
    if not os.path.exists(jpg_input_path):
        os.makedirs(jpg_input_path)
    if not os.path.exists(jpg_output_path):
        os.makedirs(jpg_output_path)
