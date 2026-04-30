# CLAUDE.md — 課程教材撰寫指南

> **課程**：NS5116 電腦硬體與程式語言在行為科學實驗與大數據分析之應用
> **學期**：2026 Spring | **授課教師**：張智宏 (Erik Chang)
> **本文件目的**：指引 Claude 協助產生本課程的講義、範例程式碼、習題、與投影片。

---

## 1. 受眾 (Audience)

教材的讀者是 **行為與社會科學領域的研究生**，具備以下背景：

- 具備基本電腦操作能力（檔案管理、安裝軟體、瀏覽器使用）。
- 對 Python 有 **入門級** 的理解（曾接觸過變數、迴圈、函式），但 **非資訊科學背景**。
- 具備認知心理學、神經科學、或行為科學的領域知識。
- 對統計、實驗設計、reaction time、accuracy 等概念熟悉。
- **不熟悉**：物件導向設計模式、軟體工程術語（如 dependency injection、polymorphism）、進階資料結構（heap、graph）、底層硬體架構。

撰寫教材時請以「能夠獨立完成研究分析任務」為目標，而非「成為軟體工程師」。

---

## 2. 寫作風格 (Writing Style)

### 2.1 語言原則

- **主要敘述使用繁體中文**（台灣慣用語），讓非英文母語的學生能無障礙閱讀。
- **技術術語保留英文原文**，並在第一次出現時附上中文簡要說明。例如：
  - ✅ 「使用 `numpy.array` 建立一個 array (陣列)，它與 Python 的 list (串列) 不同⋯⋯」
  - ❌ 「使用陣列建立一個陣列，它與 Python 的串列不同⋯⋯」
- **程式碼註解可以混用中英文**：簡短的概念用英文（`# vectorized`），需要解釋的用中文。
- **檔名、函式名、變數名一律使用英文**（例如 `plot_rt_distribution.py`，不要寫 `繪製反應時間分布.py`）。

### 2.2 常見保留英文的術語

`array`, `list`, `dict`, `tuple`, `dataframe`, `index`, `slicing`, `vectorization`, `broadcasting`,
`function`, `class`, `method`, `attribute`, `module`, `package`, `import`,
`for loop`, `if statement`, `condition`, `iteration`,
`reaction time (RT)`, `accuracy`, `trial`, `block`, `condition`, `factor`,
`stimulus / stimuli`, `fixation`, `Gabor patch`, `Stroop effect`,
`API`, `endpoint`, `request`, `response`, `JSON`, `CSV`,
`commit`, `branch`, `merge`, `pull request`, `repository`,
`prompt`, `agent`, `MCP`, `vibe coding`,
`fMRI`, `EEG`, `BOLD signal`, `voxel`, `ROI`, `MVPA`, `RSA`。

### 2.3 語氣

- 直接、精準、避免冗詞。每句話都應該有資訊量。
- 假設學生會犯典型錯誤，主動提示：「**注意**：⋯⋯」、「**常見錯誤**：⋯⋯」。
- 鼓勵實驗：「**試試看**：把 `seed=42` 改成 `seed=0`，觀察結果如何變化。」
- 避免「很簡單」、「顯而易見」這類用詞 — 對非資訊背景學生並不簡單。

---

## 3. 內容結構 (Content Structure)

每一份教材（週次講義、補充章節、homework）都應包含以下區塊：

### 3.1 標準週次結構

```markdown
# Week NN: 主題 (English Title)

> **Course / Week / Date**

## Learning Objectives (學習目標)
- 條列 5–8 個動詞開頭的可驗證目標（建立 / 計算 / 解讀 / 部署 ⋯⋯）

## Why This Matters (動機)
- 用一個 **認知神經科學的真實情境** 開場（見 §4 範例庫）。

## In-Class Topics (課堂內容)
### 1. 概念名稱 (時間估計)
- 簡要說明
- 程式碼範例（必須可執行）
- **Hands-on Practice**：學生立即動手練習的小題目（5–15 分鐘）

### 2. ⋯⋯

## Recap & Common Pitfalls (重點回顧與常見錯誤)

## Homework (作業)
- 明確的繳交格式（.ipynb / .py / .md）
- Rubric (評分標準) 摘要
```

### 3.2 程式碼範例規則

- **每個程式碼區塊都要能直接複製貼上執行**，不要有 `# ...` 省略。
- 第一行寫 `import` 區塊；不要假設前面已經 import 過。
- 使用 `np.random.seed(42)` 確保 reproducibility。
- 範例資料優先使用 **小規模、可在 1 秒內跑完** 的合成資料。
- 標註檔案位置（如果該範例在 repo 中有對應檔案）：

```markdown
*📄 [`code/numpy/rt_distribution.py`](code/numpy/rt_distribution.py)*
```python
import numpy as np
# ...
```
```

### 3.3 Hands-on Practice 規則

每個概念講解後，**必須** 緊接著一個動手練習。練習應符合：

1. **任務明確**：清楚說明 input 與預期 output。
2. **可在 5–15 分鐘內完成**（課堂節奏）。
3. **基於剛剛講解的範例修改**，不引入新概念。
4. **附上預期答案**（折疊區塊或下一節揭曉），讓學生可自我檢查。
5. **與認知神經科學情境連結**（見 §4）。

範例格式：

```markdown
### 🔬 Hands-on Practice 1: 計算每個 condition 的平均 RT

**情境**：你剛跑完一個 Stroop 實驗，拿到 60 個 trial 的 RT 與 condition label。

**任務**：給定下列資料，計算 `congruent` 與 `incongruent` 兩個條件下的平均 RT 與標準差。

```python
import numpy as np
np.random.seed(42)
rts = np.concatenate([
    np.random.normal(450, 60, 30),  # congruent
    np.random.normal(520, 80, 30),  # incongruent
])
conditions = np.array(['congruent']*30 + ['incongruent']*30)
# 你的程式碼從這裡開始
```

<details>
<summary>💡 提示</summary>
使用 boolean masking：`rts[conditions == 'congruent']`。
</details>

<details>
<summary>✅ 參考解答</summary>
```python
for cond in ['congruent', 'incongruent']:
    mask = conditions == cond
    print(f"{cond}: M={rts[mask].mean():.1f}, SD={rts[mask].std():.1f}")
```
</details>
```

---

## 4. 認知神經科學範例庫 (CogNeuro Example Bank)

**所有教材中的範例與練習，請優先採用以下情境**，避免使用「電商銷售額」、「股票價格」這類與本課程脈絡無關的例子。

### 4.1 行為實驗資料 (Behavioral Data)

| 概念 | 範例情境 |
|------|----------|
| List, dict, CSV I/O | 讀取 PsychoPy 輸出的 trial-by-trial CSV |
| For loop / 條件判斷 | 計算每個 trial 的正確率、剔除 RT < 200ms 的 outlier |
| Function | 寫一個 `compute_dprime(hits, false_alarms)` 函式 |
| NumPy array | RT array 的 vectorized outlier rejection（mean ± 3 SD）|
| Pandas DataFrame | Stroop / Flanker / N-back 資料的 group-by analysis |
| Matplotlib | RT distribution histogram、condition × accuracy bar plot |
| Seaborn | Violin plot 比較 young vs. old adults 的 RT 分布 |
| Statistics | Paired t-test 檢驗 Stroop effect、correlation 分析 |

### 4.2 神經影像 / 訊號 (Neuroimaging & Signals)

| 概念 | 範例情境 |
|------|----------|
| 2D / 3D array | 模擬 voxel × time 的 BOLD signal matrix |
| Array slicing | 從 4D fMRI volume 抽取 ROI time series |
| Broadcasting | 對每個 voxel 做 baseline correction |
| Convolution | HRF (hemodynamic response function) 與 stimulus onsets 的 convolution |
| FFT | EEG signal 的 power spectrum 計算 |
| Correlation matrix | RSA (Representational Similarity Analysis) 的 condition × condition matrix |

### 4.3 大數據 / API (Open Data & API)

| 概念 | 範例情境 |
|------|----------|
| API request | 從 [PubMed E-utilities](https://www.ncbi.nlm.nih.gov/books/NBK25500/) 抓取認知老化相關文獻 |
| JSON parsing | 解析 OpenNeuro dataset metadata |
| Web scraping | 從 [Neurosynth](https://neurosynth.org) 取得 ROI 對應的認知功能 |
| Streamlit dashboard | 視覺化 [data.gov.tw](https://data.gov.tw) 的長者健康資料 |
| Interactive plot | Plotly 互動式呈現 brain region × cognitive function 的關係 |

### 4.4 推薦合成資料生成函式

優先使用合成資料（synthetic data）以避免依賴外部下載。標準範本：

```python
import numpy as np
np.random.seed(42)

def simulate_stroop(n_trials_per_cond=30, congruent_rt=(450, 60), incongruent_rt=(520, 80)):
    """生成 Stroop task 的模擬 RT 資料。

    Returns
    -------
    rts : np.ndarray, shape (2 * n_trials_per_cond,)
    conditions : np.ndarray of str
    """
    rts = np.concatenate([
        np.random.normal(*congruent_rt, n_trials_per_cond),
        np.random.normal(*incongruent_rt, n_trials_per_cond),
    ])
    conditions = np.array(['congruent'] * n_trials_per_cond +
                          ['incongruent'] * n_trials_per_cond)
    return rts, conditions
```

---

## 5. 課程結構脈絡 (Course Context)

撰寫某一週的教材時，**必須了解前後週的銜接**，不要重複教過的概念，也不要使用尚未教過的工具。

### 5.1 兩階段架構

| 階段 | 週次 | 主題 | 核心工具 |
|------|------|------|----------|
| **Part 1: Manual Python** | 1–8 | 從零建立程式邏輯，部署線上實驗 | Anaconda, VS Code, Jupyter, NumPy, Matplotlib, **PsychoPy**, **Pavlovia** |
| **Part 2: Vibe Coding & Agentic** | 9–16 | 用 AI 工具建構資料應用 | **Claude Code**, GitHub, **Streamlit**, pandas, requests, Plotly, **Anthropic SDK** |

### 5.2 各週可使用的工具集（依時間累積）

撰寫第 N 週教材時，請只使用 ≤ N 週已介紹的工具：

- **Week 1–2**：Python 基礎語法、`print`、變數、type、operator、`if/else`、`for/while`。
- **Week 3**：函式、`list`、`dict`、`tuple`、`set`、檔案 I/O (`open`, `csv`)。
- **Week 4–6**：PsychoPy（`visual.Window`, `TextStim`, `event.waitKeys`）、Builder GUI、Pavlovia。
- **Week 7**：NumPy、Matplotlib（之後可自由使用）。
- **Week 8**：Midterm — 不引入新工具。
- **Week 9**：Claude Code CLI、prompt engineering 基礎。
- **Week 10**：git、GitHub、GitHub Actions。
- **Week 11**：Streamlit。
- **Week 12**：requests、pandas、open data API。
- **Week 13**：Plotly、Altair。
- **Week 14**：Anthropic SDK。
- **Week 15–16**：Final project — 不引入新工具。

### 5.3 Pandas 的特殊位置

雖然 pandas 在 Week 5 的 syllabus 中有提到（用於 trial data 的 groupby），但對非資訊背景學生 **DataFrame 的概念較抽象**。在 Part 1 中：

- 優先使用 NumPy + dict 處理小規模資料。
- pandas 僅在「需要 groupby 或 csv 一鍵讀取」時引入，不展開教學。
- **pandas 的完整教學集中在 Week 12**（API 取回的資料清理）。

---

## 6. 檔案組織 (File Organization)

### 6.1 Repository 結構

```
2026_Spring_CompBigData/
├── CLAUDE.md                        ← 本檔案
├── README.md                        ← 課程簡介
├── syllabus_ai_main.tex / .pdf      ← 完整 syllabus
├── sections/                        ← syllabus 的各 section
├── general/                         ← 共用資源（環境設定、final project 範例）
├── week-NN-topic_name/
│   ├── week-NN-topic.md             ← 主講義（Markdown）
│   ├── week-NN-topic.pptx           ← 投影片
│   ├── week-NN-puzzles.ipynb        ← 課堂練習 notebook
│   ├── week-NN-homework.md          ← 作業說明
│   ├── lpthw_exNN-NN.ipynb          ← 笨方法學 Python 對應章節
│   └── code/                        ← 程式碼範例（按主題分子資料夾）
│       └── numpy/
│           ├── creating_arrays.py
│           └── ...
├── homeworks/                       ← 學生作業與評分（見該資料夾的 CLAUDE.md）
└── materials/                       ← 外部教材（如 handson-ml3）
```

### 6.2 命名規則

- 週次資料夾：`week-NN-snake_case_topic`（NN 為兩位數）。
- Markdown 講義：`week-NN-topic.md`（與資料夾名一致）。
- 程式碼範例：`snake_case.py`，名稱即用途（`compute_dprime.py` 而非 `code1.py`）。
- 不要在檔名中使用空格或中文字元。

---

## 7. 與其他 CLAUDE.md 的關係

- **本檔案 (`/CLAUDE.md`)**：教材撰寫指南。
- **`homeworks/CLAUDE.md`**：作業下載、批改、上傳到 eeclass 的自動化流程（**不要**與本檔案混淆，那份檔案只用於 grading workflow）。

當任務涉及「produce / write / generate / 撰寫」教材時，請參考本檔案。
當任務涉及「grade / download submission / upload to eeclass」時，請參考 `homeworks/CLAUDE.md`。

---

## 8. 品質檢查清單 (Pre-delivery Checklist)

產出教材前，請自我檢查：

- [ ] 主敘述為繁體中文，技術術語保留英文。
- [ ] 每個概念都有 **可執行的範例程式碼**（含 import）。
- [ ] 每個概念後都有 **hands-on practice**，並附參考解答。
- [ ] 所有範例情境都來自 **認知神經科學脈絡**（行為實驗 / 神經影像 / 開放資料）。
- [ ] 沒有使用尚未在課程中介紹的工具（見 §5.2）。
- [ ] 程式碼使用 `np.random.seed()` 確保 reproducibility。
- [ ] 標註了學習目標、時間估計、與 common pitfalls。
- [ ] 檔案命名遵守 §6.2。

---

## 9. 一個完整的小範例

當被要求寫一段「教 NumPy boolean masking」的教材時，預期輸出格式：

````markdown
### 4. Boolean Masking — 篩選符合條件的 trial (15 min)

**為什麼重要**：在分析行為資料時，最常見的需求是 *「只保留正確 trial」* 或 *「剔除過快/過慢的 RT」*。Boolean masking 是 NumPy 中最快、最 Pythonic 的做法。

*📄 [`code/numpy/boolean_masking.py`](code/numpy/boolean_masking.py)*
```python
import numpy as np
np.random.seed(42)

# 模擬 50 個 trial 的 RT 與 accuracy
rts = np.random.normal(500, 100, 50)        # ms
accuracy = np.random.binomial(1, 0.85, 50)  # 0 or 1

# 建立 boolean mask
correct_mask = accuracy == 1
fast_enough_mask = rts > 200

# 結合多個條件 — 注意要用 & 而不是 and
clean_mask = correct_mask & fast_enough_mask
clean_rts = rts[clean_mask]

print(f"Original: {len(rts)} trials, M={rts.mean():.1f}ms")
print(f"Clean:    {len(clean_rts)} trials, M={clean_rts.mean():.1f}ms")
```

**常見錯誤**：
- ❌ `correct_mask and fast_enough_mask` → `ValueError: truth value of an array is ambiguous`
- ✅ `correct_mask & fast_enough_mask`（element-wise 邏輯運算用 `&`、`|`、`~`）

#### 🔬 Hands-on Practice 4: 剔除 outlier RT

**任務**：用 mean ± 3 SD 規則剔除 outlier，回報剔除前後的 trial 數與 mean RT。

```python
import numpy as np
np.random.seed(0)
rts = np.concatenate([
    np.random.normal(500, 80, 95),
    np.array([1500, 1800, 100, 80, 2000])  # 故意加入 outlier
])
# 你的程式碼從這裡開始
```

<details>
<summary>✅ 參考解答</summary>
```python
m, s = rts.mean(), rts.std()
mask = (rts > m - 3*s) & (rts < m + 3*s)
print(f"Before: n={len(rts)}, M={rts.mean():.1f}")
print(f"After:  n={mask.sum()}, M={rts[mask].mean():.1f}")
```
</details>
````

---

*最後更新：2026-04-29*
