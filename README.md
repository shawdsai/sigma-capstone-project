# Sigma Capstone Project

This repository contains datasets, scripts, and configurations for the **Sigma Capstone Project**, focused on **political article bias**.

## 📂 Repository Structure

- **`archived/`**  
  Contains old or outdated assets, including deprecated datasets, previous versions of scripts, and other historical data.

- **`data/`**  
  Contains datasets from different sources, including processed and raw data used for analysis.

- **`models/`**  
  Contains checkpoints of our trained models, used for inference and benchmarking within the pipeline.

- **`workspace/`**  
  Contains development work and experimentation on various models by team members:
  - `workspace/Boat`
  - `workspace/Nueng`
  - `workspace/Shaw`

- **`requirements.txt`**  
  Lists all necessary libraries to run our notebooks.

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
```

## 💻 Running

To run the benchmarking pipeline, you can use either of the following notebooks:
- `workspace/Boat/benchmark_pipeline.ipynb`
- `workspace/Shaw/BenchmarkPipeline.ipynb`
- `workspace/Nueng/Benchmark_Pipeline_Nueng.ipynb`

These notebooks benchmark our **Political Bias Prediction on News Articles**, using real-world data from the **2024 U.S. Election**, gathered from various news sources.

### Steps:
1. Prepare an environment of your choice to host the notebook (preferably Google Colab with a GPU instance).
2. Run the entire `Setup` section.
3. Add a news article URL inside the `url_list`.
4. Run the `Pipeline` section to get predictions.
5. (Optional) Run the `Evaluation` section to see visualizations and performance metrics.

Benchmark data is available in BenchmarkScore.xlsx.