from datetime import datetime
from logging import getLogger
from pathlib import Path

from modules.shared.constants.paths import DATA_PATH
from modules.transcriptor.src.data_convertors import to_base64
from modules.transcriptor_legacy.src.setup import setup

logger = getLogger(__name__)


def main(input_path: Path, output_path: Path) -> None:
    for year in input_path.iterdir():
        if year.is_dir():
            new_dir = output_path / year
            new_dir.mkdir(parents=True, exist_ok=True)
            for image in year.iterdir():
                logger.info(f"Encoding image {image}...")
                encoded_image = to_base64(image)
                output_file_path = new_dir / f"{image.stem}.txt"

                with open(output_file_path, "w") as f:
                    f.write(encoded_image)

                logger.info(f"Wrote file at {output_file_path}.")


if __name__ == "__main__":
    input_dir = DATA_PATH / "jpg" / "headers"
    output_dir = DATA_PATH / "base64" / "headers"
    setup(f"{datetime.now():%b_%d_%H%M}", [input_dir, output_dir])
    main(input_dir, output_dir)
