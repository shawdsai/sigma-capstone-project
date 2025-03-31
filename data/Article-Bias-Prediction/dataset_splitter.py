import argparse
import json
import os

import numpy as np
import pandas as pd
from loguru import logger
from sklearn.model_selection import train_test_split as sklearn_train_test_split


def load_json_files(folder_path):
    """Load all JSON files from a folder into a list."""
    data_list = []
    for filename in os.listdir(folder_path):
        if filename.endswith(".json"):
            file_path = os.path.join(folder_path, filename)
            try:
                with open(file_path, "r", encoding="utf-8") as file:
                    data = json.load(file)
                    data_list.append(data)
            except Exception as e:
                logger.warning(f"Failed to load '{file_path}': {e}")
    return data_list


def train_test_split(df, train_ratio=0.8, seed=None, stratify=True):
    """
    Split the dataframe into train and test sets.

    When stratification is enabled (and a "source" column exists):
      - Multi-sample sources (count > 1) are split using stratified sampling.
      - Singleton sources (count == 1) are assigned individually: each record goes
        to training with probability equal to train_ratio and to testing otherwise.
      - Records with missing 'source' are randomly split.

    If stratification is not enabled or 'source' is missing, a random split is performed.
    """
    if stratify and "source" in df.columns:
        logger.info("Performing stratified split based on 'source'")

        df_valid = df[df["source"].notna()].copy()
        df_missing = df[df["source"].isna()].copy()

        group_counts = df_valid.groupby("source").size()
        multi_sources = group_counts[group_counts > 1].index
        single_sources = group_counts[group_counts == 1].index

        df_multi = df_valid[df_valid["source"].isin(multi_sources)]
        df_single = df_valid[df_valid["source"].isin(single_sources)]

        if not df_multi.empty:
            try:
                multi_train, multi_test = sklearn_train_test_split(
                    df_multi, train_size=train_ratio, random_state=seed, stratify=df_multi["source"]
                )
            except ValueError as e:
                logger.warning(
                    f"Stratified split on multi-sample sources failed ({e}). Using random split for these records."
                )
                multi_train = df_multi.sample(frac=train_ratio, random_state=seed)
                multi_test = df_multi.drop(multi_train.index)
        else:
            multi_train = pd.DataFrame(columns=df.columns)
            multi_test = pd.DataFrame(columns=df.columns)

        if not df_single.empty:
            rng = np.random.default_rng(seed)
            mask = rng.random(len(df_single)) < train_ratio
            single_train = df_single[mask]
            single_test = df_single[~mask]
        else:
            single_train = pd.DataFrame(columns=df.columns)
            single_test = pd.DataFrame(columns=df.columns)

        if not df_missing.empty:
            logger.info("Assigning records with missing 'source' randomly.")
            missing_train = df_missing.sample(frac=train_ratio, random_state=seed)
            missing_test = df_missing.drop(missing_train.index)
        else:
            missing_train = pd.DataFrame(columns=df.columns)
            missing_test = pd.DataFrame(columns=df.columns)

        train_df = pd.concat([multi_train, single_train, missing_train])
        test_df = pd.concat([multi_test, single_test, missing_test])

        return train_df, test_df

    else:
        train_df = df.sample(frac=train_ratio, random_state=seed)
        test_df = df.drop(train_df.index)
        return train_df, test_df


def main(
    folder_path="jsons",
    output_prefix="article-bias-detection",
    subsample=None,
    train_ratio=0.8,
    seed=None,
    stratify=True,
):
    """Load JSON files, optionally subsample, split into train-test, and save as CSV."""
    logger.info(f"Loading JSON files from folder: {folder_path}")
    data_list = load_json_files(folder_path)

    if not data_list:
        logger.error("No data found. Exiting.")
        return

    df = pd.DataFrame(data_list)
    logger.info(f"Loaded {len(df)} records.")

    if subsample is not None and 0 < subsample < len(df):
        logger.info(f"Subsampling to {subsample} records.")
        df = df.sample(n=subsample, random_state=seed)

    train_df, test_df = train_test_split(df, train_ratio, seed, stratify=stratify)

    train_csv = f"{output_prefix}_train.csv"
    test_csv = f"{output_prefix}_test.csv"

    train_df.to_csv(train_csv, index=False, encoding="utf-8")
    test_df.to_csv(test_csv, index=False, encoding="utf-8")

    logger.success("CSV files created successfully:")
    logger.success(f"  - Training set: '{train_csv}' with {len(train_df)} records.")
    logger.success(f"  - Testing set: '{test_csv}' with {len(test_df)} records.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Merge JSON files into train-test split CSVs with optional subsampling."
    )
    parser.add_argument("--folder", type=str, default="jsons", help="Path to folder containing JSON files.")
    parser.add_argument(
        "--output_prefix", type=str, default="article-bias-detection", help="Prefix for output CSV files."
    )
    parser.add_argument("--subsample", type=int, default=None, help="Number of records to subsample.")
    parser.add_argument(
        "--train_ratio", type=float, default=0.8, help="Percentage of data to use for training (default: 0.8)."
    )
    parser.add_argument("--seed", type=int, default=2025, help="Random seed for reproducibility.")
    parser.add_argument(
        "--no-stratify",
        dest="stratify",
        action="store_false",
        help="Disable stratified split based on the 'source' field. Stratification is enabled by default.",
    )
    parser.set_defaults(stratify=True)

    args = parser.parse_args()

    main(
        folder_path=args.folder,
        output_prefix=args.output_prefix,
        subsample=args.subsample,
        train_ratio=args.train_ratio,
        seed=args.seed,
        stratify=args.stratify,
    )
