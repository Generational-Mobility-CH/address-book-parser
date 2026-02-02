from pathlib import Path

from modules.pages_downloader.Basel.constants.paths import (
    JPG_OUTPUT_PATH,
    PDF_INPUT_PATH,
)
from modules.pages_preprocessor.src.cutter.column_cutter import cut_columns
from modules.pages_preprocessor.src.cutter.header_cutter import cut_header
from modules.pages_preprocessor.src.jpg_preprocessing.blackout_page_borders import (
    blackout_page_borders,
)
from modules.pages_preprocessor.src.jpg_preprocessing.get_page_borders_metadata import (
    get_page_borders_metadata,
)
from modules.pages_preprocessor.src.jpg_preprocessing.resize_jpg import resize_jpg
from modules.pages_preprocessor.src.paths import (
    GENERAL_INPUT_PATH,
    JPG_INPUT_PATH,
)
from modules.pages_preprocessor.src.pdf_jpg_conversion.pdf_to_jpg_converter import (
    pdf_to_jpg_converter,
)
from modules.pages_preprocessor.src.setup import setup


def main(
    table_of_content_path: Path,
    pdf_input_path: Path,
    columns_output_folder: str,
    header_output_folder: str,
    input_folder: Path,
    border_tolerance: int,
    cut_range: int,
) -> None:
    pdf_to_jpg_converter(pdf_input_path, table_of_content_path)
    resize_jpg(input_folder)
    borders_metadata = get_page_borders_metadata(input_folder, cut_range)
    blackout_page_borders(input_folder, input_folder, borders_metadata)
    cut_header(input_folder, header_output_folder)
    # multicolumn_metadata = get_multi_columns_metadata(output_folder, f"{output_folder}2", 2)
    # cut_multi_columns(f"{output_folder}2", f"{output_folder}2", 2, multicolumn_metadata)
    cut_columns(input_folder, columns_output_folder, 2)


if __name__ == "__main__":
    demo_file = "Basel_1943"
    demo_table_of_content_path = (
        GENERAL_INPUT_PATH / "json" / "toc" / f"{demo_file}_toc.json"
    )
    demo_pdf_file = PDF_INPUT_PATH / f"{demo_file}.pdf"
    demo_columns_output_path = JPG_OUTPUT_PATH / "person_register" / f"{demo_file}"
    demo_header_output_path = JPG_OUTPUT_PATH / "person_register" / f"{demo_file}"
    demo_input_folder = JPG_INPUT_PATH / "person_register" / f"{demo_file}"

    setup()

    main(
        demo_table_of_content_path,
        demo_pdf_file,
        demo_columns_output_path,
        demo_header_output_path,
        demo_input_folder,
        0,
        200,
    )  ## for house_register = 200, for person_register = 400
