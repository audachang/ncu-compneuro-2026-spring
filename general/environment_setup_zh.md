# Python + PsychoPy 環境設置指南

對於初學者而言，要在單一環境中整合 **Python** 與 **PsychoPy**，最穩健且容易上手的方法是使用 **Conda（建議使用 Miniforge 或 Anaconda）**。

雖然 PsychoPy 提供「獨立安裝版 (Standalone)」，那是對一般實驗設計最簡單的選擇，但它是一個封閉環境，難以整合其他 Python 庫。因此，透過 Conda 建立虛擬環境是目前最能兼顧「靈活性」與「穩定性」的方案。

---

## 🚀 推薦安裝流程 (Conda 途徑)

### 1. 安裝環境管理工具

下載並安裝 [Miniforge](https://github.com/conda-forge/miniforge) 或 [Anaconda](https://www.anaconda.com/)。Miniforge 更為輕量且預設使用 `conda-forge` 頻道，對於 PsychoPy 的相依性支援較佳。

### 2. 建立專屬虛擬環境

開啟終端機（Terminal 或 Anaconda Prompt），輸入以下指令建立一個 Python 3.10 的環境（這是目前 PsychoPy 支援度最穩定的版本）：

```bash
conda create -n psychopy_env python=3.10
conda activate psychopy_env
```

### 3. 安裝 PsychoPy

在同一個環境中安裝 PsychoPy。使用 `pip` 安裝通常比單純用 `conda install` 能獲得更新、更完整的依賴項：

```bash
pip install psychopy
```

---

## ⚠️ 重要提醒

> **事實查核 (Fact Checking)：** 安裝過程中若遇到相依性問題，請務必人工查核原始來源（如 [PsychoPy 官方文件](https://www.psychopy.org/download.html)）。
> **關鍵決策 (Critical Decisions)：** 本建議僅供參考，AI 僅能提供選項，最終系統更改的責任與決定應由您親自承擔。

### 為什麼這個方法最穩健？

1. **隔離性：** 虛擬環境確保 PsychoPy 的複雜依賴項（如 `wxPython`）不會與你系統的其他 Python 專案衝突。
2. **易於修復：** 如果環境搞砸了，直接刪除該環境重來即可，不會影響作業系統。

---

### 參考來源

* [PsychoPy 官方安裝文件 (v2025.2.4)](https://www.psychopy.org/download.html) **指出**，對於需要自定義環境的用戶，建議使用 `pip` 安裝於 Conda 環境中。
* [Conda-Forge PsychoPy Package](https://anaconda.org/conda-forge/psychopy) 提供了跨平台的相依性管理資訊。
* [PsychoPy Manual install via Conda (Video)](https://www.youtube.com/watch?v=9KpWOqsoa4k) - 詳細示範如何在不使用獨立安裝版的情況下，透過 Conda 建立環境並在 VS Code 中運行 PsychoPy。

## 🧪 環境測試 (Testing Your Environment)

執行下方的 Python 腳本來檢查您的環境是否已成功識別 PsychoPy 並能啟動視窗。

```python
import sys
import psychopy
from psychopy import visual, core, event

def check_environment():
    print("="*40)
    print("       ENVIRONMENT CHECK       ")
    print("="*40)
    print(f"Python Version: {sys.version.split()[0]}")
    print(f"PsychoPy Version: {psychopy.__version__}")
    
    print("-" * 40)
    print("Testing PsychoPy Window...")
    print("Opening a window for 3 seconds...")
    
    try:
        # Create a window
        win = visual.Window(size=[800, 600], color=[0, 0, 0], units="pix", fullscr=False)
        msg = visual.TextStim(win, text="PsychoPy is working!", color=[1, 1, 1], height=30)
        msg.draw()
        win.flip()
        core.wait(3)
        win.close()
        print("[Ok] PsychoPy window test passed.")
    except Exception as e:
        print(f"[!!] PsychoPy test failed: {e}")
    
    print("="*40)

if __name__ == "__main__":
    check_environment()
```
