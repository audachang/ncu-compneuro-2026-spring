"""被 pytest 檢查的「實際分析函式」。

這個模組蒐集本資料夾中各個 test 檔會用到的核心分析函式：
- compute_accuracy / compute_mean_rt   行為實驗常用 summary
- reject_outliers                       mean ± k·SD outlier rejection
- compute_dprime                        signal detection theory d-prime
- fetch_user_meta                       一個會打 HTTP 的 helper（用來示範 mocking）
"""

from __future__ import annotations

import httpx
import numpy as np
from scipy.stats import norm


# ---------------------------------------------------------------------------
# Behavioral summaries
# ---------------------------------------------------------------------------

def compute_accuracy(correct: np.ndarray) -> float:
    """回傳 accuracy 比例 (0.0 – 1.0)。

    Parameters
    ----------
    correct : 1-D array of int (0 / 1) 或 bool
    """
    correct = np.asarray(correct)
    if correct.size == 0:
        return float("nan")
    return float(correct.mean())


def compute_mean_rt(rts: np.ndarray, only_correct: bool = True,
                    correct: np.ndarray | None = None) -> float:
    """計算平均 RT，可選擇只取正確 trial。"""
    rts = np.asarray(rts, dtype=float)
    if only_correct:
        if correct is None:
            raise ValueError("only_correct=True 時必須提供 correct array")
        rts = rts[np.asarray(correct).astype(bool)]
    if rts.size == 0:
        return float("nan")
    return float(rts.mean())


# ---------------------------------------------------------------------------
# Outlier rejection
# ---------------------------------------------------------------------------

def reject_outliers(rts: np.ndarray, k: float = 3.0) -> np.ndarray:
    """以 mean ± k·SD 規則剔除 outlier RT。"""
    rts = np.asarray(rts, dtype=float)
    if rts.size == 0:
        return rts
    m, sd = rts.mean(), rts.std()
    return rts[(rts > m - k * sd) & (rts < m + k * sd)]


# ---------------------------------------------------------------------------
# Signal detection theory
# ---------------------------------------------------------------------------

def compute_dprime(hits: int, false_alarms: int, n_signal: int,
                   n_noise: int | None = None) -> float:
    """d' = z(hit_rate) - z(fa_rate)，含 ±0.5 邊界 correction。

    使用 Macmillan & Creelman (1991) 推薦的「(h+0.5)/(N+1)」修正，
    避免 hit_rate 為 0 或 1 時 z 變成 ±inf。

    Parameters
    ----------
    hits           : 訊號試次中正確說「有」的次數
    false_alarms   : 雜訊試次中錯誤說「有」的次數
    n_signal       : 訊號試次總數
    n_noise        : 雜訊試次總數（預設與 n_signal 相同）
    """
    if n_noise is None:
        n_noise = n_signal
    if hits < 0 or false_alarms < 0:
        raise ValueError("hits / false_alarms 不能是負數")
    if hits > n_signal or false_alarms > n_noise:
        raise ValueError("hits / false_alarms 不能超過試次總數")

    hit_rate = (hits + 0.5) / (n_signal + 1)
    fa_rate = (false_alarms + 0.5) / (n_noise + 1)
    return float(norm.ppf(hit_rate) - norm.ppf(fa_rate))


# ---------------------------------------------------------------------------
# HTTP helper — used to demonstrate API mocking
# ---------------------------------------------------------------------------

def fetch_user_meta(user_id: int, base_url: str = "https://jsonplaceholder.typicode.com") -> dict:
    """從 JSONPlaceholder 取得單一使用者 metadata。

    這個函式存在的唯一目的是讓我們在 test 中示範 *如何 mock httpx*。
    在真實的研究 pipeline 中，這可能是「從 PubMed E-utilities 抓某篇文獻的 metadata」。
    """
    response = httpx.get(f"{base_url}/users/{user_id}", timeout=5.0)
    response.raise_for_status()
    return response.json()
