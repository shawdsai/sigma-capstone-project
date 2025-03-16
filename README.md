# Sigma Capstone Project

This repository contains datasets, scripts, and configurations for the **Sigma Capstone Project**, focused on **political article bias**.

## 📂 Repository Structure

- **`archived/`**  
  Contains old or outdated assets, including deprecated datasets, previous versions of scripts, and other historical data.

- **`data/`**  
  Contains datasets from different sources, including processed and raw data used for analysis.

- **`.github/workflows/`**  
  Contains GitHub Actions workflows for automation, linting, and pre-commit hooks.

- **`.gitignore`**  
  Specifies files and directories to be ignored by Git, such as large CSV files.

- **`.pre-commit-config.yaml`**  
  Configuration for the `pre-commit` framework, enforcing coding standards using `isort` and `black`.

## 🔧 Setup

To ensure code quality and formatting consistency, this repository uses **pre-commit hooks**.  
Install them by running:

```bash
pip install pre-commit
pre-commit install
