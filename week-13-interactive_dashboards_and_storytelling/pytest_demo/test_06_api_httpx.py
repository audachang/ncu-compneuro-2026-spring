"""真實 API 測試（會打網路請求）。

對應講義：『測試 API（搭配 httpx）』

⚠️ 這個檔案中的 test 會真的連到 https://jsonplaceholder.typicode.com，
    所以 (1) 需要網路；(2) 比較慢；(3) 服務掛掉時 test 也會跟著失敗。
    這就是為什麼下一個檔案 (test_07_api_mock.py) 改用 mocking。

我們把這些 test 標記為 `network`，方便用 -m 控制是否跑。

跑：
    pytest test_06_api_httpx.py -v                 # 全部
    pytest test_06_api_httpx.py -v -m network      # 只跑需要網路的
    pytest -m "not network"                        # 跳過需要網路的
"""

import httpx
import pytest

from analysis import fetch_user_meta


pytestmark = pytest.mark.network    # 整個檔案都標記為 network


# ---------------------------------------------------------------------------
# 1. 直接呼叫 httpx
# ---------------------------------------------------------------------------

def test_get_user_status_code():
    response = httpx.get("https://jsonplaceholder.typicode.com/users/1", timeout=5.0)
    assert response.status_code == 200


def test_get_user_payload():
    response = httpx.get("https://jsonplaceholder.typicode.com/users/1", timeout=5.0)
    data = response.json()
    assert data["id"] == 1
    assert "name" in data
    assert "email" in data


# ---------------------------------------------------------------------------
# 2. 呼叫我們自己包好的 fetch_user_meta
# ---------------------------------------------------------------------------

def test_fetch_user_meta_returns_dict():
    user = fetch_user_meta(user_id=2)
    assert isinstance(user, dict)
    assert user["id"] == 2
