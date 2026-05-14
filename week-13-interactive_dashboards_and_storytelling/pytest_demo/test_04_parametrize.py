"""參數化測試：@pytest.mark.parametrize。

對應講義：『參數化測試 (Parameterized Testing)』

示範：
- 一個 test 函式跑多組 input/expected
- 用 ids= 為每組參數命名（pytest 輸出更易讀）
- 多個參數 decorator 疊加 → 笛卡兒積（cartesian product）

跑：
    pytest test_04_parametrize.py -v
"""

import math

import pytest

from analysis import compute_dprime


# ---------------------------------------------------------------------------
# 1. 基本：3 組 (a, b, expected)
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("a, b, expected", [
    (1, 2, 3),
    (5, 5, 10),
    (10, -1, 9),
])
def test_add(a, b, expected):
    assert a + b == expected


# ---------------------------------------------------------------------------
# 2. 用 ids= 讓輸出有意義的名稱
# ---------------------------------------------------------------------------

@pytest.mark.parametrize(
    "hits, fa, n, expected_sign",
    [
        (8, 2, 10, +1),     # 高 hit、低 FA → d' > 0
        (2, 8, 10, -1),     # 低 hit、高 FA → d' < 0
        (5, 5, 10,  0),     # 對稱 → d' ≈ 0
    ],
    ids=["good_detector", "bad_detector", "chance_level"],
)
def test_dprime_sign(hits, fa, n, expected_sign):
    d = compute_dprime(hits, fa, n)
    if expected_sign == 0:
        assert math.isclose(d, 0.0, abs_tol=1e-10)
    elif expected_sign > 0:
        assert d > 0.5
    else:
        assert d < -0.5


# ---------------------------------------------------------------------------
# 3. 笛卡兒積：兩個 parametrize 疊加 → 9 個 test
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("hits", [3, 5, 7])
@pytest.mark.parametrize("n", [10, 20, 50])
def test_dprime_finite_across_grid(hits, n):
    """在 9 種 (hits × n) 組合下，d' 都應該是有限值。"""
    d = compute_dprime(hits, false_alarms=hits, n_signal=n)
    assert math.isfinite(d)


# ---------------------------------------------------------------------------
# 4. 進階：用一個 list of dict 做更可讀的測試表
# ---------------------------------------------------------------------------

DPRIME_CASES = [
    {"name": "very_high",   "h": 19, "fa":  1, "n": 20, "min": 2.5},
    {"name": "high",        "h": 15, "fa":  5, "n": 20, "min": 1.0},
    {"name": "moderate",    "h": 13, "fa":  7, "n": 20, "min": 0.3},
]

@pytest.mark.parametrize("case", DPRIME_CASES, ids=[c["name"] for c in DPRIME_CASES])
def test_dprime_above_threshold(case):
    d = compute_dprime(case["h"], case["fa"], case["n"])
    assert d > case["min"], f"{case['name']}: d'={d:.2f} 未達門檻 {case['min']}"
