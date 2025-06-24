import logging

from modules.persons.common.paths import DATA_PATH


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
