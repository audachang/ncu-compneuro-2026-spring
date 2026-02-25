# Option 2 專案開發計畫  
## 🚗 道路交通事故風險視覺化與認知因素分析
### Traffic Accident Risk Visualization & Cognitive Factor Analysis

> **專案名稱**: SafeRoad Taiwan — 台灣交通安全互動儀表板  
> **技術堆疊**: Python · Streamlit · Plotly · pandas · Claude API  
> **資料來源**: [政府資料開放平臺 data.gov.tw](https://data.gov.tw/)  
> **部署平台**: Streamlit Cloud (免費)

---

## 1. 專案願景 Project Vision

台灣每年有超過 30 萬件交通事故，其中涉及多種人因 (human factors) 問題——注意力不集中、疲勞駕駛、年齡相關的認知衰退等。本專案利用政府開放的交通事故資料，建立一個互動式的 Streamlit Web App，讓使用者能夠自行探索數據中隱藏的**行為模式**，並利用 AI 將冰冷的統計數字轉化為有意義的**安全故事敘事**。

### 核心問題 Core Questions

| #   | 問題                                                 | 行為科學連結                 |
| --- | ---------------------------------------------------- | ---------------------------- |
| Q1  | 不同年齡層的事故率與嚴重程度有何差異？               | 老化與認知衰退、反應時間     |
| Q2  | 一天中哪些時段事故最集中？是否反映注意力的晝夜節律？ | 警覺性 (vigilance)、疲勞效應 |
| Q3  | 哪些車種與事故嚴重程度最相關？                       | 風險知覺 (risk perception)   |

---

## 2. 資料集清單 Data Inventory

### 2.1 主要資料集

| 資料集                     | data.gov.tw ID                               | 年份       | 格式 | 欄位                                   |
| -------------------------- | -------------------------------------------- | ---------- | ---- | -------------------------------------- |
| 歷史交通事故資料 (A1 & A2) | [12197](https://data.gov.tw/dataset/12197)   | 102–110 年 | CSV  | 發生時間、地點、死傷人數、車種、經緯度 |
| 111 年傷亡道路交通事故資料 | [161199](https://data.gov.tw/dataset/161199) | 111 年     | CSV  | 同上                                   |
| 112 年傷亡道路交通事故資料 | [167905](https://data.gov.tw/dataset/167905) | 112 年     | CSV  | 同上                                   |
| 113 年道路交通事故傷亡資料 | 搜尋「113年傷亡道路交通事故」                | 113 年     | CSV  | 同上                                   |

> **A1 類**: 造成人員當場或 24 小時內死亡之事故  
> **A2 類**: 造成人員受傷或超過 24 小時死亡之事故

### 2.2 輔助資料集

| 資料集                | data.gov.tw ID                             | 用途                        |
| --------------------- | ------------------------------------------ | --------------------------- |
| 各縣市人口統計        | [8411](https://data.gov.tw/dataset/8411)   | 計算 per-capita 事故率      |
| 即時交通事故資料 (A2) | [87495](https://data.gov.tw/dataset/87495) | Demo 用即時更新功能 (bonus) |

### 2.3 關鍵欄位對照

```
發生時間  →  year, month, day, hour  (時間模式分析)
發生地點  →  county, district        (地理分布分析)
死亡人數  →  fatalities              (嚴重程度)
受傷人數  →  injuries                (嚴重程度)
車種      →  vehicle_type            (車種風險分析)
經度/緯度 →  longitude, latitude     (地圖熱點)
```

---

## 3. 應用程式架構 App Architecture

```
SafeRoad-Taiwan/
├── app.py                     # Streamlit 主程式 (多頁面入口)
├── pages/
│   ├── 1_📊_Overview.py       # 全台總覽儀表板
│   ├── 2_🗺️_Hotspot_Map.py    # 事故熱點地圖
│   ├── 3_👤_Demographics.py   # 人口學風險剖面
│   ├── 4_🕐_Time_Patterns.py  # 時間模式分析
│   └── 5_🤖_AI_Report.py      # AI 安全快報
├── data/
│   ├── raw/                   # 從 data.gov.tw 下載的原始 CSV
│   └── processed/             # 清理合併後的資料
├── utils/
│   ├── data_loader.py         # 資料載入與快取
│   ├── preprocessing.py       # 資料清理函式
│   └── ai_report.py           # Claude API 報告生成
├── requirements.txt
├── .streamlit/
│   └── config.toml            # 主題設定 (dark mode)
└── README.md
```

---

## 4. 五個頁面設計 Page-by-Page Design

### Page 1: 📊 全台總覽 Overview Dashboard

**目標**: 一眼看懂台灣交通安全全貌

| Widget         | 內容                                            |
| -------------- | ----------------------------------------------- |
| KPI 卡片       | 年度總事故數、死亡人數、受傷人數、與去年比較 ↑↓ |
| 年度趨勢折線圖 | 102–113 年事故數趨勢 (Plotly line chart)        |
| 縣市排名橫條圖 | Top-10 事故率最高縣市 (per 10 萬人口)           |
| 篩選器         | 年份範圍 slider、A1/A2 類別 radio               |

### Page 2: 🗺️ 事故熱點地圖 Hotspot Map

**目標**: 哪裡最危險？ → 空間風險知覺

| Widget         | 內容                                    |
| -------------- | --------------------------------------- |
| Scatter mapbox | 以經緯度標示每筆事故 (color = 嚴重程度) |
| 密度圖層切換   | Heatmap mode vs. point mode             |
| 縣市/鄉鎮篩選  | Selectbox 可逐層下鑽                    |
| 圖表下方       | 選定區域的摘要統計                      |

### Page 3: 👤 人口學風險剖面 Demographics

**目標**: 誰最容易出事？ → 年齡×認知科學

| Widget                 | 內容                                   |
| ---------------------- | -------------------------------------- |
| 年齡層事故率 bar chart | 18–24、25–34、35–44、45–54、55–64、65+ |
| 車種×年齡交叉分析      | Grouped bar or heatmap                 |
| A1/A2 嚴重程度對照     | 老年組在 A1 事故中是否過度代表？       |
| 行為科學卡片           | 文字解說注意力衰退與反應時間的文獻摘要 |

### Page 4: 🕐 時間模式分析 Time Patterns

**目標**: 什麼時候最危險？ → 晝夜節律與警覺性

| Widget          | 內容                            |
| --------------- | ------------------------------- |
| 24 小時事故分布 | Polar / radial bar chart (美觀) |
| 星期×小時熱力圖 | 7×24 heatmap (Mon–Sun × 0–23h)  |
| 季節趨勢        | 月份事故數折線圖                |
| 行為科學卡片    | 解說疲勞駕駛的認知神經科學      |

### Page 5: 🤖 AI 安全快報 AI Report

**目標**: 讓 AI 說故事 → 資料 → 敘事

| Widget           | 內容                                                |
| ---------------- | --------------------------------------------------- |
| 篩選條件         | 選擇縣市、年份、事故類型                            |
| 「生成報告」按鈕 | 呼叫 Claude API                                     |
| 報告輸出         | Markdown 格式的安全快報，含重點統計、趨勢解讀、建議 |
| Prompt 設計      | 將篩選後的統計摘要作為 context 傳給 Claude          |

---

## 5. 每週開發時程 Weekly Development Timeline

### Week 09 (04/23)：Vibe Coding 入門 — 搭建專案骨架

**學習目標**: Claude Code CLI 基礎、專案初始化

| 任務                                              | 產出                                   |
| ------------------------------------------------- | -------------------------------------- |
| 安裝 Claude Code CLI，完成認證                    | 可運行的 CLI 環境                      |
| 用自然語言 prompt 生成專案目錄結構                | `SafeRoad-Taiwan/` 目錄                |
| 生成 `requirements.txt`                           | streamlit, plotly, pandas, requests    |
| 生成 `app.py` 多頁面入口 + 空白 placeholder pages | 可 `streamlit run app.py` 且看到側邊欄 |

**Claude Code 示範 prompt**:
```
Create a multi-page Streamlit app called "SafeRoad Taiwan". 
Set up the folder structure with pages/ directory containing 
5 empty page files. Add a requirements.txt with streamlit, 
plotly, pandas, and requests.
```

**作業**: 截圖展示可運行的 Streamlit 空殼 app

---

### Week 10 (04/30)：GitHub 工作流 — 版本控制與協作

**學習目標**: Git commit 流程、GitHub repo、README

| 任務                                              | 產出                  |
| ------------------------------------------------- | --------------------- |
| `git init` + 建立 GitHub repo                     | 公開 repo with README |
| 用 Claude Code 生成 `.gitignore` (Python + data/) | 排除大檔案            |
| 撰寫 `README.md` (專案簡介、安裝指令、截圖)       | 專業的 README         |
| 首次 push 全部程式碼                              | GitHub 上可見的 repo  |

**作業**: 提交 GitHub repo 連結

---

### Week 11 (05/07)：Streamlit 開發 — 建立 UI 框架

**學習目標**: Streamlit layout、widgets、charts

| 任務                                         | 產出                          |
| -------------------------------------------- | ----------------------------- |
| 設計 Page 1 Overview 的 UI layout            | `st.columns()`, `st.metric()` |
| 使用假資料 (mock data) 製作 KPI 卡片         | 4 個 metric 卡片              |
| 用 Plotly 製作年度趨勢折線圖 (假資料)        | 互動式折線圖                  |
| 設定 dark theme via `.streamlit/config.toml` | 統一視覺風格                  |
| 部署至 Streamlit Cloud (初版)                | 線上可存取的連結              |

**Claude Code 示範 prompt**:
```
In my Streamlit Overview page, create 4 KPI metric cards 
showing total accidents, fatalities, injuries, and year-over-year 
change. Use st.columns(4) layout. Below, add a Plotly line chart 
showing accident trends from 2013 to 2024. Use mock data for now.
```

**作業**: Streamlit Cloud 線上連結 + 截圖

---

### Week 12 (05/14)：Open Data API — 串接真實資料

**學習目標**: HTTP 下載、CSV 讀取、資料清理

| 任務                                                  | 產出                  |
| ----------------------------------------------------- | --------------------- |
| 撰寫 `utils/data_loader.py`：從 data.gov.tw 下載 CSV  | 自動下載腳本          |
| 撰寫 `utils/preprocessing.py`：合併多年份、標準化欄位 | 乾淨的合併 DataFrame  |
| 處理中文欄位名 → 英文欄位名映射                       | 統一的 column naming  |
| 加入 `@st.cache_data` 避免重複下載                    | 快速載入體驗          |
| 將 Page 1 的假資料替換為真實資料                      | Overview 顯示真實統計 |

**關鍵程式碼片段**:
```python
import pandas as pd
import requests
from io import StringIO

# 下載範例 (110年 A1)
url = "https://opdadm.moi.gov.tw/api/v1/no-auth/resource/api/dataset/67781E29-8AAD-46A9-A2C8-C3F339592C27/resource/A9F35ABD-0826-4403-800D-D4ACDC1A151A/download"
response = requests.get(url)
df = pd.read_csv(StringIO(response.text))
```

**⚠️ 注意事項**:
- CSV 可能為 Big5 或 UTF-8 編碼，需偵測處理
- 部分年份資料分上下半年兩個檔案（108–110年）
- 欄位名稱可能跨年不一致，需建立 mapping dict

**作業**: 展示 `data_loader.py` 能成功載入至少 3 年的資料

---

### Week 13 (05/21)：互動儀表板 — 視覺化深化

**學習目標**: 進階 Plotly 圖表、互動篩選

| 任務                                                 | 產出                |
| ---------------------------------------------------- | ------------------- |
| Page 2 熱點地圖：用 `px.scatter_mapbox` 繪製事故位置 | 台灣地圖 + 事故散點 |
| Page 3 人口學分析：年齡層 bar chart + 車種交叉分析   | 人口學圖表          |
| Page 4 時間模式：24h polar chart + 7×24 heatmap      | 時間相關圖表        |
| 每頁加入 sidebar 篩選器 (年份、縣市、A1/A2)          | 動態互動            |
| 加入行為科學解說卡片 (`st.info()` / `st.expander()`) | 學術脈絡            |

**Plotly 圖表規格**:
```python
# 24 小時事故分布 (polar bar chart)
fig = px.bar_polar(hourly_data, r="count", theta="hour",
                   color="severity", template="plotly_dark",
                   title="24 小時事故分布：何時最危險？")

# 星期 × 小時熱力圖
fig = px.density_heatmap(df, x="hour", y="weekday",
                         z="count", color_continuous_scale="YlOrRd")
```

**作業**: 至少完成 3 個頁面的互動圖表

---

### Week 14 (05/28)：Claude API — AI 安全快報功能

**學習目標**: Anthropic SDK、prompt engineering、responsible AI

| 任務                                                         | 產出             |
| ------------------------------------------------------------ | ---------------- |
| 註冊 Anthropic API、設定 API key (st.secrets)                | API 可用         |
| 撰寫 `utils/ai_report.py`：生成 prompt + 呼叫 API            | 報告生成模組     |
| 設計 system prompt：角色 = 交通安全分析師                    | 專業語氣的報告   |
| Page 5：使用者選條件 → 計算統計摘要 → 傳給 Claude → 顯示報告 | 完整 AI 報告頁面 |
| 加入安全防護：限制 API 呼叫頻率、處理錯誤                    | 穩健的錯誤處理   |

**Prompt 設計範例**:
```python
system_prompt = """你是一位台灣交通安全分析師。
請根據以下統計數據，撰寫一份 300 字以內的交通安全快報。
報告應包含：(1) 重點發現 (2) 趨勢解讀 (3) 行為建議。
語氣專業但易懂，適合一般民眾閱讀。"""

user_prompt = f"""
以下是 {county} 在 {year} 年的交通事故統計：
- 事故總數：{total_accidents}
- 死亡人數：{fatalities}
- 受傷人數：{injuries}
- 最高發時段：{peak_hour}:00
- 最多涉及車種：{top_vehicle}
- 年齡分布：{age_breakdown}
"""
```

**作業**: 展示 AI 生成的安全快報截圖

---

### Week 15 (06/04)：工作坊 — 打磨與 Peer Review

**學習目標**: 程式碼品質、UI/UX 最佳化、文件撰寫

| 任務                                                     | 產出           |
| -------------------------------------------------------- | -------------- |
| Peer code review (同學互評)                              | 程式改進建議   |
| UI/UX 優化：loading spinners、error messages、responsive | 流暢的使用體驗 |
| 加入 emoji、色彩一致性、自訂 CSS                         | 視覺升級       |
| README 完善：安裝步驟、截圖、資料來源引用                | 專業文件       |
| 排練 5 分鐘 Demo 流程                                    | 發表準備       |

**品質檢查清單**:
- [ ] 所有頁面的篩選器可正常運作
- [ ] 地圖載入速度 < 5 秒 (使用 cache)
- [ ] AI 報告在 API 失敗時有 graceful fallback
- [ ] README 包含完整的資料來源引用
- [ ] Streamlit Cloud 部署正常運行

---

### Week 16 (06/18)：期末發表 Final Presentation

**發表格式**: 5 分鐘 Live Demo + 2 分鐘 Q&A

| 時間      | 內容                                                       |
| --------- | ---------------------------------------------------------- |
| 0:00–0:30 | 問題導入：「台灣每天有 __ 件交通事故…」                    |
| 0:30–1:30 | Page 1 Overview：全台趨勢與關鍵數字                        |
| 1:30–2:30 | Page 2 Hotspot Map：切換到地圖，zoom in 到特定高風險區     |
| 2:30–3:30 | Page 3–4 Demographics & Time：展示年齡與時間的行為科學洞察 |
| 3:30–4:30 | Page 5 AI Report：即時 Demo Claude 生成報告                |
| 4:30–5:00 | 結論與未來方向                                             |

**評分標準** (佔學期成績 35%):

| 項目         | 比重 | 說明                        |
| ------------ | ---- | --------------------------- |
| 技術實作     | 40%  | 資料處理、視覺化、AI 整合   |
| 資料敘事     | 25%  | 能否用數據說出有意義的故事  |
| UI/UX        | 15%  | 介面美觀、互動流暢          |
| 行為科學連結 | 10%  | 與認知/心理學文獻的整合深度 |
| 程式碼品質   | 10%  | Git history、模組化、文件   |

---

## 6. 行為科學延伸閱讀 Behavioral Science References

> 以下文獻供學生在專案中引用，增加學術深度

| 主題           | 參考文獻                                                                                                                                                                                                                                                  |
| -------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 疲勞駕駛       | Williamson, A. M., & Feyer, A. M. (2000). Moderate sleep deprivation produces impairments in cognitive and motor performance equivalent to legally prescribed levels of alcohol intoxication. *Occupational and Environmental Medicine*, 57(10), 649–655. |
| 老年駕駛認知   | Anstey, K. J., Wood, J., Lord, S., & Walker, J. G. (2005). Cognitive, sensory and physical factors enabling driving safety in older adults. *Clinical Psychology Review*, 25(1), 45–65.                                                                   |
| 注意力晝夜節律 | Schmidt, C., et al. (2007). A time to think: Circadian rhythms in human cognition. *Cognitive Neuropsychology*, 24(7), 755–789.                                                                                                                           |
| 風險知覺       | Slovic, P. (1987). Perception of risk. *Science*, 236(4799), 280–285.                                                                                                                                                                                     |

---

## 7. 技術備忘 Technical Notes

### 環境設定
```bash
# 建立虛擬環境
conda create -n saferoad python=3.11
conda activate saferoad

# 安裝套件
pip install streamlit plotly pandas requests anthropic

# 本機測試
streamlit run app.py
```

### Streamlit Cloud 部署
1. Push to GitHub
2. 到 [share.streamlit.io](https://share.streamlit.io) 選擇 repo
3. 設定 secrets (Claude API key)
4. Deploy!

### 注意事項
- **編碼**: 政府資料常用 Big5 編碼，讀取時需指定 `encoding='big5'` 或 `'utf-8-sig'`
- **欄位一致性**: 不同年份 CSV 的欄位名稱可能不同，建議建立統一 mapping
- **資料量**: A2 全年資料可達數十萬筆，建議使用 `@st.cache_data` + 預處理
- **地圖**: 需申請 Mapbox token (免費) 或使用 `open-street-map` tile
