"""第一個 test：基本 assert 用法。

對應講義：『撰寫第一個 test』、『assert 是什麼』、『assert vs if』

❶ 檔名必須以 test_ 開頭
❷ 函式名也必須以 test_ 開頭
❸ 用 assert 描述「我預期這個東西為真」

跑：
    pytest test_01_basic_assert.py -v
"""

import math


# ---------------------------------------------------------------------------
# 1. 最簡單的 test — 只是檢查算術
# ---------------------------------------------------------------------------

def test_addition():
    assert 1 + 1 == 2


def test_subtraction():
    assert 5 - 3 == 2


# ---------------------------------------------------------------------------
# 2. 帶錯誤訊息的 assert — 第二個參數會在失敗時印出
# ---------------------------------------------------------------------------

def test_assert_with_message():
    x = 10
    assert x > 5, f"預期 x 大於 5，實際得到 {x}"


# ---------------------------------------------------------------------------
# 3. 浮點數比較：絕對不要用 ==，要用 math.isclose 或 pytest.approx
# ---------------------------------------------------------------------------

def test_float_equality_naive():
    # 0.1 + 0.2 在 IEEE 754 中不是 0.3 — 這個 test 會 PASS 因為我們用 isclose
    assert math.isclose(0.1 + 0.2, 0.3)


def test_float_equality_with_pytest_approx():
    import pytest
    assert (0.1 + 0.2) == pytest.approx(0.3)


# ---------------------------------------------------------------------------
# 4. 檢查 collection 的長度與內容
# ---------------------------------------------------------------------------

def test_list_membership():
    conditions = ["congruent", "incongruent", "neutral"]
    assert "congruent" in conditions
    assert len(conditions) == 3
    assert conditions[0] != conditions[1]
