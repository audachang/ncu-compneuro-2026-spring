# Week 11 Homework — N-back Working Memory Dashboard with Streamlit

> **Course:** NS5116 電腦硬體與程式語言在行為科學實驗與大數據分析之應用 — Spring 2026
> **Due:** Before Week 12 (2026-05-14, 23:59) | **Submit via:** eeclass
> **預估時間：** 1.5–2 小時（入門難度）

---

## Overview

本週課堂上你看了 cognitive aging dashboard 的完整 demo（n=400 lifespan 認知測驗）。
這份作業給你一個 **新的 N-back working memory 資料集**，請你獨立把它變成一個互動式 Streamlit dashboard，並部署到 Streamlit Community Cloud。

完成後，你會有一個 **可以丟到履歷上的 live demo URL** — 任何人用瀏覽器都能打開、操作你的分析成果。

---

## Dataset：N-back Working Memory (n=200 受試者，3 conditions)

模擬 200 名受試者完成 1-back / 2-back / 3-back 三個記憶負荷條件的工作記憶實驗。
每位受試者 3 列（每個 condition 一列），共 **600 列**。

📄 檔案：`data/nback_working_memory.csv`（已附在 starter 內）

### Columns

| Column | Type | Description |
|--------|------|-------------|
| `participant_id` | str | P001 – P200 |
| `age` | int | 18 – 75 |
| `sex` | "F" / "M" | |
| `education` | int | 受教育年數 (9–22) |
| `group` | str | young (18–34) / middle (35–54) / older (55–75) |
| `condition` | str | "1-back" / "2-back" / "3-back" |
| `n_trials` | int | 通常 80 |
| `accuracy` | float | 0–1 |
| `mean_rt_ms` | float | 正確 trial 的平均 RT (ms) |
| `d_prime` | float | Signal-detection 敏感度指標 |

### 預期看到的型態（資料生成基於此設計）

- `accuracy` 隨 condition load 上升而下降（1-back > 2-back > 3-back）。
- 年齡越大，accuracy 與 d' 越低、RT 越慢。
- 高 load 條件的年齡效應更大（**load × age 交互作用**）。

---

## Learning Objectives

完成本作業後，你會能夠：

1. 用 `pandas.read_csv` 載入 CSV 資料並做基本錯誤處理。
2. 加入 sidebar widgets（slider / multiselect / selectbox）讓使用者篩選資料。sidebar使用方式請參考本週課程下app資料夾的app.py，以及課程投影片。
3. 用 `st.metric` 顯示關鍵摘要數字。
4. 用 matplotlib 畫一張依使用者選擇而動態變化的圖。
5. 用 `st.dataframe` 與 `st.download_button` 顯示與下載篩選後的資料。
6. 把 app 推到 GitHub 並部署到 Streamlit Community Cloud。

---

## 作業需求

### 必作項目（70 pts，達成才算完成基本要求）

請完成以下 6 個區塊。建議從 `starter/app.py` 開始填空。

#### 1. 資料載入 + 錯誤處理（10 pts）

- 用 `pd.read_csv("data/nback_working_memory.csv")` 載入資料。
- 載入失敗（檔案不存在）時用 `st.error(...)` 顯示訊息並 `st.stop()`。

#### 2. Sidebar — 至少 3 個 widget（15 pts）

在 `st.sidebar` 內放：

- **Age range slider** — 範圍 18–75，預設整段。
- **Sex multiselect** — 選項 ["F", "M"]，預設兩者皆選。
- **Condition selectbox**（或 multiselect 也可） — 選 1-back / 2-back / 3-back 至少一個。

每個 widget 套用後篩選出 `df_filtered`，用於後續顯示。

#### 3. 主畫面：3 個 metric（10 pts）

用 `st.columns(3)` 並排顯示：

- 篩選後的受試者人數（rows / 唯一 participant 數任選）
- 篩選後的平均 accuracy（小數點後 2 位）
- 篩選後的平均 RT（整數 ms）

#### 4. 主畫面：1 張 chart（15 pts）

至少一張圖，能展現 **age × performance** 的關係。例如：

- 散佈圖：x = age, y = accuracy（或 d'、RT）— 用 condition 上色
- 或：bar plot — 三個 group × 三個 condition 的 accuracy

要求：
- 用 matplotlib 並透過 `st.pyplot(fig)` 顯示。
- 圖要有 `xlabel`, `ylabel`, `title`, `legend`。

#### 5. 主畫面：篩選後 dataframe + 下載按鈕（10 pts）

- `st.dataframe(df_filtered)` 顯示篩選後資料。
- `st.download_button` 提供 CSV 下載。

#### 6. 部署到 Streamlit Cloud（10 pts）

- 把 app 推上 **public GitHub repo**（檔名 `app.py`，附 `requirements.txt` 與 `data/`）。
- 在 [share.streamlit.io](https://share.streamlit.io) 部署，取得公開 URL。
- 確認 URL 用無痕視窗能打開。

### 加分項目（每項 +5 pts，最多 +15 pts，bonus 計入總分但封頂 100）

- **Bonus A — Status messages（+5 pts）**：在資料載入與篩選後，用 `st.success / st.warning / st.info` 給使用者明確回饋（例如：「載入 600 列」、「警告：篩選後僅 N=12，太少」）。
- **Bonus B — 多分頁（+5 pts）**：用 `st.tabs([...])` 或 sidebar selectbox 把畫面分為「Overview / By condition / Raw data」至少兩個分頁。
- **Bonus C — Reflection（+5 pts）**：在 README 加一段 100 字內的 reflection：「這個 dashboard 最適合什麼類型的觀眾？為什麼？」

---

## 繳交內容（請在 eeclass 上傳一份 PDF/text 含以下三個項目）

1. **GitHub repo URL**：`https://github.com/<your-name>/<repo>`（須 public）
2. **Streamlit Cloud URL**：`https://<your-app>.streamlit.app`（須能打開）
3. **一張 dashboard 截圖**（PNG/JPG）— 顯示 widget 全部設定後的主畫面

> **注意：** 不要把 `__pycache__/`、`.venv/`、`.DS_Store` 推到 GitHub。記得寫 `.gitignore`。

---

## Rubric（總分 100 + bonus）

| 項目 | Pts | 評分觀察點 |
|------|-----|-----------|
| 1. 資料載入 + 錯誤處理 | 10 | `pd.read_csv` 正確；檔案不存在時用 `st.error + st.stop` |
| 2. Sidebar widgets | 15 | 至少 3 個、各自正確篩選資料 |
| 3. Metric 三件 | 10 | 數值會隨 widget 變化、格式正確 |
| 4. Chart 視覺化 | 15 | 圖能反應 widget 選擇、軸標籤齊全 |
| 5. Dataframe + download | 10 | dataframe 顯示正確；download 能下載 |
| 6. 部署 Streamlit Cloud | 10 | URL 可開、internet access 看得到結果 |
| README + 截圖 | 10 | README 有 how-to-run；截圖清楚 |
| Code 品質 | 10 | 命名合理、沒有 dead code、有少量註解 |
| **Subtotal** | **90** | |
| Bonus A/B/C | +15 | 每項 +5，最多三項 |
| **Total** | **100 (cap)** | |

---

## Step-by-Step Checklist（建議順序）

完成順序建議如下，對入門者最不挫折：

```text
□ Step 1.  cd 到一個新資料夾，把 starter/ 內容複製進來
□ Step 2.  python -m venv .venv && activate
□ Step 3.  pip install -r requirements.txt
□ Step 4.  streamlit run app.py — 確認看到 starter 的 placeholder 畫面
□ Step 5.  完成 TODO 1（load + error handling）— 重啟確認資料載入成功
□ Step 6.  完成 TODO 2（3 個 sidebar widgets）— 拖 slider 應看到 df 行數變
□ Step 7.  完成 TODO 3（metrics）
□ Step 8.  完成 TODO 4（chart）
□ Step 9.  完成 TODO 5（dataframe + download）
□ Step 10. 全部 local 跑通，截圖
□ Step 11. git init / commit / push 到 public GitHub repo
□ Step 12. 到 share.streamlit.io 連 repo / app.py 部署
□ Step 13. 用無痕視窗打開部署 URL，再次截圖
□ Step 14. 把 GitHub URL + Streamlit URL + 截圖 上傳 eeclass
```

---

## 常見錯誤與排除

| 症狀 | 通常原因 | 解法 |
|------|----------|------|
| `FileNotFoundError: data/nback_working_memory.csv` | cwd 不是 repo 根 | 用 `Path(__file__).parent / "data" / "..."` 寫絕對路徑 |
| 部署後 app 起不來 | 忘記 `requirements.txt` 或 `data/` 沒推到 repo | 檢查 GitHub 上有沒有這兩個 |
| 拖 slider 沒反應 | 漏掉用 widget 回傳值篩 df | `df = df_all[mask]` 一定要出現 |
| `plt.show()` 沒畫面 | 在 Streamlit 內要用 `st.pyplot(fig)` | 換掉 |
| `& and ambiguous` 錯誤 | 用 Python `and` 而非 `&` | numpy/pandas boolean 用 `&` |
| Streamlit Cloud build 失敗 | requirements.txt 缺套件或寫錯版本 | 看 build log，補足 |

---

## Resources

- 本週 demo：[`week-11-web_app_development_with_streamlit/app/app.py`](../../week-11-web_app_development_with_streamlit/app/app.py)
- 本週講義：[`week-11-web_app_development_with_streamlit.md`](../../week-11-web_app_development_with_streamlit/week-11-web_app_development_with_streamlit.md)
- Streamlit cheat sheet: <https://cheat-sheet.streamlit.app/>
- Streamlit deploy 文件: <https://docs.streamlit.io/deploy/streamlit-community-cloud>
- 陳 YT (2020). [Streamlit 入門](https://medium.com/@yt.chen/機器學習-資料科學框架應用-streamlit入門-1-d07478cd4d8). Medium.
- Mhadhbi, N. (2026). [Streamlit Tutorial](https://www.datacamp.com/tutorial/streamlit). DataCamp.

---

## Tips

- **不要過度設計**：rubric 沒給 bonus 的 layout / theme 不會加分。先把必作 6 項弄完，再加 bonus。
- **Widget 預設值要全選**：別讓 reviewer 一打開 app 看到空白 — 預設要顯示完整資料。
- **commit 訊息要寫好**：`Initial app skeleton`、`Add age slider and metrics`、`Fix sex filter` 比 `update`、`fix` 好太多。
- **先在 local 跑通再 push**：避免在 Streamlit Cloud 上 debug。
- **截圖要清楚**：建議全螢幕截圖，sidebar 與主畫面都要看得到。

---

*文件版本：2026-05-07 by Erik Chang，配合 Week 11 主教材使用。*
