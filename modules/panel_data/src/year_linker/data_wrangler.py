import numpy as np
import pandas as pd

from modules.panel_data.src.names_handling.last_and_first_names_separator import (
    separate_last_and_first_names,
)
from modules.panel_data.src.names_handling.last_names_separator import (
    separate_last_names,
)


def identify_and_remove_pattern(
    pattern: str, old_column_name: str, new_column_name: str, df: pd.DataFrame
) -> pd.DataFrame:
    df[new_column_name] = (
        df[old_column_name].str.contains(pattern, regex=True).astype(int)
    )

    df[old_column_name] = df[old_column_name].str.replace(pattern, "", regex=True)
    df[old_column_name] = (
        df[old_column_name].str.strip().replace(r"\s+", " ", regex=True)
    )
    return df


def wrangle_dataset(df: pd.DataFrame) -> pd.DataFrame:
    ## TODO: delete the cases with "KEINE ANGABE"
    ## TODO: identify family names that occur > 500 times
    ## TODO: from names with more than two: move names that do not occur > 500 times to first name
    # TODO: df = separate_last_and_first_names(df)
    df = separate_last_and_first_names(df)
    df = separate_last_names(df)
    widow_pattern = r"(?i)\b(?:wwe\.|ww\.|wwe|wittwe)\b\.?"
    df = identify_and_remove_pattern(widow_pattern, "first_names", "widow", df)
    widower_pattern = r"\(-|[()]"
    df = identify_and_remove_pattern(
        widower_pattern, "partner_last_name", "widower", df
    )
    df["sex"] = np.select(
        [df["widow"] == 1, df["widower"] == 1], ["F", "M"], default="NA"
    ).astype(object)
    return df
