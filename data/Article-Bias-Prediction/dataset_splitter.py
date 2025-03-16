import argparse
import json
import os

import pandas as pd


def load_json_files(folder_path):
    """Load all JSON files from a folder into a list."""
    data_list = []
    for filename in os.listdir(folder_path):
        if filename.endswith(".json"):
            file_path = os.path.join(folder_path, filename)
            with open(file_path, "r", encoding="utf-8") as file:
                data = json.load(file)
                data_list.append(data)
    return data_list


def train_test_split(df, train_ratio=0.8, seed=None):
    """Split the dataframe into train and test sets based on the given ratio."""
    train_df = df.sample(frac=train_ratio, random_state=seed)
    test_df = df.drop(train_df.index)
    return train_df, test_df


def main(folder_path="jsons", output_prefix="article-bias-detection", subsample=None, train_ratio=0.8, seed=None):
    """Load JSON files, optionally subsample, split into train-test, and save as CSV."""
    data_list = load_json_files(folder_path)

    if not data_list:
        print("No data found. Exiting.")
        return

    df = pd.DataFrame(data_list)

    if subsample is not None and 0 < subsample < len(df):
        df = df.sample(n=subsample, random_state=seed)

    train_df, test_df = train_test_split(df, train_ratio, seed)

    train_csv = f"{output_prefix}_train.csv"
    test_csv = f"{output_prefix}_test.csv"

    train_df.to_csv(train_csv, index=False, encoding="utf-8")
    test_df.to_csv(test_csv, index=False, encoding="utf-8")

    print(f"CSV files created successfully:")
    print(f"  - Training set: '{train_csv}' with {len(train_df)} records.")
    print(f"  - Testing set: '{test_csv}' with {len(test_df)} records.")


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

    args = parser.parse_args()

    main(
        folder_path=args.folder,
        output_prefix=args.output_prefix,
        subsample=args.subsample,
        train_ratio=args.train_ratio,
        seed=args.seed,
    )
