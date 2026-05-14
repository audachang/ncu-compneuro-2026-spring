# Week 13: Interactive Dashboards & Data Storytelling — 兩個大型資料集走完整 Pipeline

> **Course:** NS5116 Programming & AI Applications in Behavioral Science — Spring 2026
> **Week:** 13 of 16 | **Date:** 2026-05-21 | **Room:** TBA

---

## 本週主軸 (Why This Matters)

Week 12 我們建立了 **資料分析 pipeline 的心智模型**：
`load → inspect → describe → diagnose → fix → re-describe → analyse`。當時為了集中討論 cleaning 與 caching，我們刻意使用一筆 400-row 的合成 Stroop-like dataset。

本週我們**換上兩個真正的大型資料集 (≥ 1,000 rows)**，把同一條 pipeline 完整跑兩遍：

| Dataset | 來源 | 規模 | 為什麼選它 |
|---------|------|------|-----------|
| **Dataset A** — PsyArXiv preprints | OSF API (`api.osf.io`) | 課堂抓取約 1,000 筆（10 pages × 100/page，最新發表） | 心理學家「正在討論什麼」— preprint metadata 是 free-form keyword + subject taxonomy 的真實 JSON |
| **Dataset B** — 大專校院校別學生數 | 教育部統計處 (`stats.moe.gov.tw`) | 105–113 學年度合併後約 7,200 列 | 台灣 **少子化 (declining birth rate)** 對高教的衝擊 — 政策議題、學生切身相關 |

兩個 dataset 同時也代表 open data 的兩種典型形態：
- A 是 **REST API**，需要做 **pagination + JSON parsing**；
- B 是 **bulk CSV**，需要做 **跨年度 schema alignment**。

走完這兩遍，學生會看到：

> 同一條 pipeline 對「行為科學研究文獻」與「政府公開統計」都適用，差別只在 load 那一段。

把資料「載進來」之後，剩下的 clean / describe / analyse 邏輯幾乎共用。這正是 pandas + Plotly 這組工具被廣泛採用的原因。

學期脈絡：Week 11 學會「畫出 dashboard」→ Week 12 學會「**讓 dashboard 背後的資料是可信的**」→ **Week 13 用真實大型資料把流程走兩遍，並讓圖表互動化** → Week 14 (Anthropic SDK) 讓 dashboard 具備 AI 解讀能力。

---

## Learning Objectives (學習目標)

修完本週後，你應該能夠：

1. **用 `requests` 與 pagination 模式** 從 REST API 取得 ≥ 1,000 筆資料，並把巢狀 JSON 攤平成 tidy DataFrame。
2. **從教育部統計處下載多年度 CSV** 並用 `pd.concat` 對齊欄位差異，建立 schema 統一的 long-format DataFrame。
3. **把 Week 12 的 `clean()` / `describe()` / `analyse()` 三層架構**，套用到 ≥ 1,000 列的真實資料集，並能對每個 cleaning 決定說明「觀察 → 動作 → 代價」。
4. **使用 Plotly Express** 製作 bar、line、scatter、stacked-bar 等互動圖表，並善用 `hover_data`、`color`、annotation 強化敘事。
5. **將 Plotly 圖嵌入 Streamlit** (`st.plotly_chart`)，讓 Week 11/12 的 dashboard 升級為可互動圖表。
6. **比較兩個不同來源資料集** 的 pipeline 差異 (API vs. CSV、英文 vs. 中文、研究 vs. 政策)，並能說出共用的部分為什麼是共用的。
7. **應用 data storytelling 五原則**：one message per chart、context before detail、label what matters、show uncertainty、earn the complexity。

---

## Schedule at a Glance

| 段落 | 主題 | 時間 |
|------|------|------|
| Part 1.1 | 為什麼換到 Plotly：互動性是 dashboard 的第一公民 | 10 min |
| Part 1.2 | Plotly Express 與 Streamlit 的整合 | 10 min |
| **Dataset A — PsyArXiv (50 min)** | | |
| Part 2.1 | API + pagination：從 OSF 抓 1,000 筆 preprint | 15 min |
| Part 2.2 | JSON → DataFrame、clean、describe | 15 min |
| Part 2.3 | 三張 Plotly 圖 — bar / line + annotation / scatter | 20 min |
| **Break** | | 10 min |
| **Dataset B — 教育部高教統計 (50 min)** | | |
| Part 3.1 | 跨年度 CSV 合併與 schema alignment | 15 min |
| Part 3.2 | 中文欄位、欄位編碼、缺值診斷 | 15 min |
| Part 3.3 | 三張 Plotly 圖 — 趨勢 + annotation / stacked bar / city distribution | 20 min |
| Part 4 | Data storytelling 五原則 + Altair 簡介 | 15 min |
| Recap | 重點回顧 & Homework brief | 10 min |

總計：約 170 分鐘 (含 10 min break)。

---

## Tools This Week

| Tool | Purpose | Install |
|------|---------|---------|
| `requests` | API call / CSV download | `pip install requests` (Week 12) |
| `pandas` | DataFrame ops, `pd.concat`, `groupby` | (Week 12) |
| `plotly` | Interactive charts | `pip install plotly` |
| `altair` | (optional) Declarative alternative | `pip install altair` |
| `streamlit` | Embed charts in dashboard | (Week 11) |

`pip install plotly` 之後，import 慣例：

```python
import plotly.express as px
import plotly.graph_objects as go   # 只在 px 做不到的時候才用
```

---

# Part 1 — Why Plotly?

## 1.1 從靜態到互動 (10 min)

Matplotlib 產生發表級的 **靜態圖**，適合論文；Plotly 產生 **互動圖**：滑鼠 hover 顯示數值、可放大、拖曳、按 legend 篩選 trace。在 Streamlit dashboard 中，這是「使用者可以自己探索資料」與「研究者把結論硬塞給讀者」的差別。

| 任務 | Matplotlib | Plotly |
|------|------------|--------|
| 論文 figure | ✅ 首選 | ⚠ 出版社 PDF 流程不友善 |
| 探索期 EDA (exploratory data analysis) | ⚠ 缺 hover | ✅ 一行程式碼就有 hover |
| Streamlit / Web dashboard | ❌ 只能存圖 | ✅ 原生支援 |
| 嵌入 Jupyter notebook | ✅ | ✅ |

**註**：Plotly 並不是要取代 Matplotlib，而是當輸出對象變成「瀏覽器」時的合理選擇。本課程 Week 7 學的 Matplotlib 知識完全沒有浪費 — 兩者的 figure → axes → trace 心智模型相通。

## 1.2 Plotly Express 與 Streamlit 整合 (10 min)

`plotly.express` (慣稱 `px`) 是高階介面，一行 function call 對應一種圖。對應到 Streamlit：

```python
import plotly.express as px
import streamlit as st

fig = px.bar(df, x="city", y="n_students")
st.plotly_chart(fig, use_container_width=True)
```

`st.plotly_chart()` 直接吃 figure 物件，不用先 `.show()`。`use_container_width=True` 讓圖隨欄寬縮放，這在 `st.columns()` 排版時很重要。

**注意**：若你的 figure 在 Jupyter 用 `fig.show()` 開新 tab 看不到，是因為 backend 沒裝；在 Streamlit 中不會有這問題。

---

# Part 2 — Dataset A: PsyArXiv Preprints (心理學研究最新動態)

## 2.1 API + Pagination：抓 1,000 筆 (15 min)

OSF (Open Science Framework) 的 PsyArXiv preprint server 是心理學界重要的 preprint 倉庫。它的總筆數會持續變動，所以本課程不記一個固定數字；我們只抓 **最近發表的 1,000 筆**（10 頁 × 每頁 100）做趨勢分析。

*📄 [`code/osf_psyarxiv_pipeline.py`](code/osf_psyarxiv_pipeline.py)*

```python
import time

import requests

OSF_ENDPOINT = "https://api.osf.io/v2/preprint_providers/psyarxiv/preprints/"

def fetch_psyarxiv(n_pages: int = 10) -> list[dict]:
    """抓最近 n_pages * 100 筆 PsyArXiv preprints。"""
    all_items = []
    for page in range(1, n_pages + 1):
        params = {
            "page": page,
            "page[size]": 100,           # OSF 單頁上限
            "sort": "-date_published",   # 最新優先
        }
        r = requests.get(
            OSF_ENDPOINT,
            params=params,
            timeout=30,
            headers={"User-Agent": "NS5116-week13-teaching-example"},
        )
        r.raise_for_status()
        all_items.extend(r.json().get("data", []))
        time.sleep(0.3)                  # 禮貌等待，避免被 rate-limit
    return all_items
```

**關鍵概念**：

- **Pagination (分頁)**：API 不可能一次給你全部，必須 loop 直到拿完。OSF 的 page size 上限是 100。
- **Rate limit (流量限制)**：`time.sleep(0.3)` 約等於每秒 3 個 request，遠低於 OSF 的 limit (每分鐘 100 次)。
- **`r.raise_for_status()`**：當 HTTP status 不是 200 時自動 raise exception，比手動 if check 安全。

### 🔬 Hands-on Practice 1: 改抓 oldest preprints

**任務**：把 `sort` 從 `-date_published` 改成 `date_published` (去掉減號)，重跑一次。觀察 `df["date_published"].min()` 變到哪一年。

<details>
<summary>✅ 預期觀察</summary>

OSF 上 PsyArXiv 大約從 2016 年開始有 preprint。改用正向排序後，會看到 2016–2017 年的最早一批；對比之下 `n_tags` 平均較低（早期作者還不熟悉 tagging 文化）。
</details>

<details>
<summary>✅ 參考解答</summary>

```python
import time

import pandas as pd
import requests

OSF_ENDPOINT = "https://api.osf.io/v2/preprint_providers/psyarxiv/preprints/"

items = []
for page in range(1, 3):
    params = {"page": page, "page[size]": 100, "sort": "date_published"}
    r = requests.get(
        OSF_ENDPOINT,
        params=params,
        timeout=30,
        headers={"User-Agent": "NS5116-week13-teaching-example"},
    )
    r.raise_for_status()
    items.extend(r.json().get("data", []))
    time.sleep(0.3)

df = pd.DataFrame([
    {
        "title": it["attributes"].get("title"),
        "date_published": it["attributes"].get("date_published"),
    }
    for it in items
])
df["date_published"] = pd.to_datetime(df["date_published"], errors="coerce", utc=True)
print(df["date_published"].min())
print(df[["date_published", "title"]].head())
```
</details>

---

## 2.2 JSON → DataFrame → Clean → Describe (15 min)

OSF 回傳的是巢狀 JSON（`subjects` 是 list of lists），先攤平成 tidy DataFrame：

```python
import pandas as pd

def parse_to_df(items: list[dict]) -> pd.DataFrame:
    records = []
    for it in items:
        a = it["attributes"]
        subjects = a.get("subjects", [])
        # 每個 subject chain 取最後一層 (most specific label)
        leaf_subjects = [
            chain[-1].get("text")
            for chain in subjects
            if chain and chain[-1].get("text")
        ]
        records.append({
            "id": it.get("id"),
            "title": a.get("title", "").strip(),
            "date_published": a.get("date_published"),
            "tags": a.get("tags", []),
            "n_tags": len(a.get("tags", [])),
            "primary_subject": leaf_subjects[0] if leaf_subjects else None,
            "n_description_chars": len(a.get("description") or ""),
        })
    return pd.DataFrame(records)
```

清理函式遵守 Week 12 的「**觀察 → 動作 → 代價**」紀律：

```python
import pandas as pd

def clean(df: pd.DataFrame) -> pd.DataFrame:
    """
    觀察 → 動作 → 代價
    1. date_published 是 ISO string → pd.to_datetime
       代價：少數無 date 的會變 NaT，後續 plot 自動忽略。
    2. title 可能是空字串 → filter out
       代價：失去 < 1%，但避免被空字串污染。
    3. primary_subject 缺值 → 填 'Unspecified'
       代價：可能掩蓋編碼問題；但相較直接 dropna 更保留 n。
    """
    df = df.copy()
    df["date_published"] = pd.to_datetime(df["date_published"], errors="coerce", utc=True)
    df["year_month"] = (df["date_published"].dt.tz_convert(None)
                          .dt.to_period("M").dt.to_timestamp())
    df["title_len"] = df["title"].str.len()
    df = df[df["title"].str.len() > 0].copy()
    df["primary_subject"] = df["primary_subject"].fillna("Unspecified")
    return df
```

跑完 `describe()` 你應該看到類似輸出（實際數字會隨抓取時間變動）：

```
n rows           : 1000
date range       : 2026-04-XX  →  2026-05-XX
unique subjects  : ~120
n_tags  (M / SD) : 4.3  /  3.4
desc len (M / SD): 1500  /  420

top 5 subjects:
Social and Behavioral Sciences    ~80
Cognitive Neuroscience            ~50
Developmental Psychology          ~40
Clinical Psychology               ~35
Meta-science                      ~30
```

### 🔬 Hands-on Practice 2: 找出 outlier preprints

**任務**：哪些 preprint 的 `title_len` 超過 200 字元？哪些的 `n_tags == 0`？分別印出前 5 個 title。

<details>
<summary>💡 提示</summary>

```python
df.nlargest(5, "title_len")[["title", "title_len"]]
df[df["n_tags"] == 0]["title"].head()
```
</details>

<details>
<summary>✅ 參考解答</summary>

```python
long_titles = df.nlargest(5, "title_len")[["title", "title_len"]]
no_tag_titles = df.loc[df["n_tags"] == 0, ["title", "date_published"]].head(5)

print("Title length outliers")
print(long_titles.to_string(index=False))

print("\nPreprints with no tags")
print(no_tag_titles.to_string(index=False))
```
</details>

**討論**：`n_tags == 0` 對之後的關鍵字分析意味著什麼？這是 cleaning 還是 analysis decision？(對照 Week 12 Module 6 的邊界討論)。

---

## 2.3 Plotly 三張圖 — Bar / Line + Annotation / Scatter (20 min)

### 2.3.1 Bar — Top subjects

```python
import plotly.express as px

counts = (df["primary_subject"]
            .value_counts().head(15)
            .reset_index())
counts.columns = ["subject", "n"]

fig = px.bar(
    counts, x="n", y="subject", orientation="h",
    color="n", color_continuous_scale="Blues",
    title="Top 15 PsyArXiv subjects (recent ~1000 preprints)",
    labels={"n": "Number of preprints", "subject": "Primary subject"},
)
fig.update_layout(yaxis={"categoryorder": "total ascending"},
                  coloraxis_showscale=False)
fig.show()
```

- `orientation="h"` 讓 subject label 不會擠在 x 軸。
- `color_continuous_scale="Blues"` 用顏色強化排序差異 — **earn the complexity**：是有意義的加值，不是裝飾。

### 2.3.2 Line + Annotation — 每月發表數量

```python
import plotly.express as px

monthly = (df.dropna(subset=["year_month"])
             .groupby("year_month").size()
             .reset_index(name="n_preprints"))

fig = px.line(
    monthly, x="year_month", y="n_preprints", markers=True,
    title="PsyArXiv preprints per month",
    labels={"year_month": "Month", "n_preprints": "Number of preprints"},
)

peak = monthly.loc[monthly["n_preprints"].idxmax()]
fig.add_annotation(
    x=peak["year_month"], y=peak["n_preprints"],
    text=f"Peak: {int(peak['n_preprints'])} preprints",
    showarrow=True, arrowhead=2,
    bgcolor="rgba(255,255,255,0.8)", bordercolor="black",
)
fig.update_layout(hovermode="x unified")
```

**Storytelling 原則**：annotation **解釋為什麼這點重要**，不是只標籤資料點。例如可以改成「Peak — coincides with APS conference deadline」這種帶 domain 解釋的句子。

### 2.3.3 Scatter — title length vs. tag count

```python
import plotly.express as px

fig = px.scatter(
    df, x="n_tags", y="title_len",
    color="primary_subject",
    hover_name="title",
    hover_data={"date_published": True, "primary_subject": True},
    opacity=0.6,
    title="PsyArXiv preprints — title length vs. tag count",
    labels={"n_tags": "Number of tags", "title_len": "Title length (chars)"},
)
fig.update_layout(showlegend=False)  # 100+ subjects 的 legend 會擋畫面
```

**為什麼這張圖有用**：scatter 是 EDA 的主力工具。`hover_name="title"` 讓你滑鼠移過去就能看到具體論文標題，比看 raw DataFrame 更直觀。

### 🔬 Hands-on Practice 3: 加上 trendline

**任務**：在 scatter plot 中加上 `trendline="ols"` 參數，看 `n_tags` 與 `title_len` 是否有線性關係。

<details>
<summary>💡 提示</summary>

`px.scatter(..., trendline="ols")` 需要 `pip install statsmodels`。執行後 hover 黑色線可以看到 OLS 係數與 R²。

**討論**：如果 R² 很低（< 0.05），你會怎麼向 reviewer 報告這張圖？
</details>

<details>
<summary>✅ 參考解答</summary>

```python
import plotly.express as px

fig = px.scatter(
    df,
    x="n_tags",
    y="title_len",
    color="primary_subject",
    hover_name="title",
    trendline="ols",
    opacity=0.6,
    title="PsyArXiv preprints — title length vs. tag count",
    labels={"n_tags": "Number of tags", "title_len": "Title length (chars)"},
)
fig.update_layout(showlegend=False)
fig.show()
```

若 R² 很低，報告方式應該是：「在最近抓取的 PsyArXiv preprints 中，tag 數與 title length 沒有明顯線性關係；這張圖比較適合作為資料品質與 outlier 檢查，而不是支持理論主張。」
</details>

---

# Part 3 — Dataset B: 教育部高教統計 (台灣少子化議題)

## 3.1 跨年度 CSV 合併 (15 min)

教育部統計處每學年度提供獨立的 CSV。我們抓 **105–113 學年度共 9 年**，合併後約 **7,200 列**。

*📄 [`code/moe_higher_ed_pipeline.py`](code/moe_higher_ed_pipeline.py)*

```python
import pandas as pd
import requests
from io import StringIO

MOE_URL = "https://stats.moe.gov.tw/files/detail/{year}/{year}_student.csv"

def fetch_year(year: int) -> pd.DataFrame:
    url = MOE_URL.format(year=year)
    r = requests.get(url, timeout=30, headers={"User-Agent": "NS5116-week13-teaching-example"})
    r.raise_for_status()
    # 教育部 CSV 是 UTF-8 with BOM
    df = pd.read_csv(StringIO(r.content.decode("utf-8-sig")))
    df["學年度"] = year   # 早年欄位沒這欄，這裡補上確保有
    return df

def fetch_all(years=range(105, 114)) -> pd.DataFrame:
    parts = [fetch_year(y) for y in years]
    return pd.concat(parts, ignore_index=True, sort=False)
```

**`pd.concat` 的關鍵參數**：

- `ignore_index=True`：拋掉每個 DataFrame 自己的 index，重新編號 0…N-1。
- `sort=False`：保留原始欄位順序，不要按字母排序。
- 不同年度欄位數量不一樣（105–106 有 23 欄，107+ 有 26 欄，113 有 28 欄）。concat 會自動把缺欄位補成 NaN，**這正是 schema 對齊的核心機制**。

### 🔬 Hands-on Practice 4: 確認 schema 對齊

**任務**：跑 `fetch_all()` 之後執行 `df.isna().mean().sort_values(ascending=False).head(10)`，找出哪些欄位缺值比例最高。對照原始 CSV，這些欄位是「真的缺值」還是「某些年度沒這個欄位」？

<details>
<summary>✅ 預期觀察</summary>

「縣市名稱」、「體系別」在 105–106 學年度可能不存在 → concat 後變 NaN。這 **不是真的缺值**，是 schema evolution 的痕跡。`clean()` 階段要做的判斷是：**對需要這個欄位的分析，要不要 filter 掉早年資料？**
</details>

---

## 3.2 中文欄位的清理 (15 min)

這份資料展示了 Week 12 沒有遇到的兩種狀況：

1. **欄位本身有 prefix code**：「縣市名稱」實際內容是 `"30 臺北市"`，要 `str.extract` 拆出中文名。
2. **學校類型不在欄位中，要從學校名稱推導**：`"國立..."` → 公立，否則私立。

```python
import pandas as pd

def clean(df: pd.DataFrame) -> pd.DataFrame:
    """
    觀察 → 動作 → 代價
    1. 「縣市名稱」格式 "30 臺北市"  →  str.extract 拆出 city_name
       代價：若有格式異常（例如沒有空白）會 NaN。
    2. 「總計」型別應為 numeric 但讀進來是 object  →  pd.to_numeric(errors="coerce")
       代價：少數無法解析的列變 NaN。
    3. 「體系別」105–106 學年度沒有  →  fillna("未分類")
       代價：混入後可能影響跨年度 groupby 的均勻性。
    4. 公私立沒有直接欄位  →  從學校名稱推導 (rule-based)
       代價：rule 失誤的學校會被誤判，需 spot-check。
    """
    df = df.copy()

    df["city_name"] = (df["縣市名稱"].astype(str)
                          .str.extract(r"(?:\d+\s*)?(\S+)$")[0])

    for col in ("總計", "男生計", "女生計"):
        if col in df.columns:
            df[col] = pd.to_numeric(
                df[col].astype(str).str.replace(",", "", regex=False),
                errors="coerce",
            )

    df["sector"] = df["學校名稱"].astype(str).apply(
        lambda s: "公立" if s.startswith(("國立", "市立", "省立", "國防", "警察")) else "私立"
    )

    if "體系別" in df.columns:
        df["system"] = (df["體系別"].astype(str)
                          .str.replace(r"^\d+\s*", "", regex=True)
                          .replace({"nan": "未分類"}).fillna("未分類"))

    return df
```

**Describe 預期結果**：

```
n rows         : ~7,200
學年度 range   : 105 → 113
unique schools : ~170
unique cities  : ~21 (台灣本島 + 外島)
總計 (M / SD)  : ~1,350  /  ~2,570
Top 5 by 平均學生數: 臺大, 成大, 陽明交大, 淡江, 銘傳
```

### 🔬 Hands-on Practice 5: 公私立 rule 的失誤

**任務**：印出所有被分類為「公立」的學校名稱去重後的 list。有沒有看起來不對的（例如某些「私立科技大學」開頭剛好不是「國立」但實際是公立）？

<details>
<summary>💡 提示</summary>

```python
df.loc[df["sector"] == "公立", "學校名稱"].unique()
df.loc[df["sector"] == "私立", "學校名稱"].unique()[:30]
```

「市立」開頭的學校如臺北市立大學是公立，已在 rule 中處理。但若有「國防大學」、「警察大學」這類軍警校院，需要額外規則。**這正是 rule-based cleaning 的限制**。
</details>

<details>
<summary>✅ 參考解答</summary>

```python
public_schools = sorted(df.loc[df["sector"] == "公立", "學校名稱"].dropna().unique())
private_schools = sorted(df.loc[df["sector"] == "私立", "學校名稱"].dropna().unique())

print("公立學校")
for name in public_schools:
    print(name)

print("\n私立學校前 30 筆")
for name in private_schools[:30]:
    print(name)
```

**檢查重點**：如果你看到「國防」、「警察」等不以「國立 / 市立 / 省立」開頭、但實際上不是私立的學校，代表 `sector` 不能只靠 `startswith()` 一行解決。
</details>

---

## 3.3 Plotly 三張圖 — 趨勢 + Annotation / Stacked Bar / City (20 min)

### 3.3.1 Line + Annotation — 總學生數逐年下降

```python
import plotly.express as px

agg = df.groupby("學年度")["總計"].sum().reset_index()

fig = px.line(
    agg, x="學年度", y="總計", markers=True,
    title="台灣大專校院總學生數 — 105–113 學年度",
    labels={"學年度": "Academic year", "總計": "Total students"},
    color_discrete_sequence=["#3b82f6"],
)
fig.add_annotation(
    x=agg["學年度"].iloc[0], y=agg["總計"].iloc[0],
    text="少子化骨牌效應起點",
    showarrow=True, arrowhead=2,
    bgcolor="rgba(255,255,255,0.9)", bordercolor="orange",
)
```

這張圖是典型的 **policy-relevant storytelling**：用 annotation 告訴讀者 "為什麼這個下降趨勢值得擔憂"，而不是只給數字。

### 3.3.2 Stacked Bar — 公私立差異

```python
import plotly.express as px

agg = df.groupby(["學年度", "sector"])["總計"].sum().reset_index()
fig = px.bar(
    agg, x="學年度", y="總計", color="sector", barmode="stack",
    title="公立 vs. 私立 大專學生數變化",
    color_discrete_map={"公立": "#1d4ed8", "私立": "#f97316"},
)
```

**讀圖練習**：私立大專學生減幅是否比公立更陡？這對「少子化首先衝擊私校」這個直覺有沒有支持？

### 3.3.3 Horizontal Bar — 縣市分布 (latest year)

```python
import plotly.express as px

latest = df[df["學年度"] == df["學年度"].max()]
agg = (latest.groupby("city_name")["總計"].sum()
              .sort_values(ascending=False)
              .reset_index().head(15))

fig = px.bar(
    agg, x="總計", y="city_name", orientation="h",
    color="總計", color_continuous_scale="Tealgrn",
    title=f"{df['學年度'].max()} 學年度各縣市大專學生數 (Top 15)",
)
fig.update_layout(yaxis={"categoryorder": "total ascending"},
                  coloraxis_showscale=False)
```

### 🔬 Hands-on Practice 6: 跨年度 city ranking 變化

**任務**：選一個縣市（例如臺北市），畫出該縣市在 105–113 學年度的學生數變化（line chart）。哪個縣市跌幅最大？哪個逆勢成長？

<details>
<summary>💡 提示</summary>

```python
city = "臺北市"
sub = df[df["city_name"] == city].groupby("學年度")["總計"].sum().reset_index()
px.line(sub, x="學年度", y="總計", title=f"{city} 大專學生數變化").show()
```

可進一步用 `for city in df["city_name"].unique(): ...` 找出跌幅 vs. 成長的縣市。
</details>

<details>
<summary>✅ 參考解答</summary>

```python
import plotly.express as px

city = "臺北市"
sub = (df[df["city_name"] == city]
       .groupby("學年度")["總計"].sum()
       .reset_index())

fig = px.line(
    sub,
    x="學年度",
    y="總計",
    markers=True,
    title=f"{city} 大專學生數變化",
)
fig.show()

city_change = (df.groupby(["city_name", "學年度"])["總計"].sum()
                 .reset_index())
wide = city_change.pivot(index="city_name", columns="學年度", values="總計")
first_year = wide.columns.min()
last_year = wide.columns.max()
wide["change"] = wide[last_year] - wide[first_year]
wide["pct_change"] = wide["change"] / wide[first_year] * 100

print("跌幅最大")
print(wide.sort_values("pct_change").head(5)[["change", "pct_change"]])

print("\n成長最多")
print(wide.sort_values("pct_change", ascending=False).head(5)[["change", "pct_change"]])
```
</details>

---

# Part 4 — Data Storytelling 五原則

| 原則 | 意思 | 本週兩個 dataset 對應的例子 |
|------|------|----------------------------|
| **One message per chart** | 每張圖回答一個問題 | Section 2.3.1 只回答「哪些 subject 最多」，不是同時塞作者/機構 |
| **Context before detail** | 先大局再細節 | Section 3.3.1 先看總量下降，再 3.3.2 拆公私立 |
| **Label what matters** | 用 annotation 標重點 | 兩個 dataset 各有一個 annotation 例（peak、少子化起點） |
| **Show uncertainty** | 不確定性也是訊號 | scatter 用 `opacity=0.6` 暗示樣本密度；可進一步加 error band |
| **Earn the complexity** | 只在必要時用複雜圖 | 沒用 3D scatter 也沒用 choropleth 是有意識的 — 城市 bar 比地圖更清楚 |

---

# Part 5 — Altair 簡介 (Optional, 5 min)

Altair 是宣告式 (declarative) 的圖表 library，語法非常簡潔，適合喜歡 **grammar of graphics** (ggplot 風格) 的人。本課程不強迫使用，但 final project 可選擇。

```python
import altair as alt

chart = (
    alt.Chart(df.head(500))
       .mark_circle()
       .encode(
           x=alt.X("n_tags:Q", title="Number of tags"),
           y=alt.Y("title_len:Q", title="Title length (chars)"),
           color=alt.Color("primary_subject:N", legend=None),
           tooltip=["title:N", "date_published:T", "primary_subject:N"],
       )
       .properties(title="PsyArXiv (Altair version)", width=700, height=350)
       .interactive()
)
st.altair_chart(chart, use_container_width=True)
```

`:Q`, `:N`, `:T` 後綴是 Altair 的 field type — quantitative、nominal、temporal。

---

## Recap (重點回顧)

- ✅ 同一條 pipeline (`load → clean → describe → analyse → plot`) 對「API 取回的 JSON」與「政府公開 CSV」都通用，差別只在 load 那一段。
- ✅ Pagination 是抓取大型 API 資料的標準技巧；`time.sleep` + `raise_for_status` 是兩個基本紀律。
- ✅ `pd.concat(ignore_index=True, sort=False)` 處理跨年度 / 跨來源的 schema 對齊問題。
- ✅ 每個 cleaning 動作都要有 **觀察 → 動作 → 代價** 的紀錄，這在政策議題（少子化）的可信度上更重要。
- ✅ Plotly Express 一行程式對應一張互動圖；annotation 是 storytelling 的高 ROI 操作。

## Common Pitfalls

- ❌ **抓 API 沒做 pagination** → 只拿到第一頁 100 筆，誤以為 "OSF 只有 100 篇心理學論文"。
- ❌ **直接 `pd.concat` 不檢查欄位差異** → 看起來合併成功但某些欄位全 NaN 沒人發現。
- ❌ **`pd.to_numeric` 不加 `errors="coerce"`** → 遇到一個髒字串整支 script 炸掉。
- ❌ **Plotly 圖塞滿 200 種 subject 顏色** → 圖完全沒有訊息量；課程中我們刻意 `showlegend=False`。
- ❌ **Annotation 只寫值不寫意義** → "Peak: 87" 不如 "Peak coincides with conference deadline"。

---

## Homework — 將兩個 dataset 整合進你的 Streamlit dashboard

延續 Week 11/12 的 dashboard，本週作業要求：

1. **新增一個 page / tab**，使用 `osf_psyarxiv_pipeline.py` 中的 `fetch_psyarxiv() + clean()` 函式（包成 `@st.cache_data`），呈現至少 **2 張 Plotly 圖**。
2. **再新增一個 page / tab**，使用 `moe_higher_ed_pipeline.py` 的 `fetch_all() + clean()`，呈現至少 **2 張 Plotly 圖**。其中至少一張須包含 **annotation**。
3. 兩個 dataset 各加一個 Streamlit widget（`st.selectbox`, `st.slider`, `st.multiselect` 擇一），讓使用者能 filter (e.g., 選擇學年度範圍、選擇 subject)。
4. 在每張圖下方用 `st.caption()` 寫 1–2 句 **takeaway sentence**（不是 "this is a bar chart of X"，而是 "私立學生數自 109 年起加速下滑"）。
5. 在程式碼最上方寫一段 docstring 簡述：哪個 cleaning 決定你刻意 **與我提供的版本不同**？理由是什麼？

繳交：GitHub repo URL + Streamlit Cloud URL，截止時間：Week 14 上課前。

**Rubric (簡)**：

| 面向 | 比重 |
|------|------|
| Pipeline 完整 (load → clean → describe → plot) | 30% |
| Plotly 圖數量與多樣性 (≥ 4 張，含 annotation) | 25% |
| Storytelling — caption + annotation 是否 earn the complexity | 20% |
| Cleaning decision 的反思（與範例不同處 + 理由） | 15% |
| Streamlit interactivity (widget + responsive layout) | 10% |

---

## Resources

- **Plotly**
  - [Plotly Express documentation](https://plotly.com/python/plotly-express/)
  - [Streamlit `st.plotly_chart` reference](https://docs.streamlit.io/develop/api-reference/charts/st.plotly_chart)
- **OSF / PsyArXiv API**
  - [OSF API v2 documentation](https://developer.osf.io/)
  - [PsyArXiv preprint server](https://psyarxiv.com/)
- **教育部統計處 Open Data**
  - [教育部統計處主站](https://stats.moe.gov.tw/)
  - [大專校院校別學生數 (年度 CSV)](https://stats.moe.gov.tw/files/detail/113/113_student.csv)
- **Data Storytelling**
  - [Fundamentals of Data Visualization — Wilke (open access)](https://clauswilke.com/dataviz/)
  - [Storytelling with Data — Cole Nussbaumer Knaflic](http://www.storytellingwithdata.com/)
- **Altair (optional)**
  - [Altair documentation](https://altair-viz.github.io/)

---

## What Comes Next

| Week | Topic |
|------|-------|
| 14 | Anthropic SDK — 讓 dashboard 用 Claude 自動為圖表寫 caption |
| 15 | Final project workshop — peer code review |
| 16 | **Final milestone:** Live app presentation & symposium |

---

*最後更新：2026-05-13*
