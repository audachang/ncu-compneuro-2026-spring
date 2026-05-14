# Week 12 Demo Scripts

> Runnable demos that accompany `week-12-slides.pptx`.
> 每個 demo 都對應講義中特定的幾張投影片。

## 目錄

```
demo/
├── README.md                       ← 本檔案
├── data/
│   ├── generate_messy_stroop.py    Stroop messy dataset 生成器
│   └── messy_stroop.csv            n=200，故意 messy 的合成資料
├── 00_week11_app/                  Week 11 整合 dashboard（繁體中文註解版）
│   ├── app.py                      七大區塊逐段註解，對應 slides 7–21
│   ├── app_no_cache.py             對照組：load_data() 沒有 @st.cache_data
│   ├── app_with_cache.py           實驗組：加 @st.cache_data；頁面內建計時器
│   ├── data/cognitive_aging_taiwan.csv
│   └── requirements.txt
├── 01_cache_data/
│   ├── cache_demo.py               觀察 @st.cache_data 的行為差異
│   └── pitfalls.py                 三種常見錯誤（widget 在內 / Unhashable / side effects）
├── 02_cache_vs_resource/
│   └── compare.py                  cache_data vs cache_resource 的 reference vs copy 對比
└── 03_pipeline/
    ├── pipeline.py                 load → describe → clean → analyse 完整 pipeline
    └── test_clean.py               pytest — 驗證 clean() 的行為
```

## 對應投影片

| 投影片 | Demo |
|------|------|
| Slides 7–8 (app.py 拆解) + Hands-on 1 (slide 10) | `00_week11_app/app.py`（繁中註解版）|
| Slide 9 (Sidebar) | `00_week11_app/app.py` 區塊 4 |
| Slides 11–13 (rerun model + cache 核心範例) — 並排比較 | `00_week11_app/app_no_cache.py` 與 `app_with_cache.py` |
| Slides 13–16 (caching 深入解析) + Hands-on 2 (slide 19) | `01_cache_data/cache_demo.py` |
| Slides 17–18 (Pitfall 1, 2 & 3) | `01_cache_data/pitfalls.py` |
| Slides 20–21 (`cache_data` vs `cache_resource`) | `02_cache_vs_resource/compare.py` |
| Slides 25 (pipeline diagram), 28–37 (descriptive stats → fixing → end-to-end) | `03_pipeline/pipeline.py` |
| Hands-on 4 (slide 31) — 觀察 messy data | `data/messy_stroop.csv` |
| Hands-on 5 (slide 36) — 寫 `clean_stroop(df)` | `03_pipeline/pipeline.py::clean` 參考實作 |
| Homework rubric test 要求 | `03_pipeline/test_clean.py` 參考實作 |

## 執行方式

### Python (命令列)
```bash
cd 03_pipeline
python pipeline.py
PATH=$HOME/.local/bin:$PATH pytest test_clean.py -v
```

### Streamlit
```bash
# Week 11 整合 app（繁中註解版）— 課堂上拿來逐段解說
cd 00_week11_app
pip install -r requirements.txt
streamlit run app.py

# ⭐ 並排比較 — 開兩個 terminal，看頁面內建的計時器
streamlit run app_no_cache.py     --server.port 8501
streamlit run app_with_cache.py   --server.port 8502

# Caching 系列 demo
cd ../01_cache_data
streamlit run cache_demo.py
streamlit run pitfalls.py

cd ../02_cache_vs_resource
streamlit run compare.py
```

## 重生 messy data

如果 `data/messy_stroop.csv` 不見了或想要不同的 seed：

```bash
cd data
python generate_messy_stroop.py
```

## 設計原則（給看程式碼的學生）

1. **每支 demo 一個明確的觀察目標** — 不堆砌功能。
2. **故意把 cleaning 與 analysis 分開** — `clean()` 完全 deterministic、
   `analyse()` 接受 `outlier_sd` 參數，符合本週「邊界要劃清楚」的紀律。
3. **每個函式都有 docstring 寫出「觀察 → 動作 → 代價」** — 跟著作業 rubric 的要求。
4. **test_clean.py 不依賴真實 CSV** — 用最小可行 input 測單一行為，
   final project 的 test 可以照這個結構寫。
