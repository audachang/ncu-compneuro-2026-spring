"""Week 15 - Step 6: Apply the housing-style pipeline to a synthetic
Stroop-task RT dataset.

The point: the same ML pipeline is domain-agnostic.

Run:
    python 06_cogneuro_rt_pipeline.py
"""
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestRegressor
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LinearRegression
from sklearn.metrics import root_mean_squared_error
from sklearn.model_selection import (StratifiedShuffleSplit, cross_val_score)
from sklearn.pipeline import Pipeline, make_pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler


def simulate_stroop(n_subj: int = 200, n_trial: int = 30,
                    interaction: bool = False, seed: int = 42) -> pd.DataFrame:
    """Generate trial-level Stroop RT data with realistic effects.

    If ``interaction=True``, older subjects show a larger congruency effect —
    which RandomForest can capture but linear regression cannot.
    """
    rng = np.random.default_rng(seed)
    rows = []
    for sid in range(n_subj):
        age = rng.uniform(20, 75)
        for t in range(n_trial):
            congruent = rng.random() < 0.5
            isi = rng.choice([400, 800, 1200])
            cong_effect = 0 if congruent else 60
            if interaction and not congruent:
                # Strong age × congruency interaction — RF should beat linear here
                cong_effect += 4.0 * (age - 45)
            rt = (
                350
                + 2.0 * (age - 45)
                + cong_effect
                - 0.02 * isi
                + rng.normal(0, 40)
            )
            rows.append((sid, age, congruent, isi, t, rt))
    return pd.DataFrame(rows, columns=["sid", "age", "congruent",
                                       "isi", "trial_num", "rt"])


def stratified_split_by_age(df: pd.DataFrame, test_size: float = 0.2,
                             seed: int = 42) -> tuple[pd.DataFrame, pd.DataFrame]:
    df = df.copy()
    df["age_bin"] = pd.cut(df["age"], bins=[20, 35, 50, 65, 75],
                           labels=[1, 2, 3, 4])
    sss = StratifiedShuffleSplit(n_splits=1, test_size=test_size, random_state=seed)
    for tr, te in sss.split(df, df["age_bin"]):
        return df.iloc[tr].drop("age_bin", axis=1), df.iloc[te].drop("age_bin", axis=1)


def build_rt_pipeline() -> ColumnTransformer:
    num = ["age", "isi", "trial_num"]
    cat = ["congruent"]
    num_pipe = Pipeline([("imp", SimpleImputer(strategy="median")),
                         ("sc",  StandardScaler())])
    return ColumnTransformer([("num", num_pipe, num),
                              ("cat", OneHotEncoder(), cat)])


def evaluate(X, y, models: dict, prep) -> None:
    print(f"{'Model':<18} {'CV RMSE (ms)':>14}")
    print("-" * 34)
    for name, model in models.items():
        pipe = make_pipeline(prep, model)
        rmse = -cross_val_score(pipe, X, y, cv=5,
                                scoring="neg_root_mean_squared_error",
                                n_jobs=-1)
        print(f"{name:<18} {rmse.mean():>10.1f} ± {rmse.std():>2.1f}")


def main() -> None:
    for tag, interaction in [("LINEAR DGP", False), ("INTERACTION DGP", True)]:
        print(f"\n=== {tag} ===")
        df = simulate_stroop(interaction=interaction)
        train, test = stratified_split_by_age(df)
        X_tr = train[["age", "isi", "trial_num", "congruent"]]
        y_tr = train["rt"]

        prep = build_rt_pipeline()
        models = {
            "Linear":       LinearRegression(),
            "RandomForest": RandomForestRegressor(n_estimators=200, random_state=42, n_jobs=-1),
        }
        evaluate(X_tr, y_tr, models, prep)

        # Final test eval with RF
        final = make_pipeline(prep, models["RandomForest"]).fit(X_tr, y_tr)
        X_te = test[["age", "isi", "trial_num", "congruent"]]
        test_rmse = root_mean_squared_error(test["rt"], final.predict(X_te))
        print(f"RF test RMSE: {test_rmse:.1f} ms")


if __name__ == "__main__":
    main()
