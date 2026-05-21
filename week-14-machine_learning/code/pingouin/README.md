# Week 14 Supplement — Pingouin Demo Scripts

> **Companion to**: `../../week-14-pingouin-statistics.md`
> **Pingouin version**: ≥ 0.6 (欄位名使用 underscore：`p_val`, `cohen_d`, `CI95`)

## 檔案清單

| 編號 | 檔名 | 對應講義章節 | 主題 |
|------|------|-------------|------|
| 01 | `01_intro_api.py` | §1 安裝與 API 哲學 | scipy.stats vs. pingouin 對照、APA-style 輸出 |
| 02 | `02_ttest_family.py` | §2 t-test 家族 | paired / independent / one-sample / Wilcoxon / MWU + effect size + normality check |
| 03 | `03_anova.py` | §3 ANOVA | one-way / repeated-measures / mixed ANOVA + post-hoc |
| 04 | `04_correlation.py` | §4 Correlation | Pearson / Spearman / partial corr / correlation matrix |
| 05 | `05_streamlit_stats_app.py` | §5 Streamlit 部署 | 互動式 dashboard（含 sidebar、tabs、CSV download） |

## 環境準備

```bash
# 建議用 conda 或 venv 建立隔離環境
pip install -r requirements.txt
```

## 執行方式

腳本 01–04（純 Python）：

```bash
python 01_intro_api.py
python 02_ttest_family.py
python 03_anova.py
python 04_correlation.py
```

執行後會在 `code/pingouin/figures/` 產生對應 PNG。每一個 statistical test example 都有一張 companion plot，讓學生可以把統計表格與資料型態連在一起看。

腳本 05（Streamlit app）：

```bash
streamlit run 05_streamlit_stats_app.py
# 瀏覽器自動開啟 http://localhost:8501
```

## 部署到 Streamlit Community Cloud

1. 把 `05_streamlit_stats_app.py` 與 `requirements.txt` push 到 GitHub repo。
2. 到 [share.streamlit.io](https://share.streamlit.io)：
   - New app → 選 repo / branch
   - Main file path：`code/pingouin/05_streamlit_stats_app.py`
   - Deploy
3. 取得 public URL，可貼到 supplementary materials 或分享給 collaborator。

## 設計原則

- **每個 script 可獨立執行**：包含完整 `import`、`np.random.seed()`、合成資料。
- **不依賴外部下載**：所有範例資料都用 `np.random` 在 < 1 秒內生成。
- **每個檢定搭配圖形**：t-test / ANOVA / correlation 的輸出表格旁，都要有能顯示資料結構或模型比較邏輯的圖。
- **欄位命名跟隨 pingouin 0.6+**：若你用舊版，請改用 `p-val`, `cohen-d`, `CI95%`。
- **輸出可重現**：所有腳本固定 random seed。

## 常見問題

- **`ImportError: cannot import name 'pingouin'`**：執行 `pip install pingouin>=0.6`。
- **`KeyError: 'p_val'`**：你用了舊版 pingouin（≤ 0.5）；要不升級套件，要不把欄位名改成 `p-val`。
- **Streamlit app 在 cloud 跑很慢**：第一次 build 約 2–3 分鐘（要裝相依套件），之後 cache hit 就很快。

---

*Last updated: 2026-05-21*
