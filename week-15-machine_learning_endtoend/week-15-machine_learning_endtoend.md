# Week 15: End-to-End Machine Learning — 從資料到模型的完整 pipeline

> **Course**: NS5116 電腦硬體與程式語言在行為科學實驗與大數據分析之應用
> **Week**: 15 of 16 | **Date**: 2026-06-04
> **Anchor textbook**: Géron (2023) *Hands-on Machine Learning*, Chapter 2 — [02_end_to_end_machine_learning_project.ipynb](https://github.com/ageron/handson-ml3/blob/main/02_end_to_end_machine_learning_project.ipynb)

---

## Learning Objectives (學習目標)

完成本週後，你能夠：

1. **框架化 (frame)** 一個資料分析問題：判斷它屬於 supervised / unsupervised、regression / classification、batch / online 哪一類。
2. **建立** 一個 reproducible 的 train/test split，並在類別不平衡時使用 `StratifiedShuffleSplit`。
3. **組合** 一個包含 imputation、encoding、scaling 的 `ColumnTransformer` + `Pipeline`，避免 data leakage。
4. **比較** 至少五種 supervised regression algorithm（linear、tree、ensemble、k-NN、kernel SVM），並解釋它們的歸納偏置 (inductive bias)。
5. **使用** k-fold cross-validation 與 `GridSearchCV` / `RandomizedSearchCV` 做模型選擇與 hyperparameter tuning。
6. **辨識** unsupervised 方法（k-means、isolation forest）何時可用於 feature engineering 或 outlier detection。
7. **遷移** 上述 pipeline 到一個行為科學情境（預測 Stroop task 的 reaction time）。

---

## Why This Matters (動機)

你已經會用 PsychoPy 收資料、用 pandas 整理資料、用 Streamlit 展示資料。剩下一個關鍵能力 — **從資料中學到一個可預測的模型**。

舉一個 cogneuro 情境：你在實驗室收集了 200 位受試者的 Stroop task 資料，每個受試者有 60 個 trial，記錄了 stimulus type、congruency、trial number、本次 ISI、上一個 trial 的正確性，以及 reaction time。你想知道：

> 「哪些 trial-level 變項最能預測 RT？而且，能不能用一個 model 在新受試者身上預測他的 RT 分布？」

這正是一個 **supervised regression** 問題。本週我們用 Géron 章節 2 的 California Housing 資料作為 **anchor case**（因為它乾淨、好除錯、文獻充足），把整個 ML pipeline 跑一遍；然後把同樣的 pipeline 套用到上面那個 RT-prediction 問題上。

> **注意**：本週講解的所有 algorithm 都屬於 *shallow learning*（傳統 ML）。Deep learning 的部分留待後續課程或自學。本週的重點是 **pipeline 與 algorithm taxonomy**，而非單一模型的最佳化。

---

## In-Class Topics (課堂內容)

### 1. ML 問題的框架化 (20 min)

在寫任何一行 sklearn code 之前，你必須先回答四個問題：

| 問題 | 選項 | Stroop RT 範例的答案 |
|------|------|----------------------|
| 有沒有 label？ | supervised / unsupervised / semi-supervised | supervised（label = 觀測到的 RT）|
| Label 的型別？ | regression / classification | regression（RT 是連續值）|
| 資料一次給齊嗎？ | batch / online | batch（一次拿到所有受試者）|
| 模型怎麼學？ | instance-based / model-based | model-based（學出一組 coefficient）|

**框架化的重要性**：選錯類型會讓所有後續 metric 變得無意義。例如把 RT (ms) 當成 classification target，你會 silently 失去 ordinal 結構。

#### 🔬 Hands-on Practice 1: 你會怎麼框架化這些問題？

針對下列三個情境，寫出四個框架化問題的答案：

| 情境 |
|------|
| A. 從 EEG 30 秒片段判斷受試者是清醒還是睡著 |
| B. 把 1000 篇 fMRI 論文依「研究主題」自動分群 |
| C. 收到 BIDS 格式的 fMRI dataset，逐筆判斷某張 volume 是否為 motion artifact |

<details>
<summary>✅ 參考解答</summary>

| 情境 | Supervised? | 任務型別 | Batch? | 學習風格 |
|------|------------|----------|--------|----------|
| A | supervised | binary classification | batch | model-based |
| B | unsupervised | clustering | batch | model-based (e.g., k-means) |
| C | 通常 supervised（用 expert-labelled artifact）或 unsupervised（anomaly detection）| binary classification 或 anomaly | 可 online（資料逐張進來） | 兩者皆可 |

</details>

---

### 2. Anchor case — California Housing：取得資料與 EDA (25 min)

我們直接跟著 Géron 的章節跑。資料來源：1990 美國加州人口普查的 block-level 房價。**目標**：給定一個 block 的特徵（人口、收入中位數、經緯度⋯⋯），預測 median house value。

*📄 [`code/ml/01_data_exploration.py`](code/ml/01_data_exploration.py)*
```python
import pandas as pd
from pathlib import Path
import tarfile
import urllib.request

def load_housing_data():
    """下載並讀取 California Housing 資料（首次執行會下載到 datasets/）。"""
    tarball_path = Path("datasets/housing.tgz")
    if not tarball_path.is_file():
        Path("datasets").mkdir(parents=True, exist_ok=True)
        url = "https://github.com/ageron/data/raw/main/housing.tgz"
        urllib.request.urlretrieve(url, tarball_path)
        with tarfile.open(tarball_path) as t:
            t.extractall(path="datasets")
    return pd.read_csv(Path("datasets/housing/housing.csv"))

housing = load_housing_data()
print(housing.shape)        # (20640, 10)
print(housing.info())       # 注意 total_bedrooms 有 missing values
print(housing.describe())
```

#### 2.1 為什麼要先切 test set？

> **黃金法則**：拿到資料的 **第一件事** 是切出 test set，並 **不再看它**。否則你會 silently overfit 到 test set（data snooping bias）。

```python
from sklearn.model_selection import train_test_split

train_set, test_set = train_test_split(housing, test_size=0.2, random_state=42)
```

`random_state=42` 是 reproducibility 的關鍵 — 每次跑都會得到相同的切法。

#### 2.2 Stratified sampling — 當分布不均時

直接 random split 會在 income 這個重要變項上產生 bias。Géron 的做法是把 `median_income` 分成 5 個 bin，然後分層抽樣：

```python
import numpy as np
from sklearn.model_selection import StratifiedShuffleSplit

housing["income_cat"] = pd.cut(
    housing["median_income"],
    bins=[0., 1.5, 3.0, 4.5, 6., np.inf],
    labels=[1, 2, 3, 4, 5],
)

split = StratifiedShuffleSplit(n_splits=1, test_size=0.2, random_state=42)
for train_idx, test_idx in split.split(housing, housing["income_cat"]):
    strat_train = housing.iloc[train_idx]
    strat_test  = housing.iloc[test_idx]

# 驗證分層後的 income_cat 比例與母體一致
print(strat_test["income_cat"].value_counts(normalize=True).sort_index())
print(housing["income_cat"].value_counts(normalize=True).sort_index())
```

**對應到 cogneuro**：如果你的 RT dataset 中年輕人遠多於老人，random split 後 test set 中老人可能只有兩三個。用 age group 做 stratification 才能確保 test set 能反映你想 generalize 的母體。

#### 🔬 Hands-on Practice 2: Stratified split on age

**任務**：給定一個模擬的 RT dataset（n=200，age 範圍 20–80），先用 `pd.cut` 把 age 分成 4 個 bin，再用 `StratifiedShuffleSplit` 切出 20% test set。驗證 train/test 中各 age bin 的比例差異 < 1%。

```python
import numpy as np
import pandas as pd
np.random.seed(42)

df = pd.DataFrame({
    "age": np.random.uniform(20, 80, 200),
    "rt":  np.random.normal(500, 80, 200),
})
# 你的程式碼從這裡開始
```

<details>
<summary>✅ 參考解答</summary>

```python
from sklearn.model_selection import StratifiedShuffleSplit

df["age_bin"] = pd.cut(df["age"], bins=[20, 35, 50, 65, 80], labels=[1, 2, 3, 4])

split = StratifiedShuffleSplit(n_splits=1, test_size=0.2, random_state=42)
for tr, te in split.split(df, df["age_bin"]):
    train, test = df.iloc[tr], df.iloc[te]

prop_full  = df["age_bin"].value_counts(normalize=True).sort_index()
prop_test  = test["age_bin"].value_counts(normalize=True).sort_index()
print(pd.DataFrame({"full": prop_full, "test": prop_test, "diff": (prop_test - prop_full).abs()}))
```

</details>

---

### 3. Data Preparation Pipeline (30 min)

**核心觀念**：所有 preprocessing 步驟都要 **fit on train, transform on test**。否則就是 data leakage。`sklearn.pipeline.Pipeline` 與 `ColumnTransformer` 是強制你遵守這條規則的工具。

#### 3.1 Imputation — 處理 missing values

`total_bedrooms` 有 207 筆缺值。三種選擇：

```python
# Option A: drop rows
housing.dropna(subset=["total_bedrooms"])
# Option B: drop column
housing.drop("total_bedrooms", axis=1)
# Option C: impute（推薦 — 不丟資料、不丟欄位）
from sklearn.impute import SimpleImputer
imputer = SimpleImputer(strategy="median")
```

#### 3.2 Encoding categorical attributes

`ocean_proximity` 是文字。兩種轉換方式：

| 方法 | 適用情境 | 缺點 |
|------|----------|------|
| `OrdinalEncoder` | 類別有自然順序（low/medium/high）| 強加順序到無序類別會誤導模型 |
| `OneHotEncoder` | 無序類別（最安全的預設）| 類別數很多時會產生 sparse 高維特徵 |

```python
from sklearn.preprocessing import OneHotEncoder
cat_encoder = OneHotEncoder(sparse_output=False)
X_cat_1hot = cat_encoder.fit_transform(housing[["ocean_proximity"]])
print(cat_encoder.categories_)
```

#### 3.3 Feature scaling

**為什麼要 scaling**：基於距離的演算法（k-NN、SVM、k-means）與用 gradient 的演算法（linear regression with gradient descent、neural net）對 feature 的 scale 極度敏感。Tree-based 演算法則 **不需要** scaling。

```python
from sklearn.preprocessing import StandardScaler, MinMaxScaler
std_scaler = StandardScaler()   # → mean=0, std=1
mm_scaler  = MinMaxScaler()     # → [0, 1]
```

#### 3.4 把所有步驟串成 Pipeline

```python
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.impute import SimpleImputer

num_attribs = ["longitude", "latitude", "housing_median_age",
               "total_rooms", "total_bedrooms", "population",
               "households", "median_income"]
cat_attribs = ["ocean_proximity"]

num_pipeline = Pipeline([
    ("imputer", SimpleImputer(strategy="median")),
    ("scaler", StandardScaler()),
])

full_pipeline = ColumnTransformer([
    ("num", num_pipeline, num_attribs),
    ("cat", OneHotEncoder(handle_unknown="ignore"), cat_attribs),
])

X_train_prepared = full_pipeline.fit_transform(strat_train.drop("median_house_value", axis=1))
print(X_train_prepared.shape)
```

**常見錯誤**：
- ❌ 對 train + test 一起 `fit_transform()` → 把 test 的 statistics 偷渡進 train
- ✅ 對 train 用 `fit_transform()`，對 test 用 `transform()`（pipeline 自動處理）

#### 🔬 Hands-on Practice 3: 把 RT data 套進 pipeline

**情境**：你有一個 trial-level dataframe，欄位含 `congruency`（字串）、`isi`（毫秒，連續，有 missing）、`block_num`（整數）、`rt`（target）。請寫一個 `ColumnTransformer` 處理這三個 feature。

```python
import pandas as pd
import numpy as np
np.random.seed(42)
df = pd.DataFrame({
    "congruency": np.random.choice(["congruent", "incongruent"], 100),
    "isi":        np.random.choice([500, 1000, 1500, np.nan], 100),
    "block_num":  np.random.choice([1, 2, 3], 100),
    "rt":         np.random.normal(500, 80, 100),
})
# 你的程式碼從這裡開始
```

<details>
<summary>✅ 參考解答</summary>

```python
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder

num_pipe = Pipeline([
    ("imp", SimpleImputer(strategy="median")),
    ("sc",  StandardScaler()),
])

prep = ColumnTransformer([
    ("num", num_pipe, ["isi", "block_num"]),
    ("cat", OneHotEncoder(), ["congruency"]),
])

X = prep.fit_transform(df.drop("rt", axis=1))
print("Shape:", X.shape, "(expect 100 rows × 4 cols: isi, block, 2 onehot)")
```

</details>

---

### 4. Supervised Regression — 演算法動物園 (40 min)

現在我們有了乾淨的 `X_train_prepared` 與 `y_train`。同一份資料可以餵給很多 algorithm。本節用 **同一個 evaluation protocol（10-fold CV RMSE）** 比較五大類 algorithm。

#### 4.1 Algorithm taxonomy 速覽

| 類別 | 範例 | 歸納偏置 (inductive bias) | 何時用 |
|------|------|--------------------------|--------|
| **Linear (parametric)** | `LinearRegression`, `Ridge`, `Lasso` | target 是 feature 的線性組合 | baseline；feature 與 target 接近線性時 |
| **Instance-based** | `KNeighborsRegressor` | 鄰近的 sample 有相似 target | 區域結構強、訓練資料密集時 |
| **Tree-based** | `DecisionTreeRegressor` | target 是 feature 空間的 axis-aligned 分割 | feature interaction 強、可解釋性需求高 |
| **Ensemble** | `RandomForestRegressor`, `GradientBoosting` | 多個 weak learner 投票/平均 | 幾乎永遠是 tabular data 的最強 baseline |
| **Kernel methods** | `SVR(kernel='rbf')` | 在 high-dim feature space 找 margin-maximizing hyperplane | 中等資料量、非線性結構 |

> **延伸閱讀**：deep learning 屬於另一類 *representation learning*，本週不涵蓋。

#### 4.2 統一的訓練與評估

*📄 [`code/ml/03_regression_zoo.py`](code/ml/03_regression_zoo.py)*
```python
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.neighbors import KNeighborsRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.svm import SVR
from sklearn.model_selection import cross_val_score
from sklearn.pipeline import make_pipeline

models = {
    "Linear":        LinearRegression(),
    "k-NN (k=5)":    KNeighborsRegressor(n_neighbors=5),
    "DecisionTree":  DecisionTreeRegressor(random_state=42),
    "RandomForest":  RandomForestRegressor(n_estimators=100, random_state=42, n_jobs=-1),
    "SVR (RBF)":     SVR(kernel="rbf", C=10, gamma=0.1),
}

# 對每個 model 跑 5-fold CV 的 negative RMSE
results = {}
for name, model in models.items():
    # 假設 full_pipeline 已經 fit 過
    pipe = make_pipeline(full_pipeline, model)
    scores = cross_val_score(
        pipe, strat_train.drop("median_house_value", axis=1),
        strat_train["median_house_value"],
        scoring="neg_root_mean_squared_error", cv=5, n_jobs=-1,
    )
    results[name] = -scores
    print(f"{name:15s}  RMSE = {(-scores).mean():.0f} ± {scores.std():.0f}")
```

**典型輸出**（housing dataset，價格單位 USD）：

```
Linear           RMSE = 68628 ± 1500
k-NN (k=5)       RMSE = 56500 ± 1200
DecisionTree     RMSE = 69100 ± 2200   ← 純 tree 在 tabular 上容易 overfit
RandomForest     RMSE = 49500 ± 800    ← ensemble 修掉 single tree 的高 variance
SVR (RBF)        RMSE = 68000 ± 1100   ← 沒調 C/gamma 時通常不會贏
```

**關鍵觀察**：
1. RandomForest 幾乎總是比 DecisionTree 好（bias–variance tradeoff）。
2. Linear 與 SVR 的差異反映 **資料的線性度**。
3. k-NN 的表現高度依賴 feature scaling — 沒做 scaling 時 latitude (±90) 會壓過 income (~3) 的距離貢獻。

#### 4.3 Bias–Variance Tradeoff 視覺化

```
high bias                                           high variance
LinearRegression  <--  Ridge  <--  RandomForest  <--  DecisionTree (深)
(underfit)                                              (overfit)
```

選 model 不是「選最強的」而是「在 bias 與 variance 之間找平衡」。Ensemble 之所以強，是因為它用「多個 high-variance learner 平均」來降 variance 而不增加 bias。

#### 🔬 Hands-on Practice 4: 加一個 model 到比較表

**任務**：把 `Ridge(alpha=1.0)` 與 `GradientBoostingRegressor(n_estimators=100)` 加入上面的比較。哪一個 RMSE 較低？解釋為什麼 ensemble 通常贏 single tree。

<details>
<summary>✅ 參考解答（程式架構）</summary>

```python
from sklearn.linear_model import Ridge
from sklearn.ensemble import GradientBoostingRegressor

extra = {
    "Ridge (α=1)":        Ridge(alpha=1.0),
    "GradientBoosting":   GradientBoostingRegressor(n_estimators=100, random_state=42),
}
for name, model in extra.items():
    pipe = make_pipeline(full_pipeline, model)
    scores = -cross_val_score(pipe, X_full, y, scoring="neg_root_mean_squared_error", cv=5)
    print(f"{name:20s}  RMSE = {scores.mean():.0f} ± {scores.std():.0f}")
```

**解釋**：`GradientBoosting` 依序訓練多個 shallow tree，每棵 tree 學前一棵的 residual，從 bias-heavy 走向 low-bias；而 RandomForest 用 bagging 平行訓練 deep tree 來降 variance。兩者都比 single tree 強，但走的是不同的路徑。

</details>

---

### 5. Model Evaluation & Hyperparameter Tuning (25 min)

#### 5.1 為什麼不能用 train accuracy 比較 model

```python
# WRONG — 在 train set 上算 RMSE，所有 model 都會「看起來很強」
LinearRegression().fit(X_train, y_train).score(X_train, y_train)
```

`DecisionTree(max_depth=None)` 在 train set 上的 RMSE 會接近 0，但在 test 上爛透了 — 它記住了所有 noise。

#### 5.2 K-Fold Cross-Validation

```
資料                [===========================================]
fold 1   test→[==]  train→[=====================================]
fold 2   test→    [==]  train→[=================================]
fold 3   test→        [==]  train→[=============================]
...
```

```python
from sklearn.model_selection import cross_val_score

scores = cross_val_score(
    model, X, y, cv=5, scoring="neg_root_mean_squared_error", n_jobs=-1,
)
print(f"RMSE: {-scores.mean():.0f} ± {scores.std():.0f}")
```

#### 5.3 Grid Search vs. Random Search

```python
from sklearn.model_selection import GridSearchCV, RandomizedSearchCV
from scipy.stats import randint

# Grid: 窮舉所有組合 — n_estimators × max_features = 3 × 4 = 12 fits/fold
param_grid = [
    {"n_estimators": [3, 30, 100], "max_features": [2, 4, 6, 8]},
]
grid = GridSearchCV(RandomForestRegressor(random_state=42),
                    param_grid, cv=5,
                    scoring="neg_root_mean_squared_error", n_jobs=-1)

# Random: 在分布上抽 n_iter 次，連續 hyperparameter 更靈活
param_dist = {"n_estimators": randint(10, 300), "max_features": randint(2, 8)}
rand = RandomizedSearchCV(RandomForestRegressor(random_state=42),
                          param_dist, n_iter=20, cv=5,
                          scoring="neg_root_mean_squared_error", n_jobs=-1)
```

**經驗法則**：
- < 4 個 hyperparameter 且每個值不多 → `GridSearchCV`
- 連續 hyperparameter、或值很多 → `RandomizedSearchCV`
- 預算極度有限 → `HalvingRandomSearchCV`（successive halving）

#### 5.4 最終 test set 評估 — 只能做一次

```python
final_model = rand.best_estimator_
X_test  = strat_test.drop("median_house_value", axis=1)
y_test  = strat_test["median_house_value"]
final_rmse = root_mean_squared_error(y_test, final_model.predict(X_test))
```

**常見錯誤**：對 test set 看了結果後又回去調 hyperparameter — 等於把 test set 變成 train set 的一部分。如果 test RMSE 不滿意，**接受它**，並把這個結果寫進 limitation。

---

### 6. Unsupervised 小品 (15 min)

雖然本週主軸是 supervised，但 unsupervised 方法常作為 **feature engineering 工具** 或 **outlier filter** 出現在 pipeline 裡。

#### 6.1 K-Means：把 geography 變成 cluster feature

Géron 原 notebook 用 k-means 把 (latitude, longitude) 聚成 10 個 cluster，然後計算每個 sample 到每個 cluster centroid 的 RBF 相似度作為 10 個新 feature。

```python
from sklearn.cluster import KMeans
from sklearn.metrics.pairwise import rbf_kernel
from sklearn.base import BaseEstimator, TransformerMixin

class ClusterSimilarity(BaseEstimator, TransformerMixin):
    def __init__(self, n_clusters=10, gamma=1.0, random_state=None):
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
```

**Cogneuro 類比**：對 fMRI ROI time series 做 k-means 找出「functional clusters」，再以每個 voxel 與 cluster centroid 的相似度作為 feature。

#### 6.2 Isolation Forest：偵測異常 trial

```python
from sklearn.ensemble import IsolationForest
iso = IsolationForest(contamination=0.05, random_state=42)
outlier_mask = iso.fit_predict(X_train) == -1  # -1 表示 outlier
```

比 mean ± 3 SD 更穩健 — IsolationForest 能找到 **多變量** outlier（單看每個 feature 都正常，但組合起來很奇怪的 sample）。在 RT 分析中，這對抓出「正確但太快、或太慢但 motor preparation 異常」的 trial 很有用。

---

### 7. 把 pipeline 套到 RT-prediction 問題 (25 min)

*📄 [`code/ml/06_cogneuro_rt_pipeline.py`](code/ml/06_cogneuro_rt_pipeline.py)*

合成一個 Stroop-like dataset，然後用今天學的所有工具跑一遍：

```python
import numpy as np
import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.model_selection import StratifiedShuffleSplit, cross_val_score
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression

np.random.seed(42)

# ---- 1. 模擬資料：6000 個 trial × 200 受試者 -----------------------------
n_subj, n_trial = 200, 30
records = []
for sid in range(n_subj):
    age = np.random.uniform(20, 75)
    for t in range(n_trial):
        congruent = np.random.rand() < 0.5
        isi = np.random.choice([400, 800, 1200])
        # 真實生成式：RT = baseline + age_effect + congruency_effect + ISI_effect + noise
        rt = (
            350 + 2.0 * (age - 45)
            + (0 if congruent else 60)
            - 0.02 * isi
            + np.random.normal(0, 40)
        )
        records.append((sid, age, congruent, isi, t, rt))

df = pd.DataFrame(records, columns=["sid", "age", "congruent", "isi", "trial_num", "rt"])

# ---- 2. Stratified split by age group -------------------------------------
df["age_bin"] = pd.cut(df["age"], bins=[20, 35, 50, 65, 75], labels=[1, 2, 3, 4])
split = StratifiedShuffleSplit(n_splits=1, test_size=0.2, random_state=42)
for tr_idx, te_idx in split.split(df, df["age_bin"]):
    train_df, test_df = df.iloc[tr_idx], df.iloc[te_idx]

# ---- 3. Pipeline ----------------------------------------------------------
num_attribs = ["age", "isi", "trial_num"]
cat_attribs = ["congruent"]
prep = ColumnTransformer([
    ("num", Pipeline([("imp", SimpleImputer(strategy="median")),
                      ("sc",  StandardScaler())]), num_attribs),
    ("cat", OneHotEncoder(), cat_attribs),
])

# ---- 4. Algorithm zoo on cogneuro data -----------------------------------
from sklearn.pipeline import make_pipeline
X_tr = train_df[num_attribs + cat_attribs]
y_tr = train_df["rt"]

for name, model in [("Linear", LinearRegression()),
                    ("RandomForest", RandomForestRegressor(n_estimators=100,
                                                           random_state=42, n_jobs=-1))]:
    pipe = make_pipeline(prep, model)
    rmse = -cross_val_score(pipe, X_tr, y_tr, cv=5,
                            scoring="neg_root_mean_squared_error", n_jobs=-1)
    print(f"{name:15s}  RMSE = {rmse.mean():.1f} ± {rmse.std():.1f} ms")
```

**預期結果**：因為合成過程本身是線性的，`LinearRegression` 與 `RandomForest` 應該差不多（甚至 linear 略勝），這正是 **「最強的 model 取決於資料的真實結構」** 的活生生例子。

#### 🔬 Hands-on Practice 5（課堂收尾）

**任務**：把上面合成資料中的 `congruency × age` 互動項加入真實生成式（例如老年人受 incongruent trial 影響更大）。重新訓練，這次哪個 model 贏？

<details>
<summary>💡 提示</summary>

修改 rt 公式為 `+ (0 if congruent else 60 + 1.5 * (age - 45))`。Tree-based 與 ensemble 會比 linear 更能 capture interaction。

</details>

---

## Recap & Common Pitfalls (重點回顧與常見錯誤)

✅ **記住的**：
- 先 **frame** 再 code；先 **切 test set** 再 EDA。
- `Pipeline` 是 leakage 防火牆。
- 用 CV 比較 model，不用 train accuracy。
- Test set 只能評估一次。
- Ensemble (RandomForest, GradientBoosting) 是 tabular data 的強力 baseline。

❌ **常見錯誤**：
| 錯誤 | 後果 | 修正 |
|------|------|------|
| 對 train+test 一起 fit StandardScaler | data leakage，test RMSE 過於樂觀 | 用 Pipeline，對 train `fit_transform`、對 test `transform` |
| 反覆調參直到 test 變好 | test 變成 train 的一部分 | 嚴格分 validation set，或用 nested CV |
| OneHot 後忘了 `handle_unknown='ignore'` | test 出現新類別時程式 crash | 加 `handle_unknown="ignore"` |
| Tree-based model 還做 StandardScaler | 沒影響，但浪費計算 | 對 RF/GBM 可省略 scaling |
| 用 R² 比 regression model | R² 對 outlier 敏感且難解釋單位 | 用 RMSE（與 target 同單位）|

---

## Homework (作業)

詳見 [`week-15-homework.md`](week-15-homework.md)。

**摘要**：給定一份合成的 Flanker task RT dataset（提供下載 URL），套用本週學的整套 pipeline：
1. EDA + stratified train/test split
2. 至少三個 algorithm 的 CV 比較
3. 對最佳 model 做 `RandomizedSearchCV`
4. 報告 final test RMSE 與 feature importance
5. 一頁 Markdown 報告

**繳交格式**：`.ipynb` + 一份 Markdown 報告 `report.md`。

**Rubric (簡要)**：
- Reproducibility（seed、pipeline、無 leakage）：30%
- 至少三類 algorithm 正確比較：25%
- Hyperparameter tuning 有正確 CV：20%
- 對結果的解釋（哪個 model 贏、為什麼）：15%
- Code quality（commented、可重跑）：10%

---

## 參考資源 (References)

- Géron, A. (2023). *Hands-on Machine Learning with Scikit-Learn, Keras, and TensorFlow* (3rd ed.). O'Reilly. Chapter 2.
  - GitHub repo: <https://github.com/ageron/handson-ml3>
- Scikit-learn user guide — Cross-validation: <https://scikit-learn.org/stable/modules/cross_validation.html>
- Scikit-learn user guide — Preprocessing: <https://scikit-learn.org/stable/modules/preprocessing.html>
- Hastie, Tibshirani, & Friedman (2009). *The Elements of Statistical Learning*. — bias–variance 數學細節。
- Varoquaux & Cheplygina (2022). Machine learning for medical imaging: methodological failures and recommendations for the future. *npj Digital Medicine*, 5(48). — 講 ML 在 neuroimaging 上的常見錯誤，必讀。

---

*最後更新：2026-05-25*
