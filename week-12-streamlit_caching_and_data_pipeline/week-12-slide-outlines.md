# Week 12 — Slide-by-Slide Outline

> **Source lecture:** `week-12-streamlit_caching_and_data_pipeline.md`
> **Target deck:** ~43 slides, 16:9, ACL@NCU visual style (white BG, navy `#14325C` + teal `#0D9B9B` accents, top thin band on content slides; navy section dividers; amber break slide)
> **Class duration:** 170 min including 10-min break
>
> **Conventions used below**
> - Each slide lists: type, headline, key bullets / visual element, speaker-note hint.
> - "code:" lines are minimal — paste the exact snippet from the lecture .md.
> - Slide types:  `[title]` `[divider]` `[content]` `[code]` `[two-col]` `[table]` `[diagram]` `[practice]` `[recap]` `[break]`

---

## Section 0 — Opening (Slides 1–5)

### Slide 1 — `[title]` Title slide
- **Headline:** Week 12 — Streamlit Caching & The Data Analysis Pipeline
- **Subtitle (CJK):** 從 dashboard 走向「資料是可信的」data app
- **Footer:** NS5116 · ACL@NCU · 2026-05-14 · 張智宏
- **Visual motif:** thin teal top band; centred title; small ACL logo bottom-right

### Slide 2 — `[content]` 為什麼今天要回頭講 `app.py`？
- 上週介紹了 `demo01`–`demo14` 與整合 dashboard `app.py`
- 但因為時間關係，**沒有逐段拆解整合範例**
- 同時 `app.py` 用了一個關鍵元件我們還沒解釋：`@st.cache_data`
- 今天兩件事：
  1. 把 `app.py` 與 caching 講清楚 (前 60 min)
  2. 把視角拉開，談一般化的資料分析流程 (後 90 min)
- **speaker note:** 強調 Open Data API 延後到後續週次

### Slide 3 — `[content]` Learning Objectives (1/2)
- 解讀 `app.py` 的七大區塊與 Streamlit rerun model
- 正確使用 `@st.cache_data` (`ttl`, `max_entries`, `show_spinner`)
- 區分 `@st.cache_data` vs `@st.cache_resource`
- 診斷 `UnhashableParamError` 等典型錯誤
- **visual:** 4-row icon list (rerun icon / cache icon / decorator icon / bug icon)

### Slide 4 — `[content]` Learning Objectives (2/2)
- 描繪通用 data analysis pipeline (load → inspect → describe → fix → re-describe → analyse)
- 用 descriptive statistics 診斷資料品質
- 以觀察驅動方式 (observation-driven) 修補資料
- 區分 cleaning vs analysis 的邊界
- 把流程拆成 pure functions（為 Week 13–16 final project 鋪路）
- **visual:** pipeline mini-icon strip

### Slide 5 — `[table]` Schedule at a Glance
- Two-column table: 段落 / 主題 / 時間
- Highlight 1.3 & 2.3 with teal star ⭐
- Bottom note: 總計 170 min 含 10 min break

---

## Section 1 — `app.py` 拆解與 Streamlit 快取機制 (Slides 6–21)

### Slide 6 — `[divider]` PART 1 — Streamlit App & Caching
- Full navy background
- Large white "PART 1 · 60 min"
- Subtitle: `app.py` × `@st.cache_data`

### Slide 7 — `[content]` 1.1 `app.py` 整體結構導覽
- Scenario: Cognitive Aging Dashboard (n=400 lifespan 認知測驗)
- Sidebar 篩 age / sex / education
- 四個 tabs：Age trajectory / Distributions / By group / Raw data
- **visual:** screenshot thumbnail of running app on right half

### Slide 8 — `[diagram]` 一個典型 Streamlit app 的七大區塊
- Numbered vertical stack with brief description for each:
  1. Page config — `st.set_page_config()`
  2. Constants — `DATA_PATH`, `MEASURES`
  3. Data loading — `@st.cache_data` + `load_data`  ← 今天重點
  4. Sidebar widgets — `st.slider`, `multiselect`
  5. Filtering — boolean mask on DataFrame
  6. Header + KPI — `st.title`, `st.metric`
  7. Tabs — `st.tabs(...)` × 4  ← 主視覺
- **note:** `st.set_page_config()` 必須是第一個 Streamlit 呼叫

### Slide 9 — `[content]` 1.1b Sidebar 的角色 — 把 widget 值接到 filtering
- Streamlit 的 sidebar (`with st.sidebar:`) 把所有「使用者控制」收在左欄；右側留給結果
- `app.py` 的 sidebar 共 5 個 widgets：
  - `st.slider("Age range", value=(20, 80))` → 回傳一個 tuple `(age_min, age_max)`
  - `st.multiselect("Sex", options=["F","M"], default=["F","M"])` → 回傳 list
  - `st.slider("Years of education")` → tuple
  - `st.selectbox("Cognitive measure", options=..., format_func=...)` → 單值
  - `st.checkbox("Show age regression line")` → bool
- **Widget → mask** 的關鍵 pattern：每個 widget 回傳值 **直接** 被組合成 boolean mask
  ```python
  mask = (df_all["age"].between(age_min, age_max)
          & df_all["sex"].isin(sex_choices)
          & df_all["education"].between(edu_min, edu_max))
  df = df_all[mask].copy()
  ```
- **三條 sidebar 設計紀律**：
  1. **`with st.sidebar:` 的 scope** — widgets 寫在 sidebar，篩選邏輯寫在主程式（不要把 logic 也丟進 sidebar）
  2. **`default=` 與 `value=` 要寫死合理初始值** — 否則使用者打開 app 看到空白會困惑
  3. **`format_func` 讓 selectbox 顯示中文標籤、但回傳英文 key** — 內部與顯示分離
- **visual:** sidebar mockup on left → arrows → mask code on right
- **與 caching 的連結**：sidebar widget 是觸發 rerun 的最常見來源 → 為什麼 `load_data()` 必須要 cache

### Slide 10 — `[practice]` 🔬 Hands-on 1: 把 app 跑起來 + 改一個參數
- Task:
  1. `streamlit run app.py`
  2. 把 `"Reaction Time (ms)"` 改成 `"Simple RT (ms)"`
  3. 觀察 "Source file changed. Rerun." 提示
- 思考：為什麼整支程式重新執行？對 `load_data()` 開銷意味著什麼？
- **visual:** screenshot of "Rerun" button highlight

### Slide 11 — `[content]` 1.2 Streamlit 的核心執行模型
- **大字 callout：**
  > 「每當使用者操作任何 widget，Streamlit 都會從頭到尾重新執行整支 `app.py`。」
- **visual:** loop arrow diagram (widget interaction → full script rerun → new UI)

### Slide 12 — `[two-col]` Rerun 的兩個重大後果
- Left ✅ **State management 變簡單** — widget 的值自動傳到下一次 rerun
- Right ⚠️ **昂貴計算被反覆執行** — `load_data()` 每 rerun 重讀一次 CSV
- Bottom callout: 這就是為什麼需要 `@st.cache_data`
- Analogy: `functools.lru_cache` 的 Streamlit 強化版

### Slide 13 — `[code]` 1.3 ⭐ `@st.cache_data` — 核心範例
- Show lines 42–50 of `app.py`:
  ```python
  @st.cache_data
  def load_data(path: Path) -> pd.DataFrame:
      df = pd.read_csv(path)
      df["group"] = pd.Categorical(
          df["group"], categories=["young","middle","older"], ordered=True
      )
      return df
  ```
- Caption: 一個裝飾器，避免 rerun 時重讀 CSV
- **visual:** code block left, "before vs after" speed badges right (e.g., "≈80ms → 0ms")

### Slide 14 — `[content]` Cache key 是怎麼算出來的？
- 三個組成：
  1. 函式名稱 (`load_data`)
  2. 參數的 hash (這裡是 `Path` 字串)
  3. 函式原始碼的 hash — 修改函式內容後舊 cache 自動失效
- **visual:** 3-circle Venn or 3-stack diagram

### Slide 15 — `[content]` 為什麼回傳的是 copy 而不是 reference？
- `@st.cache_data` serialize → deserialize → 回傳 deep copy
- **保證：使用者下游怎麼亂改 DataFrame 都不會污染 cache**
- 短碼示範：
  ```python
  df = load_data(p); df["age"] = -999
  df2 = load_data(p)        # 仍是原值
  ```
- 代價：序列化開銷；大物件 → 用 `@st.cache_resource` (下節)

### Slide 16 — `[table]` `@st.cache_data` 重要參數
| 參數 | 用途 | 何時用 |
|---|---|---|
| `ttl` | time-to-live (秒) | API 資料每小時刷新 |
| `max_entries` | LRU 上限 | 函式被多種 input 呼叫 |
| `show_spinner` | 第一次計算的提示 | 計算 > 1 秒 |
| `persist="disk"` | cache 寫到磁碟 | reload 後仍保留 |
- **visual:** small parameter-card grid

### Slide 17 — `[content]` ⚠️ 常見錯誤 1 — Widget 寫在 cached function 內
- ❌
  ```python
  @st.cache_data
  def bad_load():
      n = st.slider("rows", 10, 100)   # slider 不會觸發重算
      return df.sample(n)
  ```
- ✅ 在外面讀 widget，把值當參數傳進去

### Slide 18 — `[content]` ⚠️ 常見錯誤 2 & 3
- **錯誤 2：UnhashableParamError** — 用底線 `_params` 跳過 hash（但需自負正確性）
- **錯誤 3：Side effect 被略過** — `print()`、寫檔在第二次呼叫不會執行
- **visual:** two side-by-side error cards (red border)

### Slide 19 — `[practice]` 🔬 Hands-on 2: 觀察 cache 行為
- 在 `load_data()` 內加 `print("DEBUG: reading CSV")`
- 對照三種設定：
  1. 有 `@st.cache_data` → 只印一次
  2. 拿掉裝飾器 → 每次 slider 都印
  3. `@st.cache_data(ttl=10)` → 10 秒後第一次互動觸發重讀
- **visual:** terminal log mock-up showing 3 scenarios

### Slide 20 — `[table]` ⭐ 1.4 `@st.cache_data` vs `@st.cache_resource`
| | `@st.cache_data` | `@st.cache_resource` |
|---|---|---|
| 回傳值 | deep copy | 同一個 reference (singleton) |
| 適用 | DataFrame, array, JSON | DB / model / LLM client |
| 跨 session | 各自快取 | 共享物件 |
- 範例：Week 14 Anthropic client
  ```python
  @st.cache_resource
  def get_anthropic_client():
      from anthropic import Anthropic
      return Anthropic(api_key=st.secrets["ANTHROPIC_API_KEY"])
  ```

### Slide 21 — `[content]` Decision rule
- **大字 callout：**
  > **要的是「資料」？用 `cache_data`。**
  > **要的是「資源 / 連線 / 物件」？用 `cache_resource`。**
- **visual:** balance-scale icon

---

## Break

### Slide 22 — `[break]` 🔄 BREAK · 10 min
- Amber background `#FBEAC0`
- Large clock or coffee icon
- Subtitle: 回來繼續 — Data Analysis Pipeline

---

## Section 2 — Data Analysis Pipeline (Slides 23–39)

### Slide 23 — `[divider]` PART 2 — The Data Analysis Pipeline
- Full navy background
- "PART 2 · 90 min"
- Subtitle: descriptive statistics × observation-driven fixing
- Footer note: Open Data API 延後至後續週次

### Slide 24 — `[content]` 2.1 為什麼今天先講通用流程？
- 不論資料來自 CSV、API、PsychoPy log、SQL、fMRI volume
- raw data → analysable data 永遠隔著相同三步
- 跳過 → 結論與雜訊綁在一起
- **visual:** four source icons (CSV / API / log / brain) all funnelling into one pipeline

### Slide 25 — `[diagram]` ⭐ 完整 Pipeline — load → inspect → describe → fix → re-describe → analyse
- Vertical 6-step flowchart (use the ASCII diagram from §2.1 as visual reference):
  1. **load** — I/O only
  2. **inspect** — shape / dtypes / head
  3. **describe (diagnose)** — descriptive statistics ← 今天重點
  4. **fix** — observation-driven ← 今天重點
  5. **re-describe** — 驗證 fix 沒引入新問題
  6. **analyse / visualise** — 回答研究問題
- Right side: teal star on steps 3 & 4

### Slide 26 — `[two-col]` 兩個常見誤區
- Left ❌ **跳過 describe 直接畫圖**
  → 你只看到前幾行；第 32 row 的 RT = 99999 不會被發現
- Right ❌ **先 `df.dropna()` 再說**
  → 沒看缺值樣態 (隨機？系統？某 condition 集中？) 容易引入 selection bias
- **visual:** two warning-card layout (red border)

### Slide 27 — `[practice]` 🔬 Hands-on 3: 替 `app.py` 標出 pipeline 位置
- 問題：
  1. 哪一行是 `load`？
  2. 哪一段是 `analyse / visualise`？
  3. **缺少哪幾步**？對合成資料合理嗎？對真實資料呢？
- 預期答案 (折疊): `load_data()` 在第 56 行；tabs 內畫圖；缺 inspect / describe / fix / re-describe

### Slide 28 — `[content]` 2.2 ⭐ Descriptive Statistics 作為「健康檢查」
- 重新定位：不是「論文 Table 1」，而是 **資料品質的診斷儀器**
- 五件每次都做的事：
  ```python
  df.shape
  df.dtypes
  df.isnull().sum()
  df.describe(include="all")
  df["col"].value_counts(dropna=False)
  ```
- 關鍵：跑完之後 **問「這合不合理？」**

### Slide 29 — `[table]` ⭐ 從 summary statistics 讀出問題 — 速查表
- Full-slide table (use abridged version of §2.2.2):
  | 現象 | 可能的問題 |
  |---|---|
  | 某欄 count 較少 | 大量缺值 |
  | dtype 是 object，但內容像數字 | 混入 "NA" / "-" / 空字串 |
  | min/max 物理上不可能 | sentinel value / 編碼錯誤 |
  | mean ≠ median | 偏斜或極端 outlier |
  | std 異常大 / ≈ 0 | outlier 或近常數 |
  | value_counts 出現 "NA","-","",999 | 缺值偽裝 |
  | level 重複 ("M","male","Male") | 編碼不一致 |
  | 某 condition trial 數遠少 | 不平衡 / logging 失敗 |
- **visual motif:** alternating row shading

### Slide 30 — `[content]` 視覺化也是 descriptive statistics
- 三張每個 dataset 都該畫一次：
  - `df.hist()` — 每欄分佈
  - `df.plot.box()` — outlier 一目了然
  - `df.isnull().sum().plot.bar()` — 缺值集中在哪幾欄
- 數字摘要會 average-out 結構性問題；圖才看得到
- **visual:** 3-mini-thumbnails of these plots

### Slide 31 — `[practice]` 🔬 Hands-on 4: 從 summary 讀出三個問題
- 情境：n=200 Stroop trial dataset，刻意 messy
- 顯示 dataset 生成 code (簡版)
- 任務：用 `info()` / `describe(include="all")` / `isnull().sum()` / `value_counts(dropna=False)` 找出至少三個問題
- 折疊預期答案：
  - `rt_ms` dtype = object → 含 "NA"
  - max = 99999 → sentinel
  - `condition` 4 個 level 但其實 2 個 (大小寫不一致)
  - `age` 有 -999 sentinel + NaN

### Slide 32 — `[content]` 2.3 ⭐ Observation-Driven Fixing — 核心原則
- **大字 callout：**
  > **每一個 cleaning 動作都應對應到 §2.2 的具體觀察，且你能說出代價。**
- **visual:** 「觀察 → 動作 → 代價」三聯式箭頭

### Slide 33 — `[table]` ⭐ 觀察 → 動作 → 代價 對應表
- Full-slide table (use §2.3.1 abridged):
  | 觀察 | 動作 | 代價 |
  |---|---|---|
  | object dtype 像數字 | `pd.to_numeric(errors="coerce")` | 無法解析 → NaN 悄悄發生 |
  | sentinel 偽裝缺值 | `replace(...)` 再 `to_numeric` | 漏掉 sentinel 就污染分析 |
  | 缺值少且隨機 | `dropna(subset=...)` | 損失 n |
  | 缺值多 / 系統性 | `fillna(策略)` | 填補本身是一個假設 |
  | 物理不可能值 | `between(...)` filter | 範圍錯 → 剔除真實 outlier |
  | categorical 不一致 | `str.lower()` + `replace` | 合併不該合的 level |
  | time 非 datetime | `pd.to_datetime(errors="coerce")` | format 不對整欄變 NaT |

### Slide 34 — `[content]` 三條 cleaning 紀律
1. **每步留 log** — `print(f"dropna: {before} → {len(df)}")`
2. **改完再跑一次 `describe()`** — 沒驗證 = 沒做
3. **不要 chain method** — 一行一動作，error 才追得到
- Right: 並排顯示 chain (❌) vs step-by-step (✅) 程式碼

### Slide 35 — `[content]` ⚠️ 兩種錯誤模式
- **錯誤 A：無腦 `dropna()`**
  - 如果 age 缺值集中在年長者 → 系統性低估 cognitive aging 效應
- **錯誤 B：把 analysis 偽裝成 cleaning**
  ```python
  df = df[df["rt_ms"] < df["rt_ms"].mean() + 3 * df["rt_ms"].std()]
  ```
  - 這條 outlier rule 直接影響 condition mean → 屬於 analysis decision
- **visual:** two warning cards

### Slide 36 — `[practice]` 🔬 Hands-on 5: 把觀察寫成 `clean_stroop(df)`
- 任務：用 Practice 4 觀察到的問題寫 cleaning function
- 註解必須寫出「觀察 → 動作 → 代價」
- 折疊參考解答（簡版 4 步：to_numeric / between / replace -999 / lower + replace）
- 檢查：cleaning 前後跑 `describe(include="all")` 對照

### Slide 37 — `[code]` ⭐ 2.4 端到端 mini-pipeline (Stroop demo)
- One-slide compact code (split into commented sections):
  1. load → 2. inspect → 3. describe → 4. fix → 5. re-describe → 6. analyse
- Bottom: 預期觀察
  - condition 從看似 4 個 → 2 個
  - mean RT 被 99999 sentinel 拉高到數千 ms → 清理後回到約 500ms
  - n 損失來自 invalid / implausible `rt_ms`，需在 report 聲明
  - 若要示範真正 Stroop effect，生成資料時讓 incongruent trials 額外增加約 50–80ms；否則只把 groupby 當作 cleaned-data summary
- **visual:** number-badge每段標 1–6

### Slide 38 — `[content]` 2.5 Cleaning vs Analysis 的邊界
- 四層 pure-function 分離：
  ```text
  load_raw(path)   # I/O only
  clean(df)        # 不可爭議的修補
  describe(df)     # 健康檢查報表
  analyse(df, *, outlier_sd=3.0)   # 可爭議閾值暴露為參數
  ```
- 為什麼這樣分：
  - `clean()` 可用 pytest 直接驗
  - `analyse()` 的 parameter 寫進 paper → 可 reproduce
- 對 reproducibility / pre-registration 至關重要

### Slide 39 — `[content]` 一個檢驗問題
- **大字 callout：**
  > 「如果換另一位研究者，這個操作會做同一個決定嗎？」
- 是 → `clean()`
- 否 → `analyse()` 並把決定寫進 report
- **visual:** decision-tree mini-diagram

---

## Section 3 — Wrap-up (Slides 40–43)

### Slide 40 — `[recap]` 一句話總結
- **大字 callout：**
  > **`@st.cache_data` 讓 dashboard 跑得動；descriptive statistics 讓 dashboard 背後的資料站得住。**
  > **任何 cleaning 動作都應對應到一個可觀察的現象，並能說出它的代價。**

### Slide 41 — `[table]` 常見錯誤 cheat sheet
- 7-row table from "Recap" section:
  - Slider 動了 dashboard 沒變 → widget 寫在 cache 內
  - UnhashableParamError → 加底線 `_`
  - describe 看不到問題 → 先 to_numeric
  - value_counts 沒顯示缺值 → 加 `dropna=False`
  - 結論隨 cleaning 一改就變 → 提到 analyse 並暴露參數
  - to_datetime 整欄 NaT → format 不對
  - set_page_config 報錯 → 不是第一個 Streamlit 呼叫

### Slide 42 — `[content]` Homework
- 用 pipeline 處理 messy Stroop-like dataset
- 交付：
  1. `pipeline.py` — `load_raw` / `describe` / `clean` / `analyse` 四個 pure functions
  2. `report.ipynb` — cleaning 前後對照 + 至少三個觀察→修補對應 + 為何 outlier 在 `analyse`
  3. `tests/test_clean.py` — 至少一個 pytest
- Due: 2026-05-20 (Week 13 前)
- Rubric 連結：講義 §Homework
- **visual:** deliverable checklist

### Slide 43 — `[content]` What Comes Next
- Week 13 — Plotly Express 與資料敘事
- Week 14 — Anthropic SDK + Streamlit
- Week 15 — Final project workshop
- Week 16 — Live app 簡報
- Footer note: Open data API 將在 final project workshop 按需引入
- **visual:** horizontal timeline with 4 nodes; current week highlighted

---

## Build notes for `build_slides.py`

- **Palette** (reuse Week 11): `BG_WHITE`, `BG_OFFWHITE`, `BG_SECTION = #14325C`, `BG_BREAK = #FBEAC0`, `ACCENT_TEAL = #0D9B9B`, `ACCENT_AMBER`, `ACCENT_RED`, `CODE_BG = #1E293B`
- **Fonts:** Calibri (Latin), Microsoft JhengHei (CJK), Consolas (code)
- **Visual motif (carry across deck):** 0.14" teal top band on all content slides; navy full-bleed for dividers; amber for break; thin hairline `#E2E6EC` separators
- **Typography:** title 36pt bold (CJK); section eyebrow 14pt teal uppercase; body 16–18pt; code 14pt mono
- **Slide count:** 43 slides for 170 min ≈ 4 min/slide average (Part 1 denser, divider/break/recap faster)
- **Star marker ⭐ slides** (deserve extra design attention): 13, 20, 25, 28, 29, 32, 33, 37
- **Hands-on slides** (5 total: 10, 19, 27, 31, 36) — use consistent 🔬 badge + light-teal background tint to distinguish from didactic slides
- **Code slides** — dark `CODE_BG` rectangle, syntax-highlight comments in `CODE_COMMENT` muted blue
