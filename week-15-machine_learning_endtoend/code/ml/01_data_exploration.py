"""Week 15 - Step 1: Load California Housing data and do EDA.

Run:
    python 01_data_exploration.py

Source: adapted from Géron (2023) Hands-on ML, Chapter 2.
"""
import tarfile
import urllib.request
from pathlib import Path

import numpy as np
import pandas as pd


def load_housing_data() -> pd.DataFrame:
    """Download + cache + load the California Housing dataset."""
    tarball_path = Path("datasets/housing.tgz")
    if not tarball_path.is_file():
        Path("datasets").mkdir(parents=True, exist_ok=True)
        url = "https://github.com/ageron/data/raw/main/housing.tgz"
        urllib.request.urlretrieve(url, tarball_path)
        with tarfile.open(tarball_path) as t:
            t.extractall(path="datasets")
    return pd.read_csv(Path("datasets/housing/housing.csv"))


def main() -> None:
    housing = load_housing_data()
    print("Shape:", housing.shape)
    print("\n--- info() ---")
    housing.info()
    print("\n--- describe() ---")
    print(housing.describe().round(2))
    print("\n--- missing values ---")
    print(housing.isna().sum())
    print("\n--- ocean_proximity counts ---")
    print(housing["ocean_proximity"].value_counts())


if __name__ == "__main__":
    main()
