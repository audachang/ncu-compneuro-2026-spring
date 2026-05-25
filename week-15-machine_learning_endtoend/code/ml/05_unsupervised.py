"""Week 15 - Step 5: Unsupervised methods as feature engineering / outlier tools.

- KMeans on (latitude, longitude) -> RBF similarity features
- IsolationForest to flag multivariate outliers

Run:
    python 05_unsupervised.py
"""
import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.cluster import KMeans
from sklearn.ensemble import IsolationForest
from sklearn.metrics.pairwise import rbf_kernel

from importlib import import_module
load = import_module("01_data_exploration").load_housing_data
stratified_split = import_module("02_preprocessing_pipeline").stratified_split


class ClusterSimilarity(BaseEstimator, TransformerMixin):
    """Replace (x, y) coords with similarity to n_clusters learned centroids."""

    def __init__(self, n_clusters: int = 10, gamma: float = 1.0,
                 random_state: int | None = None):
        self.n_clusters = n_clusters
        self.gamma = gamma
        self.random_state = random_state

    def fit(self, X, y=None, sample_weight=None):
        self.kmeans_ = KMeans(n_clusters=self.n_clusters,
                              random_state=self.random_state, n_init=10)
        self.kmeans_.fit(X, sample_weight=sample_weight)
        return self

    def transform(self, X):
        return rbf_kernel(X, self.kmeans_.cluster_centers_, gamma=self.gamma)

    def get_feature_names_out(self, names=None):
        return [f"cluster_{i}_sim" for i in range(self.n_clusters)]


def main() -> None:
    housing = load()
    train, _ = stratified_split(housing)
    coords = train[["longitude", "latitude"]].to_numpy()

    # --- KMeans -> cluster similarity features ------------------------------
    cs = ClusterSimilarity(n_clusters=10, gamma=1.0, random_state=42).fit(coords)
    sim = cs.transform(coords[:5])
    print("Cluster similarity for first 5 rows (10 clusters):")
    print(np.round(sim, 3))

    # --- IsolationForest ----------------------------------------------------
    num_cols = ["housing_median_age", "total_rooms", "total_bedrooms",
                "population", "households", "median_income"]
    X_num = train[num_cols].dropna()
    iso = IsolationForest(contamination=0.05, random_state=42).fit(X_num)
    flags = iso.predict(X_num)
    print(f"\nIsolationForest flagged {(flags == -1).sum()} / {len(flags)} rows "
          f"as outliers ({(flags == -1).mean():.1%}).")


if __name__ == "__main__":
    main()
