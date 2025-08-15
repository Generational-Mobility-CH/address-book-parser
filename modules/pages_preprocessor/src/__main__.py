from modules.pages_preprocessor.src.constants import (
    GENERAL_INPUT_PATH,
    GENERAL_OUTPUT_PATH,
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


def main(
    demo_table_of_content_path: str,
    pdf_input_path: str,
    columns_output_folder: str,
    header_output_folder: str,
    input_folder: str,
    border_tolerance: int,
    cut_range: int,
) -> None:
    # pdf_to_jpg_converter(pdf_input_path, demo_table_of_content_path)
    resize_jpg(input_folder)
    borders_metadata = get_page_borders_metadata(input_folder, cut_range)
    blackout_page_borders(input_folder, input_folder, borders_metadata)
    cut_header(input_folder, header_output_folder)
    # multicolumn_metadata = get_multi_columns_metadata(output_folder, f"{output_folder}2", 2)
    # cut_multi_columns(f"{output_folder}2", f"{output_folder}2", 2, multicolumn_metadata)
    cut_columns(input_folder, columns_output_folder, 2)


if __name__ == "__main__":
    demo_file = "Basel_1943"
    demo_table_of_content_path = f"{GENERAL_INPUT_PATH}/json/toc/{demo_file}_toc.json"
    demo_pdf_file = f"{GENERAL_INPUT_PATH}/pdf/{demo_file}.pdf"
    demo_columns_output_path = f"{GENERAL_OUTPUT_PATH}/jpg/person_register/{demo_file}"
    demo_header_output_path = (
        f"{GENERAL_OUTPUT_PATH}/jpg/person_register_namerange/{demo_file}"
    )
    demo_input_folder = f"{GENERAL_INPUT_PATH}/jpg/person_register/{demo_file}"

    main(
        demo_table_of_content_path,
        demo_pdf_file,
        demo_columns_output_path,
        demo_header_output_path,
        demo_input_folder,
        0,
        200,
    )  ## for house_register = 200, for person_register = 400
