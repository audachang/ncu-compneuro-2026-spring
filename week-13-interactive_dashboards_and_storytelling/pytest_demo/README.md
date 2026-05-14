# pytest Demo — NS5116 Week 13

> 配合投影片 `pytest_lecture_NS5116.pptx` 的可執行範例集

本資料夾包含 8 個檔案，每一個對應講義中的一個主題。所有範例皆可在 5 秒內跑完，並使用 **認知神經科學情境**（Stroop、RT outlier、d-prime、訊號偵測理論、API 抓取文獻 metadata 等）。

---

## 📁 檔案總覽

| 檔案 | 對應講義主題 | 涵蓋 pytest 概念 |
|------|---------------|------------------|
| `analysis.py` | 共用程式碼 | 被 test 檢查的「實際分析函式」 |
| `conftest.py` | Fixture 機制 | 全資料夾共用的 fixture（synthetic Stroop 資料） |
| `test_01_basic_assert.py` | 第一個 test、assert 用法 | `assert`、檔名 / 函式命名規則 |
| `test_02_dprime.py` | assert 在 pytest 的應用 | 多個 assert、邊界值檢查 |
| `test_03_fixture.py` | Fixture：setup + teardown | `@pytest.fixture`、`yield`、scope |
| `test_04_parametrize.py` | 參數化測試 | `@pytest.mark.parametrize`、ids |
| `test_05_rt_outlier.py` | Parametrize 實戰 | RT mean ± k·SD outlier rejection 測試 |
| `test_06_api_httpx.py` | API 測試（真實連網） | `httpx.get`、`response.status_code` |
| `test_07_api_mock.py` | pytest-httpx 模擬回應 | `httpx_mock.add_response`、404 / 500 模擬 |

---

## 🚀 快速開始

### 安裝依賴

```bash
pip install pytest pytest-httpx httpx numpy scipy
```

### 跑全部 test

```bash
cd week-13-interactive_dashboards_and_storytelling/pytest_demo
pytest                    # 簡潔輸出
pytest -v                 # 顯示每個 test 的名稱
pytest -v --tb=short      # 失敗時用簡短 traceback
```

### 只跑某一個檔案

```bash
pytest test_03_fixture.py -v
```

### 只跑某一個 test 函式

```bash
pytest test_04_parametrize.py::test_compute_dprime -v
```

### 跳過需要連網的 test

```bash
pytest -k "not api_httpx"
```

---

## 🔬 試試看 — Hands-on 練習

1. 故意把 `analysis.py` 裡的 `compute_dprime` 改錯（例如把 `-` 改成 `+`），重新跑 `pytest`，觀察錯誤訊息如何幫你定位問題。
2. 在 `test_05_rt_outlier.py` 加入新的 `(k, expected_n)` 組合，例如 `(0.5, 38)`，測試極端 k 值。
3. 把 `test_07_api_mock.py` 中的 `status_code=200` 改成 `503`，看看應用層的 fallback 邏輯是否能正確處理。

---

## 💡 Pro tips

- 失敗時加 `--pdb` 會在第一個失敗的 test 自動進入 Python debugger。
- `pytest --collect-only` 只顯示哪些 test 會被執行，不真的跑。
- `pytest -x` 一遇到失敗就停止，適合 debug 時加快迭代。
- `pytest --lf`（last failed）只重跑上次失敗的那些 test。

---

*Last updated: 2026-05-14 · Erik Chang (張智宏) · NCU Cognitive Neuroscience*
