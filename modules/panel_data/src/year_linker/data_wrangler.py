import pandas as pd


def separate_first_names(df: pd.DataFrame) -> pd.DataFrame:
    widow_pattern = r"(?i)\b(?:wwe\.|ww\.|wwe|wittwe)\b\.?"
    df["widow"] = df["first_names"].str.contains(widow_pattern, regex=True).astype(int)
    df["first_names"] = df["first_names"].str.replace(widow_pattern, "", regex=True)
    df["first_names"] = df["first_names"].str.strip().replace(r"\s+", " ", regex=True)
    return df


def separate_last_names(df: pd.DataFrame) -> pd.DataFrame:
    df[["own_last_name", "partner_last_name"]] = (
        df["last_names"].str.split(r"[-\s]+", n=1, expand=True).fillna("")
    )
    return df


def wrangle_dataset(df: pd.DataFrame) -> pd.DataFrame:
    df = separate_last_names(df)
    df = separate_first_names(df)
    return df
