import logging
from pathlib import Path


def setup_logging(log_file_name: str, log_path: Path) -> None:
    log_path.mkdir(parents=True, exist_ok=True)

    log_file = (log_path / log_file_name).with_suffix(".log")

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s-%(name)s-%(levelname)s: %(message)s",
        datefmt="%Y.%m.%d %H:%M",
        handlers=[logging.StreamHandler(), logging.FileHandler(log_file)],
    )
