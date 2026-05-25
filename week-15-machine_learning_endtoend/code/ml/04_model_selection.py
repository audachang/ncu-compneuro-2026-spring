"""Week 15 - Step 4: Hyperparameter tuning with Grid and Randomized search.

Run:
    python 04_model_selection.py
"""
import numpy as np
from scipy.stats import randint
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import root_mean_squared_error
from sklearn.model_selection import GridSearchCV, RandomizedSearchCV
from sklearn.pipeline import make_pipeline

from importlib import import_module
load = import_module("01_data_exploration").load_housing_data
stratified_split = import_module("02_preprocessing_pipeline").stratified_split
build_pipeline = import_module("02_preprocessing_pipeline").build_pipeline


def main() -> None:
    housing = load()
    train, test = stratified_split(housing)
    X_tr, y_tr = train.drop("median_house_value", axis=1), train["median_house_value"]
    X_te, y_te = test.drop("median_house_value", axis=1), test["median_house_value"]

    prep = build_pipeline()
    pipe = make_pipeline(prep, RandomForestRegressor(random_state=42, n_jobs=-1))

    # --- GridSearchCV --------------------------------------------------------
    param_grid = {
        "randomforestregressor__n_estimators": [30, 100, 200],
        "randomforestregressor__max_features": [4, 6, 8],
    }
    grid = GridSearchCV(pipe, param_grid, cv=3,
                        scoring="neg_root_mean_squared_error", n_jobs=-1)
    grid.fit(X_tr, y_tr)
    print("Grid best params:", grid.best_params_)
    print(f"Grid best CV RMSE: {-grid.best_score_:.0f}")

    # --- RandomizedSearchCV --------------------------------------------------
    param_dist = {
        "randomforestregressor__n_estimators": randint(30, 300),
        "randomforestregressor__max_features": randint(2, 9),
    }
    rand = RandomizedSearchCV(pipe, param_dist, n_iter=10, cv=3,
                              scoring="neg_root_mean_squared_error",
                              random_state=42, n_jobs=-1)
    rand.fit(X_tr, y_tr)
    print("\nRandom best params:", rand.best_params_)
    print(f"Random best CV RMSE: {-rand.best_score_:.0f}")

    # --- Final test set evaluation — only once -------------------------------
    final = rand.best_estimator_
    test_rmse = root_mean_squared_error(y_te, final.predict(X_te))
    print(f"\nFinal TEST RMSE: {test_rmse:.0f}  (this is the only number you report)")

    # Feature importance from the underlying RF
    rf = final.named_steps["randomforestregressor"]
    feature_names = final.named_steps["columntransformer"].get_feature_names_out()
    order = np.argsort(rf.feature_importances_)[::-1]
    print("\nTop 5 features:")
    for i in order[:5]:
        print(f"  {feature_names[i]:<35s} {rf.feature_importances_[i]:.3f}")


if __name__ == "__main__":
    main()
