from pandas import DataFrame


def separate_last_names(df: DataFrame) -> DataFrame:
    df[["own_last_name", "partner_last_name"]] = (
        df["last_names"].str.split(r"[-\s]+", n=1, expand=True).fillna("")
    )
    return df
