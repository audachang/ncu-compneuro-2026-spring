# Week 12: Streamlit Caching & The Data Analysis Pipeline

> **Course:** NS5116 Programming & AI Applications in Behavioral Science — Spring 2026
> **Week:** 12 of 16 | **Date:** 2026-05-14 | **Room:** TBA

---

## 本週主軸 (Why This Matters)

上週我們示範了一系列 Streamlit 元件 (`demo01`–`demo14`)，並交付了一個整合的 dashboard — `week-11-web_app_development_with_streamlit/app/app.py`。但因為時間關係，我們 **沒有逐段拆解這支整合範例**。

本週的安排是：

1. **前半 (60 min)** — 回到 `app.py`，把 Streamlit demos 串起來的「工程細節」講清楚，特別是 **`@st.cache_data` 的快取機制**。這是讓 dashboard 在多人連線、反覆 rerun 下仍然順暢的核心 API。
2. **後半 (90 min)** — 拉開視角，談 data science 中一般化的 **「資料分析流程 (data analysis pipeline)」**：raw data → descriptive statistics → 根據觀察修補資料 → 可分析的乾淨資料。我們先建立通用心智模型，再用一個認知神經科學的小例子 (Stroop-like RT dataset) 走一遍流程。Open data API 的具體實作會延後到後續週次再處理。

學期脈絡：Week 11 學會「畫出 dashboard」、Week 12 學會「**讓 dashboard 背後的資料是可信的**」、Week 13 (Plotly) 再讓圖更互動、Week 14 (Anthropic SDK) 讓 dashboard 具備 AI 解讀能力。

---

## Learning Objectives (學習目標)

修完本週後，你應該能夠：

1. **解讀 `app.py`** — 說明 `st.set_page_config`、`st.sidebar`、`st.tabs`、`st.columns`、`st.metric` 等元件在整合範例中扮演的角色，並理解 Streamlit 的「rerun on every interaction」執行模型 (execution model)。
2. **正確使用 `@st.cache_data`** — 區分 `@st.cache_data` 與 `@st.cache_resource` 的適用場景，掌握 `ttl`、`max_entries`、`show_spinner` 參數，並能診斷 "UnhashableParamError" 等典型錯誤。
3. **描繪一個通用的資料分析流程 (data analysis pipeline)** — load → inspect → describe → diagnose → fix → re-describe → analyse，並說明每一步要回答什麼問題。
4. **用 descriptive statistics 診斷資料品質** — 透過 `df.info()`、`df.describe()`、`value_counts()`、`isnull().sum()`、分佈圖等手段，**從統計摘要中讀出問題**（缺值、型別錯誤、outlier、編碼錯亂、不平衡 class）。
5. **以觀察驅動的方式修補資料 (observation-driven fixing)** — 根據 descriptive statistics 的線索，選擇 `to_numeric` / `to_datetime` / `dropna` / `fillna` / value filtering / recoding 中合適的操作，並能說明每個決定背後的理由與代價。
6. **區分 data cleaning 與 data analysis 的邊界** — 知道哪些是「讓資料可分析」的前處理 (preprocessing)，哪些已經是「回答研究問題」的分析步驟，避免把實質結論與清理副作用混淆。
7. **把資料流程拆成 pure functions** — 設計可測試、可重用的 `clean()` 與 `describe()` 函式，為 Week 13–16 的 final project 鋪路。

---

## Schedule at a Glance

| 段落 | 主題 | 時間 |
|------|------|------|
| Part 1.1 | `app.py` 整體結構導覽 | 15 min |
| Part 1.2 | Streamlit 執行模型：為什麼 rerun 是關鍵 | 10 min |
| Part 1.3 | **`@st.cache_data` 深入解析** | 25 min |
| Part 1.4 | `@st.cache_resource` 與兩種快取的比較 | 10 min |
| **Break** | | 10 min |
| Part 2.1 | 資料分析流程總覽 (pipeline mental model) | 15 min |
| Part 2.2 | Descriptive statistics 作為「資料的健康檢查」 | 25 min |
| Part 2.3 | Observation-driven fixing — 從統計摘要決定怎麼修 | 30 min |
| Part 2.4 | 完整走一遍 — Stroop-like RT dataset 示範 | 15 min |
| Part 2.5 | Cleaning vs. analysis 的邊界與 pure-function 化 | 5 min |
| Recap | 重點回顧 & Homework brief | 10 min |

總計：約 170 分鐘 (含 10 min break)。

---

## Course Contents Outline (課程內容優化版)

本週內容可以用一條主線理解：

> **從「可以互動的 dashboard」走向「資料是可信的 data app」。**

因此課程不只是介紹 Streamlit 或 pandas 語法，而是把 Week 11 的 Streamlit app 重新拆開，說明一個資料產品從「看得到圖」走向「結論站得住腳」時，需要補上的三個能力：

1. **Execution awareness** — 知道 Streamlit 每次互動都會 rerun，因此能判斷哪些步驟會變成效能瓶頸。
2. **Caching strategy** — 用 `@st.cache_data`、`@st.cache_resource` 分別處理資料與資源，避免不必要的重複計算。
3. **Data analysis mindset** — 把任何拿到手的資料先當成「未驗證的」，用 descriptive statistics 做健康檢查，再根據觀察結果決定怎麼修。

### A. Conceptual Roadmap

| 階段 | 核心問題 | 學生要帶走的觀念 |
|------|----------|------------------|
| 1. Streamlit app anatomy | 一個 dashboard 由哪些固定區塊組成？ | app 通常由 page config、data loading、widgets、filtering、layout 與 charts 組成。 |
| 2. Rerun model | 為什麼每次拖 slider 都會重新執行整支程式？ | Streamlit 用「重新執行腳本」換取簡單的 UI state model。 |
| 3. Data caching | 哪些程式碼應該被 cache？cache key 怎麼決定？ | expensive but deterministic 的資料函式適合 `@st.cache_data`。 |
| 4. Data analysis pipeline | 從 raw data 到可發表結果，要經過哪些固定步驟？ | load → inspect → describe → diagnose → fix → re-describe → analyse，是所有資料專案的共通骨架。 |
| 5. Descriptive statistics as diagnosis | 統計摘要除了「描述」之外還能做什麼？ | descriptive statistics 是資料品質的健檢工具 — 從 mean、SD、min/max、缺值率、value_counts 可以讀出 dataset 的問題。 |
| 6. Observation-driven fixing | 看到不對勁的數字後怎麼決定動作？ | 任何 cleaning 操作 (drop / fill / coerce / filter / recode) 都應該對應到一個 descriptive statistics 觀察到的具體現象，並理解每個動作的代價。 |
| 7. Cleaning vs. analysis | 哪些操作算「整理資料」，哪些已經算「回答研究問題」？ | 兩者必須分開：清理屬於可重複的前處理，分析則對應 hypothesis。混在一起會讓結論依賴於沒被檢視的清理決定。 |

### B. Detailed Teaching Flow

#### Module 1 — Reconstruct the Week 11 App

**Goal**：讓學生看懂完整 `app.py`，不只會改 UI 元件。

本段建議先從「使用者看到的畫面」回推程式結構：sidebar 決定篩選條件，header 呈現整體摘要，tabs 承載不同分析視角，metrics 與 charts 則是最終輸出。接著再把程式分成七個區塊，提醒學生 data loading 在 dashboard app 中通常是最容易被忽略、但最影響體驗的部分。

**Key questions**：

- 哪些程式碼只應該在 app 啟動時做一次？
- 哪些程式碼必須隨著 widget 互動重新計算？
- 如果資料來源從 400-row CSV 換成 API 或大型檔案，哪裡會先變慢？

**Mini-output**：學生能用自己的話畫出 `app.py` 的資料流：`load_data()` → sidebar filters → filtered DataFrame → KPI / tabs / plots。

#### Module 2 — Understand Streamlit Rerun and Caching

**Goal**：讓學生理解 cache 不是「加速魔法」，而是對 rerun model 的工程回應。

先用 `print("DEBUG: reading CSV")` 製造可觀察現象：有 cache 時，拖 slider 不會重讀 CSV；拿掉 cache 後，每次互動都會重讀。接著再進入 `@st.cache_data` 的 key、copy semantics、TTL、max entries 與常見錯誤。

**Key questions**：

- cache key 如果沒有包含某個輸入，會產生什麼錯誤結果？
- 為什麼 `@st.cache_data` 回傳 copy 比回傳同一個 object 更安全？
- 什麼情況下 `@st.cache_resource` 比 `@st.cache_data` 合理？

**Mini-output**：學生能判斷一個函式該不該 cache，以及應該用 `cache_data` 還是 `cache_resource`。

#### Module 3 — The Data Analysis Pipeline as a Mental Model

**Goal**：讓學生看到所有資料專案——不論是 behavioral experiment、開放資料、或 fMRI BOLD signal——背後都有同一條骨架。

本段不寫太多程式碼，而是用一張流程圖把 pipeline 講清楚：load → inspect → describe → diagnose → fix → re-describe → analyse。重點是讓學生意識到「拿到資料就直接畫 bar chart」會跳過 diagnose 與 fix，導致結論不可靠。

**Key questions**：

- 「raw data」與「analysable data」之間到底差了什麼？
- 為什麼 inspect 與 describe 必須在 fix 之前？
- 為什麼 fix 之後還要 re-describe 一次？

**Mini-output**：學生能用自己的話畫出這條 pipeline，並指出 Week 11 的 `app.py` 只覆蓋了 load 與 analyse / display 兩端。

#### Module 4 — Descriptive Statistics as a Diagnostic Tool

**Goal**：把 descriptive statistics 從「論文 Table 1」重新定位成「資料健康檢查的儀器」。

示範 `df.info()`、`df.describe()`、`df.isnull().sum()`、`df["col"].value_counts(dropna=False)`、簡單的 histogram / boxplot。重點不是這些 API 怎麼用 (學生大致都會)，而是 **「看到什麼數字代表什麼問題」**：

- `count` 比其他欄位少 → 缺值
- `min`/`max` 物理上不可能 → 編碼錯誤或 outlier
- `dtype` 是 object 但內容看起來是數字 → 型別錯誤
- `value_counts` 出現 `"NA"`, `"-"`, `""`, `999` → 缺值的偽裝
- mean 與 median 差很多 → 分佈偏斜或有極端值

**Key questions**：

- 哪些 summary statistics 對 numerical 欄位最有資訊量？對 categorical 呢？
- `df.describe()` 預設不包含 categorical，要怎麼補上？
- 為什麼用 `dropna=False` 看 `value_counts` 才不會錯過缺值樣態？

**Mini-output**：學生拿到一筆陌生 DataFrame 時，能在三分鐘內列出至少三個值得追問的疑點。

#### Module 5 — Observation-Driven Fixing

**Goal**：建立「每個 cleaning 動作都對應一個觀察」的紀律，避免無腦套用 `dropna()`。

本段把 Module 4 觀察到的每一種問題，配對到一個合適的 fix：

| Module 4 觀察到的現象 | 對應的 fix | 代價 / 風險 |
|----------|-----------|------------|
| 數值欄位 dtype 是 object | `pd.to_numeric(..., errors="coerce")` | 無法解析的值變 NaN，可能掩蓋編碼問題 |
| 缺值在少數 row | `dropna(subset=[...])` | 損失 n，可能造成 selection bias |
| 缺值在許多 row 但 systematic | `fillna(策略)` 或保留並 model 缺值 | 填補方法本身就是一個假設 |
| min/max 物理上不可能 | value filtering (`df[df.col.between(...)]`) | 選錯範圍會剔除真實的極端值 |
| 缺值的偽裝（`"NA"`, `-999`） | 先 `replace` 再 `to_numeric` | 漏掉某個 sentinel 就會污染後續分析 |
| Categorical 編碼不一致 (`"M"`, `"male"`, `"Male"`) | recode（`str.lower()`、`map()`） | 合併不該合的 level 也是錯 |

**Key questions**：

- 為什麼「先 drop 再做任何事」是危險的預設？
- 任何 cleaning 動作之後應該做什麼，才能驗證自己沒做錯？
- 哪些 cleaning 決定應該寫在 docstring / report 裡讓 reviewer 看見？

**Mini-output**：學生能對一個 messy DataFrame 寫出 cleaning function，且每一行都能說出「我看到什麼觀察、所以做這個動作、代價是什麼」。

#### Module 6 — Boundary Between Cleaning and Analysis

**Goal**：讓學生意識到「清理」與「分析」很容易彼此污染，需要刻意劃線。

舉例：在 Stroop dataset 中，「剔除 RT > mean + 3 SD 的 outlier」乍看是 cleaning，但它直接影響 congruent vs. incongruent 的差異估計。如果這個門檻設在不同地方就會得到不同結論，那它其實已經是 analysis decision。

示範一個簡單的分層：

```text
data_pipeline.py
├── load_raw(path)        # I/O only, no transformation
├── clean(df)             # pure function, 只做不可爭議的修補
├── describe(df)          # 產生 summary table / quick plots
└── analyse(df, params)   # 任何「會影響結論」的決定都在這層
```

`clean()` 與 `describe()` 寫成 pure function 後，可以單獨被 pytest 測試；`analyse()` 則應該明確接受 parameter (例如 outlier 門檻)，並把這個決定寫進 report。

**Key questions**：

- 哪些操作即使換不同的研究者來做，結果都應該一樣？(→ 屬於 clean)
- 哪些操作不同研究者可能做不同決定？(→ 屬於 analyse，要被討論)
- 為什麼把這條線畫清楚，對 reproducibility 與 pre-registration 很重要？

**Mini-output**：學生能把本週 Stroop demo 的 notebook 拆成 `clean()` / `describe()` / `analyse()` 三個函式。

### C. End-of-Class Deliverable

本週結束前，學生應該完成或至少開始一個小型練習：

1. 拿到本週 demo 用的 messy Stroop-like CSV（教師會提供）。
2. 用 descriptive statistics 列出至少三個資料品質問題。
3. 寫一個 `clean(df)` 函式逐一處理，並在 docstring 註明「觀察 → 動作 → 代價」。
4. 在 cleaning 前後各跑一次 `describe()`，比較 mean RT、accuracy、n。
5. 用乾淨資料做最後一步 analysis（congruent vs. incongruent 的 paired t-test 或 effect size）。

這個 deliverable 不要求接上 Streamlit，但必須證明學生能把 pipeline 的每一段獨立拆開、並且能解釋每個 cleaning 決定。

---

# Part 1 — `app.py` 拆解與 Streamlit 快取機制

## 1.1 `app.py` 整體結構導覽 (15 min)

打開 `week-11-web_app_development_with_streamlit/app/app.py`。這支檔案是 Week 11 的整合產出，模擬一個 **Cognitive Aging Dashboard** — 給定 n=400 的合成 lifespan 認知測驗資料 (RT、working memory span、processing speed、MoCA、Stroop interference)，讓使用者透過 sidebar 篩選年齡、性別、教育年數，並在四個 tab 中查看不同視角的結果。

整支程式的結構可以分成 **七個區塊**，剛好對應一個典型 Streamlit app 的骨架：

```
┌─────────────────────────────────────────────────┐
│ 1. Page config       — st.set_page_config()     │  ← 必須最先呼叫
│ 2. Constants         — DATA_PATH, MEASURES       │
│ 3. Data loading      — @st.cache_data + load_data│  ← 今天重點
│ 4. Sidebar widgets   — st.slider, multiselect... │  ← 使用者輸入
│ 5. Filtering logic   — boolean mask on DataFrame │
│ 6. Header + KPI      — st.title, st.metric       │
│ 7. Tabs              — st.tabs(...) × 4          │  ← 主視覺區
└─────────────────────────────────────────────────┘
```

**注意**：`st.set_page_config()` **必須是第一個 Streamlit 呼叫**，否則會 raise `StreamlitAPIException`。常見錯誤是寫到 `import` 之後才放 `st.title("...")`，再來才設定 page config。

### 🔬 Hands-on Practice 1: 把 app 跑起來、改一個小參數

**任務**：

1. 從 terminal 切到 `week-11-web_app_development_with_streamlit/app/`，執行
   ```bash
   streamlit run app.py
   ```
2. 把 `MEASURES` 字典中 `"reaction_time_ms"` 對應的 label 從 `"Reaction Time (ms)"` 改成 `"Simple RT (ms)"`，**儲存檔案**。
3. 觀察瀏覽器右上角是否出現「Source file changed. Rerun.」的提示，按下 Rerun 觀察畫面更新。

**思考**：為什麼整支程式從上到下都會被重新執行？這個行為對 `load_data()` 的開銷意味著什麼？(伏筆 — 1.3 節的快取討論。)

---

## 1.2 Streamlit 執行模型：rerun 是預設行為 (10 min)

Streamlit 的核心邏輯非常單純，但容易誤解：

> **每當使用者操作任何 widget (例如拖動 slider)，Streamlit 都會從頭到尾重新執行整支 `app.py`。**

這個模型有兩個重大後果：

| 後果 | 說明 |
|------|------|
| ✅ **State management 變簡單** | 你不需要手動處理「更新狀態 → 重繪 UI」的邏輯。Widget 的值會自動傳到下一次 rerun 的程式中。 |
| ⚠️ **昂貴的計算會被反覆執行** | `load_data()` 每次 rerun 都會重讀一次 CSV！如果換成 API 呼叫或 fMRI volume 載入，幾秒鐘的延遲會讓 app 完全不能用。 |

這就是為什麼 `app.py` 的 `load_data()` 上方必須掛 `@st.cache_data` — 它告訴 Streamlit：

> 「這個函式的結果用 input 參數做 key 快取起來。下次以相同 input 呼叫時，**不要重新執行**，直接回傳上次的結果。」

**類比 (analogy)**：把 `@st.cache_data` 想成 Python 內建的 `functools.lru_cache`，但專為 Streamlit 的 rerun 行為設計，並且**會自動處理 DataFrame、NumPy array 等 unhashable 物件**。

---

## 1.3 `@st.cache_data` 深入解析 (25 min) ⭐

這是本週前半的核心。看 `app.py` 第 42–50 行：

```python
@st.cache_data
def load_data(path: Path) -> pd.DataFrame:
    """Load the cognitive aging CSV. Cached to avoid re-reading on every rerun."""
    df = pd.read_csv(path)
    df["group"] = pd.Categorical(
        df["group"], categories=["young", "middle", "older"], ordered=True
    )
    return df
```

### 1.3.1 快取的判定 key 是什麼？

`@st.cache_data` 用以下三項組成 cache key：

1. **函式名稱**（`load_data`）
2. **參數的 hash**（這裡是 `Path` 物件的字串）
3. **函式原始碼的 hash**（你修改函式內容後，舊 cache 自動失效）

所以同一個 `path` 第二次傳進來時，整個函式被「跳過」，直接回傳第一次的 DataFrame copy。

### 1.3.2 為什麼回傳的是 **copy** 而不是 reference？

`@st.cache_data` 在底層會把回傳值 **serialize 後存起來**，每次取出時 **deserialize**，等同於回傳一個 deep copy。這帶來重要保證：

> **使用者下游怎麼亂改 DataFrame 都不會污染 cache。**

```python
df = load_data(DATA_PATH)
df["age"] = -999   # 你愛怎麼改怎麼改
df2 = load_data(DATA_PATH)
print(df2["age"].head())  # 仍然是原始值
```

代價是：序列化開銷。對 100MB 以上的物件來說，序列化本身就會變慢，這時要改用 `@st.cache_resource`（見 1.4）。

### 1.3.3 重要參數

```python
@st.cache_data(
    ttl=3600,            # time-to-live，秒。1 小時後自動過期。
    max_entries=10,      # 最多保留 10 組 input 的結果，超過則 LRU 淘汰。
    show_spinner="Loading cognitive battery...",  # 第一次計算時的提示訊息。
    persist="disk",      # 把 cache 寫到磁碟，重新啟動 app 也保留。
)
def load_data(path):
    ...
```

| 參數 | 何時用 |
|------|-------|
| `ttl` | **API 資料**：你希望每小時重新抓一次最新 PM2.5 (Part 2 用到)。 |
| `max_entries` | 函式可能被以很多種 input 呼叫，避免 cache 無限長大。 |
| `show_spinner` | 第一次計算耗時 > 1 秒的場景，給使用者回饋。 |
| `persist="disk"` | 你不希望使用者每次 reload 都等同樣的 CSV 重讀。 |

### 1.3.4 常見錯誤 (Common Pitfalls)

**錯誤 1：在 cached function 內呼叫 Streamlit widget**

```python
@st.cache_data
def bad_load():
    n = st.slider("rows", 10, 100)   # ❌ 不要在 cache 內讀 widget
    return df.sample(n)
```
為什麼錯：cache key 不包含 widget 的當前值，slider 改動後仍會回傳舊結果。
**修正**：在外面讀 widget，把值當參數傳進去。

```python
n = st.slider("rows", 10, 100)
df = good_load(n)
```

**錯誤 2：unhashable 參數**

```python
@st.cache_data
def bad_filter(df, params: dict):   # dict 在某些情境下不可 hash
    ...
```
如果遇到 `UnhashableParamError`，在參數前面加底線 `_`：

```python
@st.cache_data
def good_filter(df, _params: dict):   # 底線開頭的參數不參與 hash
    ...
```
**注意**：底線參數不參與 key — 你必須自己保證它不影響輸出，否則會回錯結果。

**錯誤 3：忘了 cache 函式內部的 side effects 也會被「跳過」**

```python
@st.cache_data
def fetch_with_log(url):
    print(f"Fetching {url}")   # 第二次呼叫不會印！
    return requests.get(url).json()
```
不要把 logging、寫檔等 side effect 放在 cached function 裡。

### 🔬 Hands-on Practice 2: 觀察 cache 行為

**任務**：在 `app.py` 的 `load_data()` 內部加一行 `print("DEBUG: reading CSV")`，然後：

1. 啟動 app，觀察 terminal 印幾次。
2. 拖動 sidebar 的 age slider 三次，terminal 又印幾次？
3. **拿掉 `@st.cache_data` 裝飾器**，重複步驟 2，觀察差異。
4. 把裝飾器加回來，但改成 `@st.cache_data(ttl=10)`，等 10 秒後再操作 slider，會發生什麼？

<details>
<summary>✅ 預期觀察</summary>

- 有 cache：第一次啟動印一次，之後 slider 操作不再印。
- 沒有 cache：每次 slider 操作都印 — CSV 被反覆讀取。
- `ttl=10`：每 10 秒過後第一次互動會觸發重讀，印一次。
</details>

---

## 1.4 `@st.cache_resource` — 另一種快取 (10 min)

Streamlit 提供兩個快取裝飾器，差別如下：

| | `@st.cache_data` | `@st.cache_resource` |
|---|----------------|---------------------|
| 回傳值處理 | Serialize → deep copy | **回傳同一個 reference** (singleton) |
| 適用場景 | DataFrame、numpy array、JSON、API response | DB connection、ML model、tokenizer、LLM client |
| 跨 user session | 各自快取 | **共享同一個物件** |
| 副作用風險 | 低 (每人都拿到 copy) | 高 — 多人改同一個物件會互相影響 |

範例 — Week 14 的 Claude API client：

```python
@st.cache_resource
def get_anthropic_client():
    from anthropic import Anthropic
    return Anthropic(api_key=st.secrets["ANTHROPIC_API_KEY"])
```

如果這裡用 `@st.cache_data`，client 物件會被序列化（很可能失敗），就算成功也會在每個 session 重建。`@st.cache_resource` 確保整個 app 只有一個 client 實例。

**Decision rule**：

> **要的是「資料」？用 `cache_data`。要的是「資源/連線/物件」？用 `cache_resource`。**

---

# 🔄 BREAK — 10 min

---

# Part 2 — The Data Analysis Pipeline (一般化概念介紹)

> **注意**：本週 Part 2 刻意**不**討論如何從 open data API 抓資料 (那是後續週次的主題)。我們先建立通用的資料分析心智模型，並用一個 in-memory 的合成 dataset 把流程走過一遍。學會這條 pipeline 後，未來不論資料來源是 CSV、API、PsychoPy log、SQL query 還是 fMRI volume，都套同一個框架。

## 2.1 資料分析流程總覽 (15 min)

### 一張圖看完整個 pipeline

```
                        ┌─────────────────────────────┐
   raw data  ─────►     │  1. load                    │
   (CSV / API / log)    │     I/O only, no transform  │
                        └─────────────┬───────────────┘
                                      │
                                      ▼
                        ┌─────────────────────────────┐
                        │  2. inspect                 │
                        │     shape, dtypes, head     │
                        └─────────────┬───────────────┘
                                      │
                                      ▼
                        ┌─────────────────────────────┐
                        │  3. describe (diagnose)     │
                        │     descriptive statistics  │  ◄── 本週重點
                        │     作為「健康檢查」          │
                        └─────────────┬───────────────┘
                                      │
                          (發現問題)    │
                                      ▼
                        ┌─────────────────────────────┐
                        │  4. fix                     │
                        │     observation-driven      │  ◄── 本週重點
                        │     coerce / drop / fill /  │
                        │     filter / recode         │
                        └─────────────┬───────────────┘
                                      │
                                      ▼
                        ┌─────────────────────────────┐
                        │  5. re-describe             │
                        │     驗證 fix 沒有引入新問題    │
                        └─────────────┬───────────────┘
                                      │
                                      ▼
                        ┌─────────────────────────────┐
                        │  6. analyse / visualise     │
                        │     回答研究問題              │
                        └─────────────────────────────┘
```

### 為什麼這條 pipeline 在每個資料專案都長一樣？

不論你是分析 PsychoPy 輸出的反應時間 (RT)、處理 EPA 空品資料、或對 fMRI BOLD signal 做 ROI analysis，**raw data 與 analysable data 之間永遠隔著「描述—診斷—修補」三步**。略過這三步直接畫圖，等於把資料的雜訊與你的研究結論綁在一起。

### 兩個常見誤區

| 誤區 | 為什麼有問題 |
|------|------|
| 「資料看起來沒問題，跳過 describe 直接畫圖。」 | 你看到的是「眼睛能掃到的前幾行」，不是整個分佈。第 32 row 有一個 RT = 99999 你不會注意到。 |
| 「先 `df.dropna()` 再說。」 | 沒看清楚缺值的樣態 (隨機？系統性？只發生在某一個 condition？) 就 drop，可能引入 selection bias。 |

### 🔬 Hands-on Practice 3: 替 Week 11 `app.py` 標出 pipeline 位置

**任務**：打開 `week-11.../app/app.py`，回答：

1. 哪一行對應 pipeline 中的 `load`？
2. 哪一段對應 `analyse / visualise`？
3. `app.py` **沒有顯式包含** pipeline 中的哪幾步？對學生使用合成乾淨資料的情境合理嗎？對真實資料呢？

<details>
<summary>✅ 預期答案</summary>

- `load`：`load_data(DATA_PATH)` (第 56 行)
- `analyse / visualise`：tabs 內的 scatter、histogram、group means、bar chart
- 缺少：inspect / describe / fix / re-describe。對於 `generate_dataset.py` 生成的乾淨合成資料可以接受；但若資料來自 PsychoPy log 或真實調查就會出大問題。
</details>

---

## 2.2 Descriptive Statistics 作為「資料的健康檢查」 (25 min)

Descriptive statistics 大家都會跑——但本節要刻意把它從「論文 Table 1」的角色，重新定位成 **「資料品質的診斷儀器」**。

### 2.2.1 五件你應該每次都做的事

```python
print(df.shape)                              # 多少 row × col？
print(df.dtypes)                             # 每欄是什麼型別？
print(df.isnull().sum())                     # 哪些欄有缺值，多少筆？
print(df.describe(include="all"))            # numeric + categorical 一次看
for col in df.select_dtypes("object"):
    print(df[col].value_counts(dropna=False).head(10))
```

**關鍵**：每個指令不只是看數字，而是 **看完之後問「這合不合理？」**

### 2.2.2 從 summary statistics 中讀出問題 — 速查表

| 觀察到的現象 | 可能的問題 |
|----------|------|
| 某欄 `count` 比其他欄小很多 | 該欄有大量缺值 |
| dtype 是 `object`，但內容看起來是數字 | 字串型數值 — 通常因為混入 `"NA"`、`"-"`、空字串 |
| `min` 或 `max` 物理上不可能 (RT = -50 或 99999；age = 250) | sentinel value 偽裝成缺值，或編碼錯誤 |
| `mean` 與 `median` 差很多 | 分佈偏斜或有極端 outlier |
| `std` 異常大 / 接近 0 | 有 outlier 或欄位幾乎是常數 |
| `value_counts` 出現 `"NA"`, `"-"`, `""`, `"unknown"`, `999` | 缺值被人類用 sentinel 編碼 |
| Categorical level 看起來重複 (`"M"`, `"male"`, `"Male"`) | 大小寫不一致 / 編碼不統一 |
| 某 condition 的 trial 數遠少於其他 | 不平衡 (unbalanced design) 或 logging 失敗 |

### 2.2.3 視覺化也是 descriptive statistics 的一部分

數字摘要常常會「平均掉」結構性問題。下面這三張圖每個 dataset 都該畫一次：

```python
import matplotlib.pyplot as plt

df.hist(figsize=(10, 6))                    # 每個 numeric 欄位的分佈
df.plot.box(figsize=(8, 4))                 # outlier 一目了然
df.isnull().sum().plot.bar()                # 缺值在哪幾欄？
plt.show()
```

如果 histogram 出現雙峰、或 boxplot 一堆極端點、或缺值集中在某一欄，**這些都是 cleaning 決定的入口**。

### 🔬 Hands-on Practice 4: 從 summary 讀出三個問題

**情境**：你拿到一個 Stroop 實驗資料 (n=200 trials)，欄位是 `subject_id`、`condition`、`rt_ms`、`accuracy`、`age`。

```python
import pandas as pd
import numpy as np
np.random.seed(42)

# 故意製造一個 messy dataset
n = 200
df = pd.DataFrame({
    "subject_id": np.random.choice([1, 2, 3, 4, 5], n),
    "condition":  np.random.choice(["congruent", "Congruent", "incongruent", "INCONG"], n),
    "rt_ms":      np.random.normal(500, 80, n).astype(object),
    "accuracy":   np.random.choice([0, 1, 1, 1, 1], n),
    "age":        np.random.choice([25, 30, 35, -999, np.nan], n),
})
# 注入缺值與 sentinel
df.loc[np.random.choice(n, 12, replace=False), "rt_ms"] = "NA"
df.loc[np.random.choice(n, 5,  replace=False), "rt_ms"] = 99999
```

**任務**：只用 `info()`、`describe(include="all")`、`isnull().sum()`、`value_counts(dropna=False)` 這四個工具，列出至少三個資料品質問題。

<details>
<summary>✅ 預期觀察</summary>

1. `rt_ms` 的 dtype 是 `object`（不是 float）→ 內含字串 `"NA"`。
2. `rt_ms.describe()` 之前要先轉 numeric，否則摘要不會反映分佈；轉完後會看到 max = 99999 → sentinel outlier。
3. `condition.value_counts()` 出現 4 個 level，但其實只有 2 個（大小寫不一致）。
4. `age` 出現 -999 → sentinel；也有真的 NaN。
</details>

---

## 2.3 Observation-Driven Fixing — 從統計摘要決定怎麼修 (30 min)

**核心原則**：

> **每一個 cleaning 動作都應該對應到 Part 2.2 觀察到的一個具體現象，並且你能說出這個動作的代價。**

### 2.3.1 從觀察到動作的對應表

| 2.2 觀察到的現象 | 對應動作 | 程式碼 | 代價 / 風險 |
|----------|------|------|------|
| 數值欄是字串 (`object`) | coerce 成 numeric | `df["rt_ms"] = pd.to_numeric(df["rt_ms"], errors="coerce")` | 無法解析的值悄悄變 NaN |
| Sentinel 值偽裝缺值 (`-999`, `"NA"`) | 先 replace 再 coerce | `df["age"] = df["age"].replace({-999: np.nan})` | 漏掉某個 sentinel 就會污染後續分析 |
| 缺值少且隨機 | drop | `df = df.dropna(subset=["rt_ms"])` | 損失 n |
| 缺值多 / 系統性 | fill 或保留 + model | `df["age"] = df["age"].fillna(df["age"].median())` | 填補本身是一個假設 |
| 物理上不可能的值 | filter | `df = df[df["rt_ms"].between(150, 3000)]` | 範圍選錯會剔除真實 outlier |
| Categorical 不一致 | recode | `df["condition"] = df["condition"].str.lower().replace({"incong": "incongruent"})` | 把不該合的 level 合在一起 |
| Time 不是 datetime | parse | `df["time"] = pd.to_datetime(df["time"], errors="coerce")` | format 不對整欄變 NaT |

### 2.3.2 三條 cleaning 紀律

1. **每一步都要留下 print / log，記錄「修了多少 row」**。
   ```python
   before = len(df)
   df = df.dropna(subset=["rt_ms"])
   print(f"dropna(rt_ms): {before} → {len(df)}  (-{before - len(df)})")
   ```

2. **改完之後，再跑一次 `describe()` 驗證**。沒驗證的 cleaning 等於沒做。

3. **不要把 cleaning 寫成一長串 chain method**。每個動作獨立一行，error 才追得到。
   ```python
   # ❌ 不易 debug
   df = (df.replace(-999, np.nan)
            .dropna()
            .query("rt_ms.between(150, 3000)")
            .reset_index(drop=True))

   # ✅ 可逐步檢查
   df = df.replace(-999, np.nan)
   print(df.isnull().sum())
   df = df.dropna(subset=["age"])
   df = df[df["rt_ms"].between(150, 3000)]
   ```

### 2.3.3 觀察 → 動作的兩種錯誤模式

**錯誤 A：無腦 `dropna()`** — 看到缺值就 drop，沒看缺值樣態。

```python
df = df.dropna()    # ⚠️ 等於說「我不在乎缺值帶來什麼 bias」
```
如果 `age` 缺值集中在 older 受試者 (因為年長者更可能未填寫)，這一行會系統性低估 cognitive aging 效應。

**錯誤 B：把 analysis 決定偽裝成 cleaning**

```python
# 看起來是 cleaning ⋯⋯
df = df[df["rt_ms"] < df["rt_ms"].mean() + 3 * df["rt_ms"].std()]
```
這條 outlier rule 直接影響 condition mean 的估計，**它已經是 analysis 決定**，應該放在 `analyse()` 而非 `clean()`，並在 report 中明確聲明閾值。

### 🔬 Hands-on Practice 5: 把觀察轉成 cleaning 函式

**任務**：根據 Practice 4 觀察到的問題，寫一個 `clean_stroop(df)` 函式，並 **在每一步的註解中寫出「觀察 → 動作 → 代價」**。

<details>
<summary>✅ 參考解答骨架</summary>

```python
def clean_stroop(df: pd.DataFrame) -> pd.DataFrame:
    """Clean Stroop trial data.

    Steps (observation → action → cost):
    1) rt_ms 是 object dtype → coerce to numeric → "NA" 字串會變 NaN
    2) rt_ms 出現 99999 sentinel → 在 to_numeric 後用 range filter → 假設合理 RT < 3000ms
    3) age = -999 是 sentinel → replace 成 NaN → 後續 age-based 分析會少 n
    4) condition 有大小寫不一致 → str.lower + recode → "incong" 合併入 "incongruent"
    """
    df = df.copy()

    # 1) rt_ms type fix
    df["rt_ms"] = pd.to_numeric(df["rt_ms"], errors="coerce")

    # 2) rt_ms physically implausible
    df = df[df["rt_ms"].between(150, 3000)]

    # 3) age sentinel
    df["age"] = df["age"].replace({-999: np.nan})

    # 4) condition recode
    df["condition"] = (
        df["condition"].str.lower()
                       .replace({"incong": "incongruent"})
    )

    return df
```
</details>

**檢查**：cleaning 前後各跑一次 `describe(include="all")`，比對 n、mean RT、condition level 數。

---

## 2.4 完整走一遍 — Stroop-like RT 流程 (15 min)

把 Part 2.1–2.3 串成一個從頭到尾的 mini-pipeline：

```python
import numpy as np
import pandas as pd

# ----------- 1. load -----------
np.random.seed(42)
n = 200
raw = pd.DataFrame({
    "subject_id": np.random.choice([1, 2, 3, 4, 5], n),
    "condition":  np.random.choice(["congruent", "Congruent",
                                    "incongruent", "INCONG"], n),
    "rt_ms":      np.random.normal(500, 80, n).astype(object),
    "accuracy":   np.random.choice([0, 1, 1, 1, 1], n),
    "age":        np.random.choice([25, 30, 35, -999, np.nan], n),
})
raw.loc[np.random.choice(n, 12, replace=False), "rt_ms"] = "NA"
raw.loc[np.random.choice(n, 5,  replace=False), "rt_ms"] = 99999

# ----------- 2. inspect -----------
print(raw.shape, raw.dtypes, sep="\n")
print(raw.head(3))

# ----------- 3. describe (diagnose) -----------
print(raw.describe(include="all"))
print(raw.isnull().sum())
print(raw["condition"].value_counts(dropna=False))

# ----------- 4. fix -----------
def clean_stroop(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["rt_ms"] = pd.to_numeric(df["rt_ms"], errors="coerce")
    df = df[df["rt_ms"].between(150, 3000)]
    df["age"] = df["age"].replace({-999: np.nan})
    df["condition"] = (df["condition"].str.lower()
                                       .replace({"incong": "incongruent"}))
    return df

clean = clean_stroop(raw)

# ----------- 5. re-describe -----------
print(clean.describe(include="all"))
print(clean["condition"].value_counts())
print(f"Rows: {len(raw)} → {len(clean)}")

# ----------- 6. analyse -----------
summary = (clean
           .groupby("condition")["rt_ms"]
           .agg(["mean", "std", "count"])
           .round(1))
print(summary)
# 期待：incongruent mean RT > congruent mean RT (Stroop effect)
```

執行後學生可以看到：

1. 兩個 condition (`congruent`, `incongruent`)，而非原本看起來像 4 個。
2. RT 統計從 mean ≈ 千百倍級 (因為混入 99999) 變成合理的 ~500 ms。
3. n 從 200 縮為較小數字 (因為 sentinel + outlier 被剔除)，這個損失必須在 report 中聲明。

---

## 2.5 Cleaning vs. Analysis 的邊界與 pure-function 化 (5 min)

把流程拆成三個 pure functions，方便寫 pytest：

```python
def load_raw(path: str) -> pd.DataFrame:
    """I/O only, no transformation."""
    return pd.read_csv(path)

def clean(df: pd.DataFrame) -> pd.DataFrame:
    """Pure: 不可爭議的修補 (型別、sentinel、編碼)。"""
    ...

def describe(df: pd.DataFrame) -> pd.DataFrame:
    """Pure: 統一格式的健康檢查報表。"""
    ...

def analyse(df: pd.DataFrame, *, outlier_sd: float = 3.0) -> pd.DataFrame:
    """任何「可能影響結論」的決定都放在這裡，並把 parameter 暴露出來。"""
    ...
```

**為什麼這樣分**：

- `clean()` 的決定可重現、結果可預期 → pytest 直接餵假資料測試。
- `analyse()` 的參數 (例如 `outlier_sd=3.0`) 應該寫進 paper / report → 別人能 reproduce 你的結論。
- 兩者混在一起 = 結論依賴一個沒被檢視的清理決定，未來 reviewer 會問到死。

---

## Recap & Common Pitfalls (10 min)

### 一句話總結

> **`@st.cache_data` 讓 dashboard 跑得動；descriptive statistics 讓 dashboard 背後的資料站得住。任何 cleaning 動作都應該對應到一個可觀察的現象，並能說出它的代價。**

### 常見錯誤 cheat sheet

| 症狀 | 通常的原因 | 修法 |
|------|----------|------|
| Slider 動了 dashboard 沒變 | Widget 寫在 `@st.cache_data` 函式內 | 把 widget 拿到函式外，把值當參數傳進去 |
| `UnhashableParamError` | 傳了 dict / DataFrame 進 cached function | 參數加底線 `_` 跳過 hash，或改傳 hashable 版本 |
| `describe()` 看不到關鍵問題 | 數值欄是 `object` dtype，summary 自動跳過 | 先 `pd.to_numeric(errors="coerce")` 再 describe |
| `value_counts()` 沒顯示缺值 | 沒加 `dropna=False` | 永遠用 `value_counts(dropna=False)` |
| 結論隨 cleaning 一改就變 | 把 analysis 決定混在 cleaning 裡 | 把可爭議閾值 (例如 outlier SD) 提到 `analyse()` 並暴露為 parameter |
| `to_datetime` 整欄變 NaT | format 字串對不上 | 用 `errors="coerce"` 並印幾筆原始字串確認格式 |
| `st.set_page_config` 報錯 | 不是第一個 Streamlit 呼叫 | 把它移到所有 `st.*` 之前 |

---

## Homework (作業)

**目標**：用本週介紹的 pipeline (load → describe → fix → re-describe → analyse) 處理一個 messy dataset，並把 cleaning 與 analysis 明確分層。

**繳交內容**（GitHub repo URL 或 `.ipynb`，Week 13 前繳交）：

1. **資料**：使用 §2.4 教師提供的 messy Stroop-like dataset（或自己研究領域的 messy 小資料），存成 `data/raw.csv`。
2. **`pipeline.py`** — 至少包含四個函式：
   - `load_raw(path) -> DataFrame` — 只做 I/O，不做任何轉換。
   - `describe(df) -> dict | DataFrame` — 回傳一個結構化的健康檢查報表 (n、dtype、缺值數、numeric summary、categorical level)。
   - `clean(df) -> DataFrame` — pure function，每一步的 docstring 寫明「觀察 → 動作 → 代價」。
   - `analyse(df, *, outlier_sd=3.0) -> DataFrame` — 計算 condition × subject 的 mean RT 與 Stroop effect，並把任何**可爭議閾值**暴露成 parameter。
3. **`report.ipynb`** — 跑完 pipeline 並回答：
   - cleaning 前後 n、mean RT、condition level 數的對照。
   - 至少列出三個從 descriptive statistics 觀察到的問題，並對應到 `clean()` 的哪一行修補。
   - 說明 outlier 閾值為何放在 `analyse()` 而非 `clean()`。
4. **`tests/test_clean.py`** — 至少一個 pytest 測試：餵入一個含 sentinel (`-999`) 或字串 `"NA"` 的小 DataFrame，驗證 `clean()` 輸出符合預期。

### Rubric

| 項目 | 分數 |
|------|------|
| Pipeline 四層拆分清楚、pure function 正確 | 25% |
| `describe()` 報表結構化、能讀出資料品質 | 15% |
| 每個 cleaning 動作有「觀察 → 動作 → 代價」說明 | 25% |
| Cleaning vs. analysis 邊界正確、outlier 閾值放對位置 | 15% |
| pytest 測試 pass | 10% |
| Report notebook 完整、結論可重現 | 10% |

---

## Tools This Week

| Tool | Purpose | Install |
|------|---------|---------|
| `streamlit` (already installed) | App 框架、`@st.cache_data` / `@st.cache_resource` | — |
| `pandas` | 描述統計與資料修補 | `pip install pandas` |
| `numpy` | 合成 dataset、數值運算 | `pip install numpy` |
| `matplotlib` | histogram、boxplot、missing-value bar | `pip install matplotlib` |
| `pytest` | 測試 `clean()` 與 `analyse()` | `pip install pytest` |

---

## Resources

- [Streamlit caching docs](https://docs.streamlit.io/develop/concepts/architecture/caching) — `@st.cache_data` vs `@st.cache_resource` 官方解說
- [Streamlit execution model](https://docs.streamlit.io/develop/concepts/architecture/run-your-app) — rerun 機制
- [pandas missing data user guide](https://pandas.pydata.org/docs/user_guide/missing_data.html)
- [pandas `describe()` reference](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.describe.html)
- [Tukey, J. W. (1977). *Exploratory Data Analysis*](https://en.wikipedia.org/wiki/Exploratory_data_analysis) — EDA 作為「先看資料、再下結論」的奠基性方法論
- Wickham, H. (2014). *Tidy Data*. Journal of Statistical Software, 59(10). — 為什麼 cleaning 是分析之前的獨立步驟

---

## What Comes Next

| Week | Topic |
|------|-------|
| 13 | Interactive dashboards — Plotly Express 與資料敘事 |
| 14 | AI features — 在 Streamlit app 中呼叫 Claude API |
| 15 | Final project workshop — 同儕互評與 UI polish |
| 16 | **Final milestone:** Live app 簡報 |

> **Open data API 的具體實作** (REST、`requests`、Taiwan open data portal) 將在後續週次或 final project workshop 中按需引入。本週先把通用的 pipeline 心智模型建立起來，未來不論資料來源是什麼，這條 pipeline 都能直接套用。
