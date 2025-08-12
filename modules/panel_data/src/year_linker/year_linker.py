import pandas as pd
import recordlinkage


def link_two_years(year1: str, year2: str, df: pd.DataFrame) -> None:
    df1 = df[df.year == year1]
    df2 = df[df.year == year2]

    common_last_names = set(df1["last_names"]) & set(df2["last_names"])
    print(f"Common last names: {len(common_last_names)}")

    df1.index = df1.index.astype(str) + year1
    df2.index = df2.index.astype(str) + year2

    indexer = recordlinkage.Index()
    indexer.block("last_names")
    candidate_links = indexer.index(df1, df2)
    print(f"{len(candidate_links)} candidate pairs generated")

    compare = recordlinkage.Compare()

    compare.string(
        "first_names",
        "first_names",
        method="jarowinkler",
        threshold=0.85,
        label="first_name_sim",
    )
    compare.string(
        "street_name",
        "street_name",
        method="levenshtein",
        threshold=0.85,
        label="address_sim",
    )
    compare.string("job", "job", method="jarowinkler", threshold=0.85, label="job_sim")

    features = compare.compute(candidate_links, df1, df2)

    features["score"] = features.sum(axis=1)

    matches = features[features["score"] >= 2]

    left_cols = ["first_names", "last_names", "street_name", "job"]
    right_cols = ["first_names", "last_names", "street_name", "job"]

    left_records = df1.loc[matches.index.get_level_values(0), left_cols].copy()
    right_records = df2.loc[matches.index.get_level_values(1), right_cols].copy()

    left_records = left_records.add_prefix("left_").reset_index()
    right_records = right_records.add_prefix("right_").reset_index()
    match_scores = matches.reset_index()

    # Combine all together
    detailed_matches = pd.concat(
        [
            left_records,
            right_records,
            match_scores.drop(columns=["level_0", "level_1"]),
        ],
        axis=1,
    )

    with pd.option_context("display.max_columns", None):
        print(detailed_matches.head())
        print(len(detailed_matches))
