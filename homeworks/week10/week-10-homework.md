# Week 10 Homework: Agentic Workflows × GitHub — 從 Prompt 到 Live Demo

> **Course:** NS5116 電腦硬體與程式語言在行為科學實驗與大數據分析之應用 — Spring 2026
> **Due:** Before Week 11 (2026-05-07) | **Submit via:** eeclass

---

## Overview

本週課堂上你完成了 `tw-airquality-mini` 的範例練習，走過完整 SOP：venv → git → Claude Code scaffold → push → GitHub Pages。

這份作業的目標是把 SOP 內化為你自己的工作流程，並進一步思考 **三件對研究人員特別重要的事**：

1. **Prompt style matters.** 同一個任務，用不同方式叫 Claude 做，得到的程式碼品質會差很多。學會比較與選擇。
2. **README 是專案的對外名片。** 三個月後的你、實驗室同事、PI、審稿人，都會先看 README。
3. **`docs/index.html` 是你的成果頁。** 它應該清楚回答：你的 *目標* 是什麼？*過程* 怎麼做？*結果* 是什麼？

本作業使用一個真實的開放心理測驗資料集，讓你完整經歷一次「拿到資料 → 探索 → 公開發布」的迷你研究流程。

---

## Dataset: Open-Source Psychometrics Project

你將使用 [Open-Source Psychometrics Project](https://openpsychometrics.org/_rawdata/) 提供的開放資料集。這是研究界廣泛使用的心理測驗資料來源（已被 25+ 篇 peer-reviewed 論文引用）。

### 預設資料集（推薦）：Big Five Personality Test

- **Download:** [https://openpsychometrics.org/_rawdata/BIG5.zip](https://openpsychometrics.org/_rawdata/BIG5.zip)
- **n = 19,719** participants
- **Variables:** 50 個 IPIP Big Five 題項（Likert 1–5）+ gender, age, race, native language, country
- **Codebook:** zip 檔內附 `codebook.txt`
- **資料量:** ~3 MB unzip 後，CSV 可直接 push 到 GitHub（單檔 < 100 MB）

### 替代資料集（任選其一即可）

如果你的研究興趣偏向情緒/臨床心理或認知能力，可改用：

| Dataset                                 | n      | Theme           | Download                                                                                 |
| --------------------------------------- | ------ | --------------- | ---------------------------------------------------------------------------------------- |
| DASS (Depression Anxiety Stress Scales) | 39,775 | 情緒/精神症狀   | [`DASS_data_21.02.19.zip`](https://openpsychometrics.org/_rawdata/DASS_data_21.02.19.zip) |
| HEXACO Personality                      | 22,786 | 六因子人格      | [`HEXACO.zip`](https://openpsychometrics.org/_rawdata/HEXACO.zip)                         |
| Vocabulary IQ Test                      | 12,173 | 詞彙能力 + 人格 | [`VIQT_data.zip`](https://openpsychometrics.org/_rawdata/VIQT_data.zip)                   |
| Multifactor General Knowledge Test      | 19,218 | 通識知識能力    | [`MGKT_data.zip`](https://openpsychometrics.org/_rawdata/MGKT_data.zip)                   |

> **注意：** 這些 CSV 多以 tab 分隔（`sep="\t"`），不是逗號。第一次讀檔時要留意。
>
> **倫理提醒：** 雖然資料已匿名，但 DASS 等臨床量表涉及敏感主題。在 README/Pages 撰寫時請避免做出對個人或群體的污名化推論，僅描述 *資料中的統計關係*。

---

## 題目一：Project Bootstrap 與 Claude Prompt Style 比較 (30 pts)

> **Learning goal:** 體會「給 Claude 不同風格的指令」對產出品質的影響，並學會選擇適當的風格。

### 1.1 從零建立新專案 (5 pts)

依照 Week 10 SOP 建立一個 **新的 GitHub repo**（不要重用 `tw-airquality-mini`）。命名建議：`big5-mini-explorer`、`dass-mini-explorer` 等，視你選的資料集而定。

- Step 1–3 手動完成：mkdir、venv、git init、`.gitignore`、第一次 commit。
- 在 README 第一行先寫一句話描述（後面再修）。
- 把資料集下載解壓到 `data/raw/`（**注意：raw 資料不入 git**，請在 `.gitignore` 排除 `data/raw/*.csv`）。

### 1.2 三種 Prompt Style 對照（核心練習，20 pts）

針對 **同一個任務**：「載入資料集，產出一張顯示 *年齡分布* 的直方圖，並儲存為 `reports/age_distribution.png`」，分別用以下三種 prompt 風格給 Claude Code 寫程式碼：

#### Style A — One-liner（一句話風格）

```
> 幫我畫一張資料的年齡分布圖。
```

把產生的程式碼存為 `notebooks/style_a_oneliner.ipynb`。

#### Style B — Specification（規格化風格）

```
> Read data/raw/data.csv (tab-separated). Filter rows where 13 <= age <= 80
  to remove implausible entries. Plot a histogram of age with 30 bins,
  using matplotlib. Set xlabel="Age (years)", ylabel="Count",
  title with the dataset name and n. Save as reports/age_distribution.png
  at dpi=150. Print to stdout: total rows loaded, rows kept after filter,
  and the path of the saved figure.
```

把產生的程式碼存為 `notebooks/style_b_specification.ipynb`。

#### Style C — Plan-first / Agentic（先計畫再執行）

```
> I want to produce reports/age_distribution.png from data/raw/data.csv.
  Before writing code:
  1. List the steps you plan to take (load → inspect dtype → filter → plot → save).
  2. List 3 things that could go wrong (encoding, separator, missing values).
  3. Then write the code, with comments explaining each defensive step.
  Confirm the plan with me before producing the final code.
```

把產生的程式碼存為 `notebooks/style_c_planfirst.ipynb`。

### 1.3 Reflection Table（5 pts）

在 README.md 的 `## Prompt Style Comparison` 區塊，填寫下表（不需多長，每格 1–3 句即可）：

| Style            | 產出能直接跑嗎？ | 程式碼可讀性 | 防呆程度（處理 edge case） | 你下次會選哪個？為什麼？ |
| ---------------- | ---------------- | ------------ | -------------------------- | ------------------------ |
| A. One-liner     |                  |              |                            |                          |
| B. Specification |                  |              |                            |                          |
| C. Plan-first    |                  |              |                            |                          |

> **提示：** 沒有「絕對最好」的答案。簡單探索任務 one-liner 可能更快，正式分析則 specification 或 plan-first 更穩。寫出 **你的判準** 比挑出贏家重要。

---

## 題目二：Mini Analysis Pipeline (25 pts)

> **Learning goal:** 練習把分析寫成 **可重複執行** 的程式，而不是一次性的 notebook 探索。

選你 1.2 中產出的 **最佳版本**（通常是 Style B 或 C）作為起點，擴充成下列分析：

### 2.1 資料清理（5 pts）

寫一個 `src/load_data.py` 模組，提供函式 `load_clean_data(path: str) -> pd.DataFrame`。要求：

- 讀取 tab-separated CSV。
- 過濾 `age` 在合理範圍（依資料集調整，例如 13–80）。
- 過濾 `gender` 為 0（unstated）的列（Big Five 資料集的編碼）。
- 印出清理摘要：原始 n、清理後 n、流失百分比。

### 2.2 兩個分析圖表（15 pts）

在 `notebooks/01_explore.ipynb` 中產出兩張圖，並儲存到 `reports/`：

**Figure 1 — 描述性 (descriptive):** 你選的資料集中**任一主要變項**的分布或 cross-tab。例如：

- Big Five → 五個分數的小提琴圖 (violin plot)，比較性別差異。
- DASS → Depression / Anxiety / Stress 三個分數的散布圖矩陣。
- HEXACO → 六因子的 correlation heatmap。

**Figure 2 — 關係 (relational):** 一個變項與另一個變項的關係。例如：

- Big Five → Extraversion 分數隨年齡的趨勢（用 binned mean ± SEM）。
- DASS → Depression 分數的國家差異（取前 10 大國家）。
- 自由發揮，但要有意義的研究問題。

每張圖都要有 **標題、軸標籤、圖例**，且能從圖看出主要結論。

### 2.3 把分析包成可重複執行 (5 pts)

讓你的 repo 滿足：

```bash
git clone <your-repo-url>
cd <repo-name>
python -m venv .venv && source .venv/bin/activate  # or .venv\Scripts\activate
pip install -r requirements.txt
# 把資料下載解壓到 data/raw/
jupyter notebook notebooks/01_explore.ipynb
```

任何人照做都能產生你 reports/ 中的圖。

> **提示：** 因為 raw 資料不入 git，README 必須清楚指示資料下載步驟（URL + 解壓位置）。

---

## 題目三：README.md — 寫一張好名片 (20 pts)

> **Learning goal:** README 不是檔名清單，而是 **30 秒內讓讀者知道值不值得繼續看** 的廣告文案。

你的 `README.md` 必須包含以下區塊（按順序）：

1. **Title + Tagline** — 一句話說明這是什麼專案。
2. **Live Demo** — 連到你 GitHub Pages URL（題目四）。
3. **Screenshot / 主要圖表** — `reports/` 中最有代表性的那張圖直接內嵌進來（用 `![alt](reports/figure_name.png)`）。
4. **Motivation / 一段話** — 你為什麼選這個資料集？要回答什麼問題？
5. **How to run** — clone → venv → pip install → 下載資料 → 執行 notebook，每一步都是可複製的 shell 指令。
6. **Project structure** — 樹狀列出 `data/`、`notebooks/`、`src/`、`reports/`、`docs/` 各自的用途。
7. **Prompt Style Comparison** — 題目一的 reflection table。
8. **Data source & License** — 引用 Open-Source Psychometrics Project 的 URL；如果你選的是 Big Five，加上 codebook 中的引用聲明。
9. **Author** — 姓名 + 學號 + 一行身分（e.g., NCU 認知神經科學研究所碩二）。

### Rubric for README

| 項目                                   | Pts | 觀察點                      |
| -------------------------------------- | --- | --------------------------- |
| 第一段廣告文案是否清楚                 | 4   | 滑過的人 5 秒內知道這是什麼 |
| Live Demo 連結是否能打開               | 3   | 連到題目四的 Pages          |
| 主要圖表是否內嵌                       | 3   | 不是文字描述，是真的圖片    |
| How to run 是否完全可複製              | 5   | 助教實際照做能不能跑起來    |
| Prompt Style Comparison 表格的洞察品質 | 5   | 不是堆形容詞，要有具體判準  |

> **常見錯誤：**
>
> - ❌ README 只列檔名，沒有說明專案做什麼。
> - ❌ How to run 缺步驟（例如忘了講要先下載資料）。
> - ❌ 圖表用「請看 reports 資料夾」帶過 — 應該直接內嵌。

---

## 題目四：docs/index.html — 把成果做成一頁 Live Demo (20 pts)

> **Learning goal:** 一份分析的價值，最後展現於 **非技術讀者也看得懂** 的成果頁。

啟用 GitHub Pages（Settings → Pages → Source: `Deploy from a branch`, Branch: `main`, Folder: `/docs`），並讓 `https://<username>.github.io/<repo>/` 顯示一個結構清楚的成果頁。

### `docs/index.html` 必須包含 (按順序)

1. **Title + 一句話 Tagline**（與 README 一致）。
2. **Goal / 目標** — 一段 1–3 句的研究問題敘述：「我用這份資料想回答什麼？」
3. **Procedure / 過程** — 條列 4–6 個關鍵步驟（資料來源、清理規則、分析方法、視覺化選擇）。不要貼 code，要寫成讀者看得懂的句子。
4. **Outcome / 結果** — 兩張圖嵌入（從 `reports/` 複製到 `docs/` 內，路徑要相對於 `docs/`），每張圖配 1–2 句結論。
5. **Caveats / 侷限** — 至少 2 點：取樣偏誤、心理測驗自陳資料的限制、推論範圍等。
6. **Repo link / GitHub** — 連回 repo 首頁。
7. **Author + Date**。

### 兩種寫法擇一

**A. 自己手寫 HTML** — 適合想練習 web 基礎的人。

**B. 用 Claude Code 生成** — 在你的 prompt 中明確指定 *結構*（上述 7 個區塊）、*風格*（minimal、可讀、字體大小）、*顏色*（最多 2–3 色）。把這個 prompt 也存進 `notebooks/landing_prompt.md`，作為作業繳交的一部分（讓助教看你怎麼指揮 Claude）。

### 不允許

- ❌ 直接把 notebook nbconvert 成 HTML 當 index.html — 那是分析過程，不是成果頁。可以另外放成 `docs/notebook.html` 並從 index.html 連過去。
- ❌ 預設黑底深灰字、字體 < 14px、圖片寬度溢出視窗等對讀者不友善的設計。

### Rubric for docs/index.html

| 項目                                  | Pts | 觀察點             |
| ------------------------------------- | --- | ------------------ |
| 七個必要區塊都齊全                    | 7   | 缺一扣 1 分        |
| Goal / Procedure / Outcome 是否說人話 | 5   | 非技術讀者能否看懂 |
| 圖片載入正確（不是 broken image）     | 4   | 路徑相對於 docs/   |
| Caveats 是否誠實                      | 2   | 有寫到資料限制     |
| 整體可讀性與美感                      | 2   | 字級、留白、配色   |

---

## 題目五：Reflection Note (5 pts)

在 repo 根目錄建立 `REFLECTION.md`，回答以下三個問題（每題 100–200 字）：

1. **Prompting reflection** — 在題目一三種風格中，你發現自己最容易卡的是什麼？例如「Style B 太囉唆，我打到一半就放棄」、「Style A 產出的程式碼看起來對但跑不出來」。
2. **README reflection** — 寫 README 時，哪個區塊最難寫？為什麼？
3. **Public artifact reflection** — 想像三個月後你要找實習，你會把這個 repo URL 放進履歷嗎？如果不會，缺什麼？

> 這題評分重點是 **誠實與具體**，不是答得漂亮。

---

## Deliverables / 繳交內容

不繳交檔案 — **只繳交兩個 URL**：

1. **Repo URL：** `https://github.com/<your-username>/<repo-name>`
2. **Pages URL：** `https://<your-username>.github.io/<repo-name>/`

> 助教會 clone 你的 repo、依 README 的 How to run 跑一次，並打開 Pages URL 檢查 live demo。

### 檔案結構參考

```
<your-repo-name>/
├── README.md
├── REFLECTION.md
├── requirements.txt
├── .gitignore
├── data/
│   └── raw/                  ← 不入 git
├── notebooks/
│   ├── style_a_oneliner.ipynb
│   ├── style_b_specification.ipynb
│   ├── style_c_planfirst.ipynb
│   ├── 01_explore.ipynb
│   └── landing_prompt.md     ← 若用 Claude 生成 docs/index.html
├── src/
│   ├── __init__.py
│   └── load_data.py
├── reports/
│   ├── age_distribution.png
│   ├── figure1_descriptive.png
│   └── figure2_relational.png
└── docs/
    ├── index.html
    ├── figure1_descriptive.png
    └── figure2_relational.png
```

---

## Grading Summary (100 pts)

| Section                                    | Pts           |
| ------------------------------------------ | ------------- |
| 題目一 — Project Bootstrap & Prompt Style | 30            |
| 題目二 — Mini Analysis Pipeline           | 25            |
| 題目三 — README.md                        | 20            |
| 題目四 — docs/index.html                  | 20            |
| 題目五 — Reflection Note                  | 5             |
| **Total**                            | **100** |

### Bonus (up to 10 pts)

- **(+5 pts) GitHub Actions CI** — 加一個 `.github/workflows/lint.yml`，在每次 push 時跑 `python -m py_compile src/*.py`，並在 README 加上 build status badge。
- **(+5 pts) Plotly 互動圖** — 在 `docs/index.html` 內嵌一張 Plotly 互動圖（hover 顯示細節），取代或補充 figure2。

---

## Tips / 提示

- **時間預估：** 認真做約 4–6 小時。Prompt 比較與 README/Pages 撰寫是大頭，分析本身可以很簡潔。
- **不要在最後一刻才 push。** GitHub Pages build 大約要 1–2 分鐘，等待會讓你壓力更大。
- **下載資料時遇到亂碼？** Open Psychometrics 的 CSV 有時是 `latin-1` 而非 `utf-8`，加 `pd.read_csv(path, sep="\t", encoding="latin-1")` 試試。
- **commit 訊息要寫好。** 助教會看你的 git log。`Initial commit`、`update`、`fix bug` 這類訊息會扣印象分。
- **README 寫不出來時**，把它丟給 Claude：「Here is my repo structure and notebooks. Draft a first version of README.md following this template: [貼模板]. Use my actual figure paths.」 然後 *你來編輯* — 不要原封不動 commit。

---

## Resources / 參考資料

- Open-Source Psychometrics Project：[https://openpsychometrics.org/_rawdata/](https://openpsychometrics.org/_rawdata/)
- GitHub Pages 官方文件：[https://docs.github.com/en/pages](https://docs.github.com/en/pages)
- Markdown 語法：[https://www.markdownguide.org/basic-syntax/](https://www.markdownguide.org/basic-syntax/)
- 「Awesome README」精選清單：[https://github.com/matiassingers/awesome-readme](https://github.com/matiassingers/awesome-readme)
- Claude Code Prompt Engineering Guide：[https://docs.claude.com/en/docs/build-with-claude/prompt-engineering/overview](https://docs.claude.com/en/docs/build-with-claude/prompt-engineering/overview)

---

*文件版本：2026-04-30 by Erik Chang，配合 Week 10 主教材使用。*
