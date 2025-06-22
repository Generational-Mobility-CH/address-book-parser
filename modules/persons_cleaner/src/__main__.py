import logging
from datetime import datetime

from libs.file_handler.src.extractor import extract_data
from modules.common.paths import DATA_PATH, INPUT_PATH, OUTPUT_PATH
from modules.persons_cleaner.src.load.loader import save_data, SupportedOutputFileTypes
from modules.persons_cleaner.src.transform.parser import transform

logger = logging.getLogger(__name__)


def main(data_path: str, output_path: str) -> None:
    setup_logging()

    raw_persons = extract_data(data_path)
    cleaned_persons = transform(raw_persons)
    save_data(cleaned_persons, output_path, SupportedOutputFileTypes.CSV)


def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s-%(name)s-%(levelname)s: %(message)s',
        datefmt='%Y.%m.%d %H:%M',
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler(f'{DATA_PATH}/app.log')
        ]
    )


if __name__ == "__main__":
    output_type = SupportedOutputFileTypes.CSV.value
    demo_input_path = f"{INPUT_PATH}/csv"
    demo_output_path = f"{OUTPUT_PATH}/{output_type}/{datetime.now():%m.%d-%H.%M.%S}.{output_type}"

    main(demo_input_path, demo_output_path)
