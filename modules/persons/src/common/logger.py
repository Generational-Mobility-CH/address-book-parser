import logging

from modules.persons.src.common.paths import DATA_PATH


def setup_logging(log_file_name: str = "app"):
    log_file = (DATA_PATH / log_file_name).with_suffix(".log")

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s-%(name)s-%(levelname)s: %(message)s",
        datefmt="%Y.%m.%d %H:%M",
        handlers=[logging.StreamHandler(), logging.FileHandler(log_file)],
    )
