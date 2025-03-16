# Dataset Splitter

## Overview
`dataset_splitter.py` is a Python script that loads JSON files from a specified folder, processes the data into a structured format, optionally subsamples the data, and splits it into training and testing sets based on a configurable percentage. The resulting datasets are saved as CSV files.

## Folder Structure
```
project_root/
│── jsons/                     # Folder containing input JSON files
│── dataset_splitter.py        # Python script for processing and splitting data
│── article-bias-detection_train.csv  # Output training dataset
│── article-bias-detection_test.csv   # Output testing dataset
│── README.md                  # This documentation file
```

## Installation & Requirements
This script requires Python 3 and the following Python libraries:
- `pandas`

To install dependencies, run:
```sh
pip install pandas
```

## Usage
Run the script using:
```sh
python3 dataset_splitter.py
```
By default, the script:
- Loads JSON files from the `jsons/` folder.
- Splits the data into 80% training and 20% testing sets.
- Saves the results as CSV files (`article-bias-detection_train.csv` and `article-bias-detection_test.csv`).

### Command-line Arguments
You can customize the script behavior using the following options:
```sh
python3 dataset_splitter.py --folder jsons --output_prefix my_dataset --subsample 10000 --train_ratio 0.75 --seed 42
```

| Argument        | Description |
|----------------|-------------|
| `--folder`     | Path to folder containing JSON files (default: `jsons/`). |
| `--output_prefix` | Prefix for output CSV files (default: `article-bias-detection`). |
| `--subsample`  | Number of records to randomly sample from the dataset. If omitted, all records are used. |
| `--train_ratio` | Proportion of data used for training (default: 0.8, meaning 80% training and 20% testing). |
| `--seed`       | Random seed for reproducibility (default: 2025). |

## Output
Upon successful execution, the script creates:
- `article-bias-detection_train.csv`: Training dataset (e.g., 30,043 records).
- `article-bias-detection_test.csv`: Testing dataset (e.g., 7,511 records).

These files are stored in the same directory as the script.

## Example Output
```
CSV files created successfully:
  - Training set: 'article-bias-detection_train.csv' with 30043 records.
  - Testing set: 'article-bias-detection_test.csv' with 7511 records.
```

## Notes
- Ensure the JSON files are correctly formatted before running the script.
- If subsampling, make sure the sample size is smaller than the total dataset size.
- The script preserves column names based on the JSON structure.

## License
This project is open-source. Feel free to modify and extend it for your needs.

## Author
Shaw

