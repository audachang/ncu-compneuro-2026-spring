"""測試 d-prime 計算函式。

對應講義：『assert 在 pytest 中的應用』、『邊界值檢查』

示範：
- 用多個 assert 在同一個 test 中檢查不同性質
- 邊界情況（hits=0, hits=n）的處理
- 用 pytest.raises 檢查錯誤輸入是否正確 raise

跑：
    pytest test_02_dprime.py -v
"""

import math

import pytest

from analysis import compute_dprime


# ---------------------------------------------------------------------------
# 1. 對稱情況：hit_rate == fa_rate → d' 應該為 0
# ---------------------------------------------------------------------------

def test_dprime_zero_when_rates_equal():
    d = compute_dprime(hits=5, false_alarms=5, n_signal=10)
    assert math.isclose(d, 0.0, abs_tol=1e-10)


# ---------------------------------------------------------------------------
# 2. 完美 detection：hit_rate ≫ fa_rate → d' 應該大很多
# ---------------------------------------------------------------------------

def test_dprime_high_when_perfect_detection():
    d = compute_dprime(hits=10, false_alarms=0, n_signal=10)
    assert d > 2.5, f"預期 d' > 2.5（接近 3），實際 {d:.3f}"


# ---------------------------------------------------------------------------
# 3. 邊界情況：hits=0 與 hits=n 不能回傳 ±inf（因為有 0.5 修正）
# ---------------------------------------------------------------------------

def test_dprime_finite_at_extremes():
    d_zero = compute_dprime(hits=0, false_alarms=0, n_signal=20)
    d_full = compute_dprime(hits=20, false_alarms=20, n_signal=20)
    assert math.isfinite(d_zero), "hits=0 時 d' 不該是 inf"
    assert math.isfinite(d_full), "hits=n 時 d' 不該是 inf"


# ---------------------------------------------------------------------------
# 4. 錯誤輸入：用 pytest.raises 檢查我們有沒有正確抓到 ValueError
# ---------------------------------------------------------------------------

def test_dprime_rejects_negative_hits():
    with pytest.raises(ValueError, match="不能是負數"):
        compute_dprime(hits=-1, false_alarms=0, n_signal=10)


def test_dprime_rejects_overflow():
    with pytest.raises(ValueError, match="超過試次總數"):
        compute_dprime(hits=15, false_alarms=0, n_signal=10)


# ---------------------------------------------------------------------------
# 5. 對稱性：交換 hits 與 false_alarms 應該讓 d' 變號
# ---------------------------------------------------------------------------

def test_dprime_sign_flips_when_swapped():
    d_pos = compute_dprime(hits=8, false_alarms=2, n_signal=10)
    d_neg = compute_dprime(hits=2, false_alarms=8, n_signal=10)
    assert math.isclose(d_pos, -d_neg, abs_tol=1e-10)
