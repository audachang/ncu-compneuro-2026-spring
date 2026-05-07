# Week 11: Web App Development with Streamlit

> **課程**：NS5116 電腦硬體與程式語言在行為科學實驗與大數據分析之應用
> **週次 / 日期**：Week 11 of 16 · 2026-05-07
> **總時長**：150 分鐘（含 10 分鐘休息）

---

## Learning Objectives (學習目標)

完成本週後，你將能夠：

1. **解釋** Streamlit 的 *rerun-on-interaction* 執行模型，以及它與 Jupyter notebook 的差異。
2. **建立** 一個多區塊 Streamlit app，包含 title、markdown、metric、與 dataframe 顯示。
3. **加入** 互動式 widgets（`selectbox`、`slider`、`multiselect`、`checkbox`、`file_uploader`）並理解每個 widget 的回傳值。
4. **整合** Matplotlib 圖表與 Streamlit 內建的 `st.line_chart` / `st.bar_chart`。
5. **使用** `st.columns`、`st.sidebar`、`st.tabs`、`st.expander` 規劃 dashboard 版面。
6. **套用** `@st.cache_data` 避免重複載入大型資料。
7. **部署** 自己的 app 到 Streamlit Community Cloud 並取得公開 URL。

---

## Streamlit vs. Flask vs. Dash — 為什麼是 Streamlit？

| | Streamlit | Flask | Dash (Plotly) |
|---|---|---|---|
| 學習曲線 | 平 — 純 Python，不用 HTML/CSS/JS | 陡 — 要懂 routing、template、HTTP | 中 — Python 為主但要懂 React 概念 |
| 寫法 | top-to-bottom script | route decorator + template | callback graph |
| 適合 | 快速做資料分析 dashboard、demo | 通用 web app、API server | 複雜 callback 的互動圖表 |
| 部署 | Streamlit Cloud（免費） | 自架或 PaaS | 自架或 Dash Enterprise |

**結論**：對研究者、學生、資料科學家，Streamlit 是最低摩擦的選擇 — 你已經會寫 Python 與 pandas，再多學 5–10 個 `st.*` 函式就能做 web app。本週聚焦 Streamlit。

---

## Why This Matters (動機)

你已經會用 Jupyter 跑分析、用 matplotlib 畫圖。但當你想把結果分享給：

- 不會寫 Python 的合作研究者（例如臨床同事），
- 想自己「拉拉看 slider」探索資料的 PI，
- 在 Week 16 的 final project 要展示成果的觀眾，

**寄一份 `.ipynb` 不會有人打開**。Streamlit 讓你把同一份分析變成一個 *網頁*，對方只要有瀏覽器就能用。整個過程不需要 HTML、CSS、JavaScript — 全部用 Python。

本週我們會以一個 **認知老化 (cognitive aging) 資料集** 為例：n=400 名受試者、年齡 20–80、5 項認知測驗。目標是建立一個讓使用者可以「依年齡、性別、教育程度篩選，並比較不同年齡組認知表現」的 dashboard。

---

## In-Class Topics

### 1. The Streamlit Mental Model (10 min)

最重要的一個觀念：**每次使用者互動，整支 `app.py` 從頭跑到尾**。沒有 callback、沒有 event handler、沒有 `onClick`。

```python
import streamlit as st

count = st.slider("Pick a number", 0, 100, 50)
st.write(f"You picked {count}")
```

當使用者拖動 slider，Streamlit 會：

1. 重新執行 `app.py`。
2. 第二行 `st.slider(...)` 回傳當前的 slider 值（不再是 50，而是新值）。
3. 第三行 `st.write(...)` 渲染新文字。

**為什麼這個設計很方便**：你寫程式的方式和 Jupyter 一樣 — 由上到下，一行一行 — 卻得到一個互動式網頁。

**常見錯誤**：以為 slider 會「等使用者點 OK 才更新」。它會在 *每次互動* 立刻 rerun。

```bash
pip install streamlit
streamlit run app.py
```

App 會在 `http://localhost:8501` 打開，存檔後右上角會出現 *Rerun* 與 *Always rerun* 的提示。

> **⚡ 先看官方 demo**（推薦，5 分鐘）：在 terminal 執行 `streamlit hello`，會啟動四個內建範例 — animated chart + progress bar、互動式地圖、國家篩選 dataframe、即時影像辨識。對 Streamlit 的能力範圍有具體想像後，再回來寫 code。
>
> 這個入門框架的整理參考自陳 YT 的 Medium 文章 *機器學習/資料科學框架應用 — Streamlit 入門*（見文末 Resources）。

---

### 1.5 `st.write()` — Streamlit 的「萬能輸出函式」 (5 min)

Streamlit 的一個核心設計哲學：**用一個函式應付所有顯示需求**。

```python
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.write("# 這是 markdown 標題")              # markdown
st.write("這是一段純文字。")                    # plain text
st.write({"a": 1, "b": [2, 3]})                # dict → JSON view
st.write(pd.DataFrame({"x": [1, 2, 3]}))       # interactive table

fig, ax = plt.subplots()
ax.plot([1, 2, 3], [4, 5, 6])
st.write(fig)                                  # matplotlib figure
```

`st.write` 會自動偵測物件型別：DataFrame → 互動式 table、figure → 圖、dict → JSON 樹狀檢視、字串 → markdown。寫快速 prototype 時不用記 `st.dataframe` / `st.pyplot` / `st.json` — 全部丟 `st.write` 就好。

**Magic commands**（Python 3 隱式渲染）— 連 `st.write` 都省了：

```python
df = pd.DataFrame({"age": [25, 60], "rt": [320, 410]})

"# Streamlit Magic"        # 直接寫字串 → markdown
df                         # 直接寫 dataframe → 互動表格
fig                        # 直接寫 figure → 圖
```

任何「孤立的表達式」會被 Streamlit 自動視為 `st.write(...)`。**正式的 dashboard 仍建議顯式呼叫 `st.dataframe / st.pyplot`** — 比較容易讀；但 prototyping 時 magic 很省事。

---

### 2. The Cognitive Aging Dataset (10 min)

我們今天的範例資料 `cognitive_aging_taiwan.csv`（合成資料，n=400）：

| Column | Type | Description |
|--------|------|-------------|
| `subject_id` | str | S001 – S400 |
| `age` | int | 20–80 |
| `sex` | str | F / M |
| `education` | int | 受教育年數 (9–22) |
| `group` | str | young / middle / older |
| `reaction_time_ms` | float | 簡單反應時間 (lower = faster) |
| `working_memory_span` | int | n-back 記憶容量 (2–9) |
| `processing_speed` | float | digit-symbol substitution |
| `moca_score` | int | Montreal Cognitive Assessment (0–30) |
| `stroop_interference_ms` | float | incongruent − congruent RT |

資料生成邏輯（節錄）符合認知老化文獻 (Salthouse, 2010; Hartshorne & Germine, 2015) 的典型模式：

- RT 隨年齡增加而變慢（約 +2 ms/年）
- working memory 在 25 歲達高峰後逐漸下降
- processing speed 線性下降
- MoCA 在高齡才有輕微 ceiling-到-decline 變化
- Stroop interference 隨年齡增加

**試試看**：跑 `app/generate_dataset.py`，打開 CSV，用 pandas 確認 `df.groupby("group")["reaction_time_ms"].mean()` 的結果。

*📄 [`app/generate_dataset.py`](app/generate_dataset.py)*

---

### 3. Hands-on Practice 1 — Hello, Streamlit (15 min)

**任務**：建立第一個 app，顯示資料前 10 列、總受試者數、平均年齡。

```python
# app_step1.py
import streamlit as st
import pandas as pd

st.title("🧠 Cognitive Aging Dashboard")
st.write("First look at the dataset.")

df = pd.read_csv("data/cognitive_aging_taiwan.csv")

st.metric("Participants", len(df))
st.metric("Mean age", f"{df['age'].mean():.1f} years")

st.dataframe(df.head(10))
```

執行：

```bash
streamlit run app_step1.py
```

**檢查清單**：
- [ ] 看到 title「🧠 Cognitive Aging Dashboard」
- [ ] 看到兩個大數字 metric
- [ ] 看到可排序的 dataframe 表格

**常見錯誤**：把 `st.dataframe(df)` 寫成 `st.write(df.head(10))`。後者也會顯示，但不是互動式表格。

---

### 4. Widgets — 讓使用者操控資料 (15 min)

**Selectbox**（單選）：

```python
measure = st.selectbox(
    "Which cognitive measure to plot?",
    options=["reaction_time_ms", "moca_score", "working_memory_span"],
)
st.write(f"You chose: {measure}")
```

**Slider**（範圍）：

```python
age_min, age_max = st.slider(
    "Age range", min_value=20, max_value=80, value=(20, 80)
)
df_filtered = df[df["age"].between(age_min, age_max)]
st.write(f"{len(df_filtered)} participants in age {age_min}–{age_max}")
```

**Multiselect**（多選）：

```python
sex_choices = st.multiselect(
    "Sex", options=["F", "M"], default=["F", "M"]
)
df_filtered = df_filtered[df_filtered["sex"].isin(sex_choices)]
```

**Checkbox**（開關）：

```python
show_table = st.checkbox("Show raw data table", value=False)
if show_table:
    st.dataframe(df_filtered)
```

**重點**：每個 widget 都 *回傳一個值*。把它存到變數，後續用這個變數過濾資料 — 不需要 callback。

**Status messages — 視覺化的 user feedback**：

```python
st.success("Loaded 400 participants successfully.")
st.warning("12 trials had RT < 200 ms — excluded as outliers.")
st.error("File missing required column: 'reaction_time_ms'")
st.info("Tip: Slide age range below 30 to see young adult subsample.")

# 進度
with st.spinner("Running RSA computation..."):
    rsm = compute_rsm(df)
st.success("Done!")

bar = st.progress(0)
for i in range(100):
    bar.progress(i + 1)

st.balloons()       # 慶祝 — 任務完成的小彩蛋
```

`st.success / .warning / .error / .info / .exception` 不是用 `print` 寫到 console，而是渲染成色塊提示。把它們當作 dashboard 與使用者溝通的回饋管道 — 比靜默更新或丟例外好得多。

**展示 stimuli 與媒體**（對行為實驗 dashboard 有用）：

```python
st.image("stim/gabor_45deg.png", caption="Gabor patch (45°)", width=240)
st.audio("stim/tone_1khz.wav")
st.video("stim/biological_motion.mp4")
```

這三個 API 接受 file path、URL、bytes、或 numpy array — 對「在 dashboard 旁邊放當次 trial 的 stimulus 預覽」很方便。

---

### 5. Hands-on Practice 2 — 加入篩選器 (15 min)

**任務**：在 Practice 1 的基礎上，加入：
1. 一個 age slider（範圍 20–80，預設整段）
2. 一個 sex multiselect
3. 篩選後重新顯示 metric 與 dataframe

<details>
<summary>✅ 參考解答</summary>

```python
import streamlit as st
import pandas as pd

st.title("🧠 Cognitive Aging Dashboard")

df_all = pd.read_csv("data/cognitive_aging_taiwan.csv")

# Widgets
age_min, age_max = st.slider("Age range", 20, 80, (20, 80))
sex_choices      = st.multiselect("Sex", ["F", "M"], default=["F", "M"])

# Filter
df = df_all[df_all["age"].between(age_min, age_max) & df_all["sex"].isin(sex_choices)]

# Display
c1, c2 = st.columns(2)
c1.metric("Participants", len(df))
c2.metric("Mean RT", f"{df['reaction_time_ms'].mean():.0f} ms")

st.dataframe(df.head(20))
```
</details>

---

### ☕ 休息 10 min

---

### 6. Charts — Matplotlib 與 Streamlit 內建圖表 (15 min)

Streamlit 提供兩種畫圖路徑。

**Built-in charts（一行搞定）**：

```python
group_means = df.groupby("group", observed=True)["reaction_time_ms"].mean()
st.bar_chart(group_means)         # bar chart
st.line_chart(df.set_index("age")["moca_score"])  # quick line
```

**Matplotlib（更多控制）**：

```python
import matplotlib.pyplot as plt
import numpy as np

fig, ax = plt.subplots(figsize=(8, 4))
ax.scatter(df["age"], df["reaction_time_ms"],
           s=20, alpha=0.5, c="#1F6FB4")

# Linear fit
slope, intercept = np.polyfit(df["age"], df["reaction_time_ms"], 1)
xs = np.array([df["age"].min(), df["age"].max()])
ax.plot(xs, slope*xs + intercept, "k--", label=f"slope={slope:.2f} ms/yr")

ax.set_xlabel("Age (years)")
ax.set_ylabel("Reaction Time (ms)")
ax.legend()
st.pyplot(fig)        # ← 不要用 plt.show()
```

**常見錯誤**：在 Streamlit 內用 `plt.show()` — 它什麼都不會發生。一律用 `st.pyplot(fig)`。

---

### 7. Layout — Columns, Sidebar, Tabs, Expander (10 min)

**Columns**（左右排版）：

```python
left, right = st.columns([2, 1])    # 2:1 寬度比

with left:
    st.subheader("Scatter")
    st.pyplot(fig)

with right:
    st.subheader("Stats")
    st.dataframe(df.describe())
```

**Sidebar**（左側固定面板，常用於 filters）：

```python
with st.sidebar:
    st.header("Filters")
    age_range = st.slider("Age", 20, 80, (20, 80))
    measure   = st.selectbox("Measure", [...])
```

**Tabs**（多分頁）：

```python
tab1, tab2, tab3 = st.tabs(["Scatter", "Distribution", "Raw data"])
with tab1:
    st.pyplot(fig_scatter)
with tab2:
    st.pyplot(fig_hist)
with tab3:
    st.dataframe(df)
```

**Expander**（折疊區塊）：

```python
with st.expander("📖 About this dataset"):
    st.markdown("Synthetic data, n=400, ages 20–80...")
```

---

### 8. `@st.cache_data` — 別讓 CSV 每次都重讀 (10 min)

預設情況下，*每次互動都會重新執行整支 `app.py`*。如果你的 `pd.read_csv()` 要 2 秒，那每次拖 slider 都要等 2 秒。

```python
@st.cache_data
def load_data(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)
    df["group"] = pd.Categorical(df["group"],
                                 categories=["young", "middle", "older"],
                                 ordered=True)
    return df

df = load_data("data/cognitive_aging_taiwan.csv")
```

**運作方式**：Streamlit 用 *函式名稱 + 參數值* 當 cache key。同樣參數第二次呼叫不會重跑函式，直接回傳第一次的結果。

**何時要用 `@st.cache_data`**：
- 讀取檔案、API request
- 任何「同樣輸入永遠回同樣結果」且耗時 > 50 ms 的計算

**何時 *不要* 用**：
- 函式有副作用（寫檔、改變全域變數）
- 函式回傳的物件包含 thread / connection（用 `@st.cache_resource` 而非 `@st.cache_data`）

#### `@st.cache_data` vs. `@st.cache_resource` — 知道差別

| Decorator | 適用 | 範例 |
|---|---|---|
| `@st.cache_data` | 可序列化（serializable）資料：DataFrame、字串、字典、numpy array | CSV / API / 計算結果 |
| `@st.cache_resource` | 不可序列化的「資源物件」：DB connection、ML model、tokenizer | Loading sklearn model |

```python
@st.cache_resource
def load_model(path):
    """ML model 不能被 pickle 跨 session 序列化 — 用 cache_resource。"""
    import joblib
    return joblib.load(path)

model = load_model("models/cognitive_age_predictor.pkl")
```

**判斷原則**：「我每次 rerun 想要拿到 *同一個* 物件實例（而不是相同內容的新副本）嗎？」如果是 → `cache_resource`。否則 → `cache_data`。

---

### 9. Hands-on Practice 3 — 完成 Dashboard (15 min)

**任務**：以 Practice 2 為基礎，加入：

1. 把 filters 全部移到 `st.sidebar`
2. 加入一個 cognitive measure 的 selectbox
3. 主畫面用 `st.tabs(["Scatter", "Distribution", "Raw data"])` 分三頁
4. 在 scatter 頁顯示 age × measure 的散佈圖加迴歸線
5. 在 distribution 頁畫三個 group 的 histogram
6. 用 `@st.cache_data` 包住 CSV 讀取

完整參考解答在 `app/app.py` — 上課示範完成後再打開比對。

---

### 9.5 Multi-page App Pattern — 把 dashboard 變成 ML app (5 min)

對 prediction app（例如「依使用者輸入的年齡、教育、性別 → 預測認知分數」）一個 page 不夠用。最簡單的多頁結構：sidebar selectbox 控制 mode：

```python
mode = st.sidebar.selectbox(
    "Page",
    ["📊 Overview", "🔍 EDA", "🤖 Predict your score"],
)

if mode == "📊 Overview":
    show_overview(df)
elif mode == "🔍 EDA":
    show_eda(df)
else:
    show_prediction_page(df, model)
```

`show_*` 是普通 Python 函式，每個函式內部用 `st.metric / st.plotly_chart / st.dataframe` 等繪製對應 view。**重點**：sidebar 在所有 pages 共用，但主畫面內容依 mode 切換。

> Streamlit 也內建 *正式* 的 multipage 機制（在 repo 內建立 `pages/` 資料夾，每個檔案自動成為一頁）。對複雜 app 推薦 `pages/` 寫法；對 prototype 上面的 selectbox 模式最簡單，直接用單一 `app.py`。

---

### 10. Deploy to Streamlit Cloud (10 min)

部署流程一次走完：

**Step 1 — 準備檔案**：repo 必須包含

```
your-repo/
├── app.py
├── requirements.txt
└── data/
    └── cognitive_aging_taiwan.csv
```

`requirements.txt`：

```
streamlit>=1.33
pandas>=2.0
numpy>=1.26
matplotlib>=3.8
```

**Step 2 — push 到 public GitHub repo**（沿用 Week 10 學的 git 工作流程）：

```bash
git add app.py requirements.txt data/
git commit -m "Add cognitive aging Streamlit app"
git push origin main
```

**Step 3 — 連到 [share.streamlit.io](https://share.streamlit.io)**：

1. Sign in with GitHub
2. Click **New app**
3. 選 repository、branch、`app.py` 路徑
4. Click **Deploy** — 約 1–2 分鐘後就有公開 URL（例如 `https://your-name-cognitive-app.streamlit.app`）

**Step 4 — 修改後 redeploy**：直接 push commit 到 main，Streamlit Cloud 會自動偵測並重新 build。不需要在 Streamlit Cloud 介面做任何事。

**這個 URL 就是你 Week 16 final presentation 要展示的東西。**

---

## Recap & Common Pitfalls (重點回顧與常見錯誤)

| 主題 | 常見錯誤 | 正確做法 |
|------|----------|----------|
| 執行模型 | 期待 callback / event handler | 接受 *every interaction = full rerun* |
| 顯示 DataFrame | `print(df)` 或 `st.write(df.head())` | `st.dataframe(df)` |
| 顯示 matplotlib | `plt.show()` | `st.pyplot(fig)` |
| 多個 widget 共用 widget 物件 | 重用 widget 變數 | 每個 widget 用獨立變數名 |
| 載入大資料 | 每次都 `pd.read_csv` | 用 `@st.cache_data` |
| 部署 | 忘記 `requirements.txt` | 一律先用 `pip freeze` 或手寫 requirements |

---

## Homework

**目標**：以本週介紹的 cognitive aging dataset 建立你自己的 dashboard，並部署到 Streamlit Cloud。

**最低要求**：
1. 用 `@st.cache_data` 載入 `cognitive_aging_taiwan.csv`。
2. 至少 **3 個** 不同類型的 widget（slider / selectbox / multiselect / checkbox / radio 任選）。
3. 至少 **2 種** 視覺化（scatter + histogram，或 bar + line，等等）。
4. 使用 `st.sidebar` 或 `st.columns` 規劃版面。
5. 至少 **1 個** `st.metric` 並適當設定 `delta_color`。
6. 加入 `st.download_button` 讓使用者下載篩選後的資料。
7. 部署到 Streamlit Cloud 並取得公開 URL。

**繳交內容**：
- GitHub repo URL（包含 `app.py`、`requirements.txt`、`data/`）
- Streamlit Cloud 公開 URL
- 一段 100 字內的 reflection：*「使用者最可能用我這個 app 學到什麼?」*

**Rubric**：
- 功能完整性（widgets, charts, layout）：50%
- Code 品質（caching、註解、命名）：20%
- Deploy 成功且 URL 可開：20%
- Reflection：10%

---

## Resources

- [Streamlit Documentation](https://docs.streamlit.io/)
- [Streamlit Cheat Sheet](https://cheat-sheet.streamlit.app/)
- [Streamlit API Reference — Widgets](https://docs.streamlit.io/develop/api-reference/widgets)
- [Streamlit Caching Guide](https://docs.streamlit.io/develop/concepts/architecture/caching)
- [share.streamlit.io](https://share.streamlit.io) — Streamlit Community Cloud
- 陳 YT (2020). [機器學習/資料科學框架應用 — Streamlit 入門 (1)](https://medium.com/@yt.chen/機器學習-資料科學框架應用-streamlit入門-1-d07478cd4d8). Medium. — 中文入門教學，含 `streamlit hello`、`st.write` 萬能用法、與 Magic Commands 介紹。
- Mhadhbi, N. (2026). [Streamlit Tutorial: A Beginner's Guide to Building Data Apps](https://www.datacamp.com/tutorial/streamlit). DataCamp. — 包含完整 text 顯示家族、status messages、`@st.cache_resource` 與 ML prediction app 的 end-to-end 範例。
- Salthouse, T. A. (2010). *Selective review of cognitive aging.* JINS, 16(5), 754–760.
- Hartshorne, J. K., & Germine, L. T. (2015). *When does cognitive functioning peak?* Psychological Science, 26(4), 433–443.

---

## What Comes Next

| Week | Topic |
|------|-------|
| 12 | Open Data APIs — 從 PubMed / data.gov.tw 抓即時資料 |
| 13 | 互動式圖表 (Plotly Express) 與 data storytelling |
| 14 | 用 Claude API 為你的 app 加上 AI feature |
| 16 | **Final milestone**：展示部署完成的 Streamlit app |

---

*最後更新：2026-05-06*
