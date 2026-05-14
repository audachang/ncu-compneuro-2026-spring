"""Parametrize 實戰：RT outlier rejection。

對應講義：『Parametrize 實戰：RT outlier 邊界檢查』

示範：
- 用 fixture 提供原始資料，用 parametrize 列舉不同 k 值
- 用 approx 容許數值誤差
- 結合 monkeypatch 暫時改寫 numpy 的 random seed（進階）

跑：
    pytest test_05_rt_outlier.py -v
"""

import numpy as np
import pytest

from analysis import reject_outliers


# ---------------------------------------------------------------------------
# 1. 不同 k 值下的保留比例
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("k, min_kept, max_kept", [
    (1.0,  60, 80),     # 1 SD ≈ 68%
    (2.0,  90, 99),     # 2 SD ≈ 95%
    (3.0,  95, 100),    # 3 SD ≈ 99.7%
])
def test_reject_outliers_proportions(k, min_kept, max_kept):
    rng = np.random.default_rng(42)
    rts = rng.normal(500, 80, 1000)
    n_kept = len(reject_outliers(rts, k=k))
    pct = 100 * n_kept / len(rts)
    assert min_kept <= pct <= max_kept, f"k={k} 時保留 {pct:.1f}% (預期 {min_kept}–{max_kept}%)"


# ---------------------------------------------------------------------------
# 2. 配合 conftest.py 的 rts_with_outliers fixture
# ---------------------------------------------------------------------------

def test_obvious_outliers_are_rejected(rts_with_outliers):
    """100 個 trial 中有 5 個極端 outlier，3 SD 規則應該全部剔除。"""
    cleaned = reject_outliers(rts_with_outliers, k=3.0)
    assert 90 <= len(cleaned) <= 99   # 大部分保留，極端值剔除
    assert cleaned.max() < 1500       # 1500 / 1800 / 2000 應該被砍掉


# ---------------------------------------------------------------------------
# 3. Edge case：空 array 不應該爆掉
# ---------------------------------------------------------------------------

def test_reject_outliers_empty_array():
    result = reject_outliers(np.array([], dtype=float), k=3.0)
    assert result.size == 0


# ---------------------------------------------------------------------------
# 4. Edge case：所有值都一樣（SD = 0）— 應該全部保留
# ---------------------------------------------------------------------------

def test_reject_outliers_zero_variance():
    rts = np.full(50, 500.0)
    # SD=0 時 mean ± k*SD 是一個點，所有 rts 等於 mean → 不在嚴格 < / > 區間 → 全部被剔除
    result = reject_outliers(rts, k=3.0)
    assert result.size == 0     # 文件化目前的行為（未必是理想行為！）


# ---------------------------------------------------------------------------
# 5. Property：剔除後的 array 一定是原 array 的子集
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("seed", [0, 1, 7, 42, 100])
def test_reject_returns_subset(seed):
    rng = np.random.default_rng(seed)
    rts = rng.normal(500, 80, 200)
    cleaned = reject_outliers(rts, k=2.0)
    assert set(cleaned.tolist()).issubset(set(rts.tolist()))
