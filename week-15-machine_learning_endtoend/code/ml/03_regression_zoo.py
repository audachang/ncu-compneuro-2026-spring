"""Week 15 - Step 3: Compare regression algorithms with 5-fold CV.

Models covered (one representative per algorithm family):
    - Linear      : LinearRegression  + Ridge
    - Instance    : KNeighborsRegressor
    - Tree        : DecisionTreeRegressor
    - Ensemble    : RandomForestRegressor + GradientBoostingRegressor
    - Kernel      : SVR(kernel='rbf')

Run:
    python 03_regression_zoo.py
"""
import numpy as np
from sklearn.ensemble import GradientBoostingRegressor, RandomForestRegressor
from sklearn.linear_model import LinearRegression, Ridge
from sklearn.model_selection import cross_val_score
from sklearn.neighbors import KNeighborsRegressor
from sklearn.pipeline import make_pipeline
from sklearn.svm import SVR
from sklearn.tree import DecisionTreeRegressor

from importlib import import_module
load = import_module("01_data_exploration").load_housing_data
stratified_split = import_module("02_preprocessing_pipeline").stratified_split
build_pipeline = import_module("02_preprocessing_pipeline").build_pipeline


MODELS = {
    "Linear":          LinearRegression(),
    "Ridge (a=1)":     Ridge(alpha=1.0),
    "k-NN (k=5)":      KNeighborsRegressor(n_neighbors=5),
    "DecisionTree":    DecisionTreeRegressor(random_state=42),
    "RandomForest":    RandomForestRegressor(n_estimators=100, random_state=42, n_jobs=-1),
    "GradientBoost":   GradientBoostingRegressor(n_estimators=100, random_state=42),
    "SVR (RBF)":       SVR(kernel="rbf", C=10, gamma=0.1),
}


def main() -> None:
    housing = load()
    train, _ = stratified_split(housing)
    X = train.drop("median_house_value", axis=1)
    y = train["median_house_value"]
    prep = build_pipeline()

    print(f"{'Model':<18} {'RMSE mean':>11} {'RMSE std':>10}")
    print("-" * 41)
    for name, model in MODELS.items():
        pipe = make_pipeline(prep, model)
        # NOTE: SVR is slow on 16k samples — subsample for in-class demo.
        if isinstance(model, SVR):
            sub = np.random.RandomState(0).choice(len(X), 3000, replace=False)
            scores = -cross_val_score(
                pipe, X.iloc[sub], y.iloc[sub], cv=5,
                scoring="neg_root_mean_squared_error", n_jobs=-1,
            )
        else:
            scores = -cross_val_score(
                pipe, X, y, cv=5,
                scoring="neg_root_mean_squared_error", n_jobs=-1,
            )
        print(f"{name:<18} {scores.mean():>11.0f} {scores.std():>10.0f}")


if __name__ == "__main__":
    main()
