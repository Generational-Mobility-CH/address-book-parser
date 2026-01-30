# This file uses the provided demo data to showcase the pipeline
from datetime import datetime

from modules.__main__ import main
from modules.setup import setup
from modules.shared.common.paths import PROJECT_ROOT_PATH


DEMO_CITY = "Basel"


if __name__ == "__main__":
    time_stamp = f"{datetime.now():%b %d - %H%M}"
    demo_data_dir = PROJECT_ROOT_PATH / "demo_data" / DEMO_CITY
    demo_input_dir = demo_data_dir / "transcriptions"
    demo_output_dir = demo_data_dir / "db"

    setup(
        time_stamp,
        [
            demo_data_dir,
            demo_input_dir,
            demo_output_dir,
        ],
    )

    main(demo_input_dir, demo_output_dir / "demo_output.db")
