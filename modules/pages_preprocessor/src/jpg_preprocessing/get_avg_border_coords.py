import numpy as np
import pandas as pd


def flatten_dictionnary(dictionnary: dict, parent_key="") -> dict:
    items = []
    for key, value in dictionnary.items():
        new_key = f"{parent_key}_{key}" if parent_key else key
        if isinstance(value, dict):
            items.extend(flatten_dictionnary(value, new_key).items())
        elif value is not None:
            items.append((new_key, value))
        else:
            pass
    return dict(items)


def dict_to_df(dictionnary: dict, entrytype: str) -> pd.DataFrame:
    records = []
    for entry, content in dictionnary.items():
        flattened_metadata = flatten_dictionnary(content)
        flattened_metadata[f"{entrytype}"] = entry
        records.append(flattened_metadata)

    df = pd.DataFrame(records)
    df = df.replace({None: np.nan})
    df = df.sort_values(by=f"{entrytype}").reset_index(drop=True)

    return df


def metadata_as_df(metadata: dict) -> pd.DataFrame:
    metadata_df = dict_to_df(metadata, "page")
    metadata_df["digits"] = metadata_df["page"].str.extract(r"(\d+)")
    metadata_df["digits"] = pd.to_numeric(metadata_df["digits"], errors="coerce")
    metadata_df["is_even"] = metadata_df["digits"] % 2 == 0
    return metadata_df


def get_avg_coords(metadata: dict, columns_to_drop: list[str]) -> tuple:
    if columns_to_drop:
        metadata_df = metadata_as_df(metadata)
        metadata_df = metadata_df.drop(columns=columns_to_drop)
    else:
        metadata_df = metadata_as_df(metadata)

    # metadata_df = metadata_df[(metadata_df.filter(like="x1", axis=1) != 0).any(axis=1)]

    even_avg_series = metadata_df[metadata_df["is_even"]].mean(numeric_only=True)
    uneven_avg_series = metadata_df[not metadata_df["is_even"]].mean(numeric_only=True)

    return even_avg_series, uneven_avg_series
