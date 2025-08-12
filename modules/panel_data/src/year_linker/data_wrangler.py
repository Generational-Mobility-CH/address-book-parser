import numpy as np
from pandas import DataFrame

from modules.panel_data.src.names_handling.first_names_cleaner import clean_first_names
from modules.panel_data.src.names_handling.last_and_first_names_separator import (
    separate_names_legacy,
)

from modules.panel_data.src.names_handling.last_names_separator import (
    separate_last_names,
)


def identify_and_remove_pattern(
    pattern: str, old_column_name: str, new_column_name: str, df: DataFrame
) -> DataFrame:
    df[new_column_name] = (
        df[old_column_name].str.contains(pattern, regex=True).astype(int)
    )

    df[old_column_name] = df[old_column_name].str.replace(pattern, "", regex=True)
    df[old_column_name] = (
        df[old_column_name].str.strip().replace(r"\s+", " ", regex=True)
    )
    return df


def separate_last_and_first_names(df: DataFrame) -> DataFrame:
    for index, og_name in enumerate(df["original_names"]):
        separated_names = separate_names_legacy(og_name)
        cleaned_names = clean_first_names(separated_names)

        df.at[index, "first_names"] = cleaned_names.first_names
        df.at[index, "last_names"] = cleaned_names.last_names

    return df


def wrangle_dataset(df: DataFrame) -> DataFrame:
    # TODO: delete the cases with "KEINE ANGABE"
    # TODO: identify family names that occur > 500 times
    # TODO: from names with more than two: move names that do not occur > 500 times to first name

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
