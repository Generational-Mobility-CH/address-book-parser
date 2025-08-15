import pandas as pd

from modules.pages_preprocessor.src.file_handling.read_json import read_json


def get_entry_by_pos(
    table_of_content: pd.DataFrame, search_term: str, position: int
) -> tuple[str, str]:
    index = table_of_content[
        table_of_content["Chapter"].str.contains(search_term)
    ].index
    if len(index) > 0:
        hit_start_index = index[position - 1]
        start_page = table_of_content.iloc[hit_start_index]["Page"]

        hit_end_index = hit_start_index + 1
        if hit_end_index < len(table_of_content):
            end_page = table_of_content.iloc[hit_end_index]["Page"]
        else:
            end_page = None
    return start_page, end_page


def get_register_range(
    table_of_content_path: str,
    search_term_start: str,
    search_term_end: str,
    search_term_start_pos: int,
    search_term_end_pos: int,
) -> tuple[int, int]:
    table_of_content = read_json(table_of_content_path)
    register_df = pd.DataFrame(table_of_content)
    register_df.columns = ["Chapter", "Page"]
    register_df.Page = register_df.Page.str.extract("(\\d+)")

    start_page = get_entry_by_pos(
        register_df, search_term_start, search_term_start_pos
    )[0]

    end_page = get_entry_by_pos(register_df, search_term_end, search_term_end_pos)[1]

    page_range = (int(start_page) + 1, int(end_page))
    return page_range
