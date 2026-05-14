# Week 13 PPTX Slide Outline

> **用途**：供後續 slide deck card creation / PPTX 製作用。  
> **語言原則**：主要文字使用台灣華語，關鍵技術詞保留 English terms in parentheses。

## Deck Title

Week 13: 互動式儀表板與資料敘事  
(Interactive Dashboards & Data Storytelling)

## Slide 1｜本週主題

**標題**：從可信資料到互動敘事

**重點**：
- Week 12：建立資料清理流程 (data pipeline)
- Week 13：把真實資料變成互動圖表 (interactive charts)
- 核心問題：圖表如何幫助讀者理解資料，而不只是「看起來漂亮」

**視覺**：`load → clean → describe → analyse → plot → story` 流程圖

## Slide 2｜為什麼這很重要

**標題**：Dashboard 不是圖表集合

**重點**：
- 好的 dashboard 回答明確問題
- 每張圖都應該服務一個訊息 (one message per chart)
- 使用者需要探索資料，也需要被引導解讀

**視覺**：左側「雜亂圖表牆」，右側「有敘事順序的 dashboard」

## Slide 3｜本週兩個真實資料集

**標題**：同一條 pipeline，兩種資料來源

**重點**：
- PsyArXiv preprints：API + JSON
- 教育部高教統計：CSV + schema alignment
- 差異在 load，核心流程可共用

**視覺**：兩欄比較卡片：API (REST API) vs CSV (bulk data)

## Slide 4｜學習目標

**標題**：今天你會學會什麼

**重點**：
- 使用 pagination 抓取 API 資料
- 將 nested JSON 轉成 DataFrame
- 合併跨年度 CSV
- 用 Plotly 製作互動圖表
- 用 annotation 與 caption 建立 data storytelling

**視覺**：5 個 icon checklist

## Slide 5｜Plotly 的角色

**標題**：從靜態圖到互動探索

**重點**：
- Matplotlib：適合論文圖 (static figure)
- Plotly：適合 dashboard 與探索式分析 (exploratory analysis)
- Hover、zoom、legend filtering 讓讀者能自己檢查資料

**視覺**：Matplotlib vs Plotly 對照表

## Slide 6｜Plotly Express 基本模式

**標題**：一行函式，一張互動圖

**重點**：
- `px.bar()`
- `px.line()`
- `px.scatter()`
- `st.plotly_chart()` 嵌入 Streamlit

**視覺**：程式碼卡片 + 對應圖表縮圖

## Slide 7｜Dataset A：PsyArXiv

**標題**：心理學界正在討論什麼？

**重點**：
- PsyArXiv 是心理學 preprint server
- Metadata 包含 title、tags、subjects、date
- 適合練習 API、pagination、JSON parsing

**視覺**：preprint metadata 卡片：title / date / subject / tags

## Slide 8｜API Pagination

**標題**：為什麼不能只抓第一頁？

**重點**：
- API 通常分頁回傳 (pagination)
- 每頁最多 100 筆
- Loop 每一頁，累積成完整資料集
- 加上 `time.sleep()` 避免過度請求

**視覺**：Page 1 → Page 2 → Page 3 → DataFrame

## Slide 9｜JSON 到 DataFrame

**標題**：把 nested JSON 攤平成 tidy data

**重點**：
- OSF 回傳 nested JSON
- `attributes` 裡面才有 title、date、tags
- `subjects` 是 list of lists
- 分析前要整理成一列一篇 preprint

**視覺**：nested JSON 樹狀圖 → tidy table

## Slide 10｜Cleaning Decisions

**標題**：清理資料要說得出代價

**重點**：
- 觀察：日期是 string
- 動作：轉成 datetime
- 代價：無法解析者變成 `NaT`
- 每個 cleaning decision 都要可解釋

**視覺**：「觀察 → 動作 → 代價」三段流程卡

## Slide 11｜PsyArXiv 圖 1：Top Subjects

**標題**：哪些主題最常出現？

**重點**：
- 使用 horizontal bar chart
- 長 label 適合放在 y 軸
- 顏色用來強化排序，不只是裝飾

**視覺**：Top 15 subjects bar chart

## Slide 12｜PsyArXiv 圖 2：Monthly Volume

**標題**：發表量是否有時間趨勢？

**重點**：
- 使用 line chart
- `hovermode="x unified"` 方便比較
- 用 annotation 標出 peak
- Annotation 應該說明意義，不只是標數字

**視覺**：月發表量 line chart + peak annotation

## Slide 13｜PsyArXiv 圖 3：Title Length vs Tags

**標題**：Metadata 也可以做品質檢查

**重點**：
- Scatter plot 適合看 outlier
- `hover_name` 顯示具體論文標題
- Legend 太多時可以關閉
- 低 R² 也可能是有用結果

**視覺**：scatter plot + outlier hover tooltip

## Slide 14｜Dataset B：教育部高教統計

**標題**：少子化如何反映在高教資料？

**重點**：
- 105–113 學年度校別學生數
- 真實政策議題
- 適合練習跨年度 CSV 合併與中文欄位清理

**視覺**：台灣高教資料表 + 年度時間軸

## Slide 15｜Schema Alignment

**標題**：不同年度的欄位不一定一樣

**重點**：
- `pd.concat()` 可合併多個年度
- 缺少的欄位會補成 `NaN`
- `NaN` 不一定代表資料缺漏，也可能代表 schema evolution

**視覺**：105 年欄位、107 年欄位、113 年欄位疊合示意

## Slide 16｜中文欄位清理

**標題**：真實資料常常藏著編碼規則

**重點**：
- `"30 臺北市"` 要拆成 `city_name`
- `"1 一般"` 要拆成 `system`
- 數字欄位可能被讀成文字
- 公私立可先用 rule-based cleaning

**視覺**：原始欄位 → 清理後欄位對照表

## Slide 17｜MOE 圖 1：總學生數趨勢

**標題**：總量變化先看大局

**重點**：
- Line chart 回答「整體是否下降」
- 先看總量，再拆分類別
- Policy dashboard 需要清楚的 takeaway

**視覺**：105–113 學年度總學生數 line chart

## Slide 18｜MOE 圖 2：公立 vs 私立

**標題**：下降是否集中在特定 sector？

**重點**：
- Stacked bar 比較總量組成
- Grouped / stacked 要依問題選擇
- Caption 應該解讀趨勢，而不是描述圖表類型

**視覺**：public/private stacked bar chart

## Slide 19｜Data Storytelling 五原則

**標題**：讓圖表說出研究問題

**重點**：
- One message per chart
- Context before detail
- Label what matters
- Show uncertainty
- Earn the complexity

**視覺**：五原則放射圖或 5-card grid

## Slide 20｜Common Pitfalls

**標題**：互動圖表常見錯誤

**重點**：
- 只抓 API 第一頁
- 合併 CSV 後不檢查欄位
- 把 100 種 subject 都放進 legend
- Annotation 只寫數字，不寫意義
- Caption 只是重複圖表標題

**視覺**：錯誤清單 + warning icons

## Slide 21｜Homework Brief

**標題**：把兩個資料集整合進 Streamlit dashboard

**重點**：
- PsyArXiv：至少 2 張 Plotly 圖
- MOE：至少 2 張 Plotly 圖
- 至少一張圖含 annotation
- 每張圖下方寫 takeaway caption
- 每個 dataset 至少一個 widget

**視覺**：dashboard wireframe

## Slide 22｜Takeaway

**標題**：資料可信，圖表才有說服力

**重點**：
- Pipeline 讓資料可信
- Plotly 讓資料可探索
- Storytelling 讓分析有方向
- Dashboard 的目標不是展示所有資料，而是幫助使用者做判斷

**視覺**：三角形：Pipeline / Interactivity / Storytelling
