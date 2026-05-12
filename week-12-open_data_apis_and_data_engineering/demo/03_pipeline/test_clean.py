"""pytest tests for clean() — 對應 Homework 第 3 點。

執行：
    pytest test_clean.py -v

示範如何用 pytest 測試 pure cleaning function，
不需要真實 CSV 也不需要真實 API。
"""

import numpy as np
import pandas as pd
import pytest

from pipeline import clean


def _make_messy(rt_ms, age, condition):
    """組一個 messy 小 DataFrame — 一定義一筆 row。"""
    return pd.DataFrame({
        "subject_id": [1, 2, 3],
        "condition":  condition,
        "rt_ms":      rt_ms,
        "accuracy":   [1, 1, 1],
        "age":        age,
    })


def test_rt_ms_NA_becomes_nan_then_dropped():
    """rt_ms = 'NA' → to_numeric coerce → NaN → between() 篩掉。"""
    df = _make_messy(
        rt_ms=["NA", 500, 600],
        age=[30, 40, 50],
        condition=["congruent", "incongruent", "congruent"],
    )
    out = clean(df)
    assert len(out) == 2
    assert out["rt_ms"].dtype.kind == "f"


def test_99999_sentinel_filtered():
    """rt_ms = 99999 在 between(150, 3000) 之外 → 被剔除。"""
    df = _make_messy(
        rt_ms=[400, 99999, 600],
        age=[30, 40, 50],
        condition=["congruent", "congruent", "incongruent"],
    )
    out = clean(df)
    assert 99999 not in out["rt_ms"].values
    assert len(out) == 2


def test_age_minus_999_becomes_nan():
    """age = -999 應該被換成 NaN（不剔除 row）。"""
    df = _make_messy(
        rt_ms=[400, 500, 600],
        age=[-999, 40, 50],
        condition=["congruent", "incongruent", "congruent"],
    )
    out = clean(df)
    assert out["age"].isna().sum() == 1
    assert len(out) == 3   # row 沒被剔除


def test_condition_recoded():
    """condition 大小寫不一致 + 'incong' 縮寫應該被統一。"""
    df = _make_messy(
        rt_ms=[400, 500, 600],
        age=[30, 40, 50],
        condition=["Congruent", "INCONG", "incongruent"],
    )
    out = clean(df)
    assert set(out["condition"].unique()) <= {"congruent", "incongruent"}


def test_clean_does_not_mutate_input():
    """clean() 必須是 pure function — 不能改到輸入的 df。"""
    df = _make_messy(
        rt_ms=["NA", 500, 600],
        age=[-999, 40, 50],
        condition=["Congruent", "INCONG", "incongruent"],
    )
    original = df.copy()
    _ = clean(df)
    pd.testing.assert_frame_equal(df, original)
