"""Project-wide pytest fixtures.

放在 `conftest.py` 中的 fixture 會 *自動被同資料夾下所有 test 檔* 共用，
不需要 import。pytest 會自動發現它們。
"""

from __future__ import annotations

import numpy as np
import pytest


# ---------------------------------------------------------------------------
# 行為實驗合成資料
# ---------------------------------------------------------------------------

@pytest.fixture
def stroop_data() -> dict:
    """模擬一個 Stroop 實驗：60 個 trial，congruent / incongruent 各半。

    回傳 dict 包含：
        rts        : ndarray, RT in ms
        conditions : ndarray of str ('congruent' / 'incongruent')
        correct    : ndarray of int (0/1)
    """
    rng = np.random.default_rng(42)
    n_per_cond = 30
    rts = np.concatenate([
        rng.normal(450, 60, n_per_cond),     # congruent
        rng.normal(520, 80, n_per_cond),     # incongruent
    ])
    conditions = np.array(["congruent"] * n_per_cond + ["incongruent"] * n_per_cond)
    correct = rng.binomial(1, 0.92, 2 * n_per_cond)
    return {"rts": rts, "conditions": conditions, "correct": correct}


@pytest.fixture
def rts_with_outliers() -> np.ndarray:
    """100 個 trial 的 RT，故意混入 5 個 outlier。"""
    rng = np.random.default_rng(0)
    clean = rng.normal(500, 80, 95)
    outliers = np.array([1500, 1800, 100, 80, 2000], dtype=float)
    return np.concatenate([clean, outliers])


# ---------------------------------------------------------------------------
# Setup + Teardown 示範（test_03_fixture.py 會用到）
# ---------------------------------------------------------------------------

@pytest.fixture
def temp_session_log(tmp_path):
    """建立一個臨時資料夾與 session log，test 結束後自動由 tmp_path 清理。

    `tmp_path` 是 pytest 內建的 fixture，會幫你建立一個 unique tmp directory。
    """
    log_path = tmp_path / "session.log"
    log_path.write_text("session start\n", encoding="utf-8")
    print(f"\n[setup] log created at {log_path}")
    yield log_path
    print(f"[teardown] log size = {log_path.stat().st_size} bytes")
    # 不需要手動 unlink — pytest 會自動清理 tmp_path
