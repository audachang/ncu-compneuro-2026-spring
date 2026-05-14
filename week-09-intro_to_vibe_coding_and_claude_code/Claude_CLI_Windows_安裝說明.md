# Claude CLI 在 Windows PowerShell 的首次啟動與登入說明

## 事前準備

確認已安裝 Node.js（版本 ≥ 18）。在 PowerShell 中執行以下指令確認：

```powershell
node --version
```

若尚未安裝，請至 [https://nodejs.org](https://nodejs.org) 下載安裝，完成後重新開啟 PowerShell 使 PATH 生效。

---

## 步驟一：安裝 Claude CLI

在 PowerShell 中執行：

```powershell
npm install -g @anthropic-ai/claude-code
```

安裝完成後，確認版本：

```powershell
claude --version
# 輸出範例：Claude Code v2.1.114
```

---

## 步驟二：進入專案資料夾並啟動

```powershell
cd C:\Projects\my-project
claude
```

首次啟動會看到歡迎畫面：

```
Welcome to Claude Code v2.1.114
```

---

## 步驟三：選擇登入方式

CLI 會顯示互動式選單，使用 **方向鍵** 選擇、**Enter** 確認：

```
Select login method:

❯ 1. Claude account with subscription  · Pro, Max, Team, or Enterprise
  2. Anthropic Console account         · API usage billing
  3. 3rd-party platform                · Amazon Bedrock, Microsoft Foundry, or Vertex AI
```

| 選項 | 適用情況 |
|------|---------|
| **1（建議）** | 已有 Claude.ai 訂閱帳號（Pro / Max / Team / Enterprise） |
| 2 | 使用 Anthropic Console API 金鑰，按 token 計費 |
| 3 | 透過 Amazon Bedrock、Microsoft Foundry 或 Vertex AI 存取 |

一般用戶請選 **選項 1**。

---

## 步驟四：瀏覽器 OAuth 授權

選擇選項 1 後，CLI 會自動開啟預設瀏覽器，導向：

```
https://claude.ai/oauth/authorize?...
```

瀏覽器會顯示如下授權同意頁面：

> **Claude Code would like to connect to your Claude chat account**
>
> YOUR ACCOUNT WILL BE USED TO:
> - ✓ Access your Anthropic profile information
> - ✓ Contribute to your Claude subscription usage
> - ✓ Access your Claude Code sessions
> - ✓ Use and manage your connectors
> - ✓ Upload files on your behalf
> - ✓ Your privacy settings apply to coding sessions

若您已在該瀏覽器登入 Claude.ai，頁面底部會顯示您的帳號（例如 `you@gmail.com`）。確認帳號無誤後，點選 **Authorize（授權）** 按鈕。

> **注意：** 若瀏覽器未自動開啟，請複製 PowerShell 中顯示的 URL，手動貼入瀏覽器網址列。

---

## 步驟五：授權完成，進入互動模式

授權成功後，PowerShell 會顯示：

```
✓ Logged in as you@gmail.com

 Claude Code  (claude-sonnet-4-5)
 cwd: C:\Projects\my-project

>
```

在 `>` 提示符後輸入您的第一個指令或問題即可開始使用。

---

## 憑證儲存位置（Windows）

登入後的認證資訊會儲存於：

```
%APPDATA%\Claude\
```

實際路徑通常為：

```
C:\Users\<您的使用者名稱>\AppData\Roaming\Claude\
```

往後每次執行 `claude` 時會自動讀取此憑證，**無需重複登入**，除非 Session 過期。

---

## 常見問題

| 問題 | 解決方式 |
|------|---------|
| `claude` 指令找不到 | 關閉並重新開啟 PowerShell，或執行 `refreshenv` |
| 瀏覽器未自動開啟 | 手動複製 URL 貼入瀏覽器 |
| 想切換帳號 | 在瀏覽器授權頁面點選「Switch account」 |
| 重新登入 | 在 PowerShell 執行 `claude logout` 後再執行 `claude` |
