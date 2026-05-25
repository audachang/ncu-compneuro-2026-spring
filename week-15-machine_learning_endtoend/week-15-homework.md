# Week 15 Homework — End-to-End ML on a Synthetic Flanker Task

> **Due**: 2026-06-11 23:59 (上傳至 eeclass)
> **Format**: 一個 `.ipynb` + 一個 `report.md`（總共 ≤ 4 頁 PDF 也可接受）
> **Anchor**: Géron Chapter 2 pipeline，套用到一個新的 cogneuro dataset

---

## 情境

你接手了實驗室的一份 Flanker task 行為資料。每位受試者完成 80 個 trial，trial-level 變項包括：

| 欄位 | 型別 | 說明 |
|------|------|------|
| `subject_id` | int | 受試者編號（1 – 250）|
| `age` | float | 年齡（20 – 80）|
| `group` | str | `young` / `middle` / `older`（依 age 分） |
| `congruency` | str | `congruent` / `incongruent` / `neutral` |
| `flanker_distance` | int | flanker 與 target 距離（度，連續）|
| `trial_num` | int | 1 – 80 |
| `prev_correct` | bool | 上一個 trial 是否正確 |
| `isi` | int | 毫秒，有部分 missing |
| `rt` | float | reaction time (ms) — **target** |
| `correct` | bool | 該 trial 是否正確 |

**生成資料**：用下方的 `simulate_flanker()` 函式產生 dataset（**不要**自己亂改參數，否則 grading 會對不上）。

```python
import numpy as np
import pandas as pd

def simulate_flanker(seed: int = 2026) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    rows = []
    for sid in range(1, 251):
        age = rng.uniform(20, 80)
        group = "young" if age < 40 else ("middle" if age < 60 else "older")
        for t in range(1, 81):
            cong = rng.choice(["congruent", "incongruent", "neutral"],
                              p=[0.4, 0.4, 0.2])
            dist = rng.choice([1, 2, 3])
            prev_correct = bool(rng.random() < 0.92)
            isi = rng.choice([300, 600, 900, np.nan], p=[0.3, 0.3, 0.3, 0.1])

            base = 380 + 1.8 * (age - 40)
            cong_effect = {"congruent": 0, "neutral": 25, "incongruent": 70}[cong]
            if cong == "incongruent":
                cong_effect += 1.2 * max(age - 50, 0)  # age × congruency interaction
            dist_effect = -15 * dist
            slow_after_error = 0 if prev_correct else 40
            isi_effect = 0 if np.isnan(isi) else -0.015 * isi

            rt = (base + cong_effect + dist_effect + slow_after_error
                  + isi_effect + rng.normal(0, 45))
            correct = bool(rng.random() < 0.96 - 0.02 * (cong == "incongruent"))
            rows.append((sid, age, group, cong, dist, t, prev_correct,
                         isi, rt, correct))
    return pd.DataFrame(rows, columns=[
        "subject_id", "age", "group", "congruency", "flanker_distance",
        "trial_num", "prev_correct", "isi", "rt", "correct",
    ])

df = simulate_flanker()
```

---

## 任務 (Tasks)

### Task 1 — EDA + train/test split (10%)

1. 描述 dataset：n trials、n subjects、各 group 的 n、`rt` 分布、`isi` 的 missing rate。
2. **剔除 `correct == False` 的 trial**（標準 RT 分析慣例）。
3. 用 `StratifiedShuffleSplit` 切 20% test set，**stratify on `group`**。
4. 報告 train/test 中各 group 的 trial 數。

### Task 2 — Pipeline 設計 (15%)

建立一個 `ColumnTransformer` + `Pipeline`：
- Numeric features (`age`, `flanker_distance`, `trial_num`, `isi`)：median impute + StandardScaler
- Categorical (`congruency`, `group`)：OneHotEncoder（`handle_unknown="ignore"`）
- Boolean (`prev_correct`)：直接 pass-through 為 0/1

> **注意**：不要把 `subject_id` 當 feature（會 leak）。也不要把 `correct` 留下來。

### Task 3 — Algorithm comparison (25%)

至少比較 **三個 algorithm 類別**，每類選一個代表：

- Linear / Regularized: `LinearRegression` 或 `Ridge`
- Tree-based / Ensemble: `RandomForestRegressor` 或 `GradientBoostingRegressor`
- 第三類自選：`KNeighborsRegressor` 或 `SVR(kernel='rbf')`（注意 SVR 慢，subsample 至 ≤ 3000 rows）

對每個 model 用 **5-fold CV** 報告 mean ± std RMSE（單位：ms）。把結果畫成 bar plot。

### Task 4 — Hyperparameter tuning (20%)

對 Task 3 中 CV RMSE 最低的 model，用 `RandomizedSearchCV(n_iter ≥ 10, cv=3)` 調至少 **2 個 hyperparameter**。報告 best params 與 best CV RMSE。

### Task 5 — Final test eval (10%)

用 tuned best model 在 **test set** 上做 **一次** prediction，報告 test RMSE。

### Task 6 — Feature importance + interpretation (10%)

- 若 best model 是 tree-based：用 `feature_importances_`。
- 若為 linear：用標準化後的 coefficient absolute value。

回答（在 `report.md` 中）：
1. Top-3 feature 是什麼？是否符合「我們知道 Flanker 應該怎麼受到 age × congruency × distance 影響」的先驗？
2. 哪個 feature 表現出乎意料？為什麼？

### Task 7 — 一頁 Markdown 報告 (10%)

`report.md` 須包含：
- **Method**: 200 字內描述 pipeline、algorithm、CV 設定、tuning 範圍。
- **Results**: CV bar plot、tuning 結果、test RMSE。
- **Discussion**: feature importance 解釋、limitation（為什麼不能 generalize 到真人資料？至少寫兩個 reason）。

---

## Rubric 細節

| 項目 | 配分 |
|------|------|
| Reproducibility（seed、pipeline、無 leakage） | 15 |
| EDA + stratified split 正確 | 10 |
| Pipeline 結構正確（含 boolean pass-through） | 15 |
| 至少三類 algorithm 正確比較 + CV 視覺化 | 20 |
| Hyperparameter tuning 流程正確 | 15 |
| Test set 只評估一次、報告 final RMSE | 5 |
| Feature importance 解釋合理 | 10 |
| Report 結構完整、有 limitation 討論 | 10 |

**Bonus (+5)**：在 pipeline 中加入一個 custom `TransformerMixin`（例如算 `prev_rt`、`block_within_subject` 或剔除 multivariate outliers 的 step），並說明動機。

---

## 常見扣分點

- ❌ 對 train + test 一起 `fit_transform` → 扣 15 分（嚴重 leakage）
- ❌ 看完 test RMSE 後回頭調 hyperparameter 又重跑 → 扣 10 分
- ❌ 直接用 `df.fillna(df.mean())` 而非 pipeline 內的 imputer → 扣 5 分
- ❌ 用 R² 報告而非 RMSE → 扣 5 分
- ❌ 完全不寫 limitation → 扣 10 分

---

## 提示

- 整個 pipeline 寫完後，跑一遍 `pipe.fit(X_tr, y_tr)` 應該在 30 秒內完成（除非用 SVR 沒 subsample）。
- 如果 RandomForest CV RMSE > 60 ms，可能是 feature engineering 哪裡漏了 — 檢查 `prev_correct` 有沒有被正確 encode。
- 真實 RT 資料應該還會用 mixed-effects model 處理 subject-level random effect — 本作業 **不**要求做這層，但在 limitation 段落要提到。

---

*最後更新：2026-05-25*
