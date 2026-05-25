"""Week 15 - Step 2: Build a ColumnTransformer + Pipeline for preprocessing.

Run:
    python 02_preprocessing_pipeline.py

Demonstrates: stratified split, imputation, OneHotEncoder, StandardScaler.
"""
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.model_selection import StratifiedShuffleSplit
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

# Re-use the loader from step 1
from importlib import import_module
load = import_module("01_data_exploration").load_housing_data


def stratified_split(housing: pd.DataFrame, test_size: float = 0.2,
                     random_state: int = 42) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Stratify the split by income category to avoid sampling bias."""
    housing = housing.copy()
    housing["income_cat"] = pd.cut(
        housing["median_income"],
        bins=[0., 1.5, 3.0, 4.5, 6., np.inf],
        labels=[1, 2, 3, 4, 5],
    )
    splitter = StratifiedShuffleSplit(n_splits=1, test_size=test_size,
                                      random_state=random_state)
    for tr, te in splitter.split(housing, housing["income_cat"]):
        train = housing.iloc[tr].drop("income_cat", axis=1)
        test = housing.iloc[te].drop("income_cat", axis=1)
    return train, test


def build_pipeline() -> ColumnTransformer:
    """Numeric: median impute + standard scale. Categorical: OneHot."""
    num_attribs = ["longitude", "latitude", "housing_median_age",
                   "total_rooms", "total_bedrooms", "population",
                   "households", "median_income"]
    cat_attribs = ["ocean_proximity"]
    num_pipe = Pipeline([
        ("imputer", SimpleImputer(strategy="median")),
        ("scaler", StandardScaler()),
    ])
    return ColumnTransformer([
        ("num", num_pipe, num_attribs),
        ("cat", OneHotEncoder(handle_unknown="ignore"), cat_attribs),
    ])


def main() -> None:
    housing = load()
    train, test = stratified_split(housing)
    print(f"Train: {len(train)}, Test: {len(test)}")

    prep = build_pipeline()
    X_train = train.drop("median_house_value", axis=1)
    X_train_prepared = prep.fit_transform(X_train)
    print("Prepared shape:", X_train_prepared.shape)
    print("Feature names:", prep.get_feature_names_out()[:6], "...")


if __name__ == "__main__":
    main()
