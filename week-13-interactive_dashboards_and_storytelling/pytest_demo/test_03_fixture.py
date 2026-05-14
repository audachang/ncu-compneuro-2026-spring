"""Fixture 機制：setup + teardown + scope。

對應講義：『使用 Fixture 設定測試環境』、『yield 做 setup + teardown』

示範：
- 注入 conftest.py 中的 fixture（stroop_data）
- 在檔案內定義 fixture
- 用 yield 寫 setup / teardown
- 不同 scope 的差別（function / module / session）
- 用 tmp_path 處理暫存檔

跑：
    pytest test_03_fixture.py -v -s    # -s 讓 print 真的顯示出來
"""

from __future__ import annotations

import time

import numpy as np
import pytest

from analysis import compute_accuracy, compute_mean_rt


# ---------------------------------------------------------------------------
# 1. 使用 conftest.py 中已經定義好的 fixture
# ---------------------------------------------------------------------------

def test_stroop_accuracy(stroop_data):
    """stroop_data 由 conftest.py 自動注入，不需 import。"""
    acc = compute_accuracy(stroop_data["correct"])
    assert 0.85 < acc < 1.0, f"預期 acc ≈ 0.92，實際 {acc:.3f}"


def test_stroop_effect(stroop_data):
    """檢查 incongruent RT > congruent RT（這就是 Stroop effect）。"""
    rts = stroop_data["rts"]
    cond = stroop_data["conditions"]
    rt_cong = rts[cond == "congruent"].mean()
    rt_incong = rts[cond == "incongruent"].mean()
    assert rt_incong > rt_cong, (
        f"Stroop effect 反向：congruent={rt_cong:.1f}, incongruent={rt_incong:.1f}"
    )


# ---------------------------------------------------------------------------
# 2. 在檔案內定義 fixture（只在這個檔案中可用）
# ---------------------------------------------------------------------------

@pytest.fixture
def small_rt_array() -> np.ndarray:
    """Hard-coded 小 array，方便人類用心算驗證。"""
    return np.array([400, 450, 500, 550, 600], dtype=float)


def test_mean_rt_simple(small_rt_array):
    rt = compute_mean_rt(small_rt_array, only_correct=False)
    assert rt == 500.0


# ---------------------------------------------------------------------------
# 3. yield 做 setup + teardown（搭配 conftest.py 的 temp_session_log）
# ---------------------------------------------------------------------------

def test_session_log_writes(temp_session_log):
    """檢查 fixture 建立的 log 確實存在，並可被附加寫入。"""
    assert temp_session_log.exists()
    with temp_session_log.open("a", encoding="utf-8") as f:
        f.write("trial 1 done\n")
    content = temp_session_log.read_text(encoding="utf-8")
    assert "trial 1 done" in content


# ---------------------------------------------------------------------------
# 4. Scope：module / session 的 fixture 只執行一次，在多 test 共用
# ---------------------------------------------------------------------------

@pytest.fixture(scope="module")
def expensive_setup() -> dict:
    """模擬一個耗時的 setup（例如：載入大型 .nii fMRI volume）。

    `scope="module"` 表示這個 fixture 在整個 module 中只跑一次，
    所有 test 共用同一個結果。
    """
    print("\n[expensive_setup] 開始載入大型資料集...")
    time.sleep(0.05)            # 假裝它很慢
    rng = np.random.default_rng(123)
    return {"voxels": rng.standard_normal((1000, 100))}     # 1000 voxel × 100 TR


def test_voxels_shape(expensive_setup):
    assert expensive_setup["voxels"].shape == (1000, 100)


def test_voxels_zero_mean(expensive_setup):
    """因為 scope=module，這裡會用 *和上一個 test 同一個* fixture 結果。"""
    assert abs(expensive_setup["voxels"].mean()) < 0.1
