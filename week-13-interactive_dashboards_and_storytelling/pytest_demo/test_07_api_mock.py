"""用 pytest-httpx 模擬 API 回應。

對應講義：『模擬 API 回應』、『使用 pytest-httpx』、『模擬 404 / 500』

關鍵：
- pytest-httpx 提供一個內建 fixture `httpx_mock`
- 用 `httpx_mock.add_response(url=..., json=..., status_code=...)` 註冊假回應
- 之後 httpx.get/post 不會真的連網，而是直接回 mock data

⚠️ 需要先安裝：
    pip install pytest-httpx

跑：
    pytest test_07_api_mock.py -v
"""

import httpx
import pytest

from analysis import fetch_user_meta


# ---------------------------------------------------------------------------
# 1. 模擬 200 OK
# ---------------------------------------------------------------------------

def test_mocked_200(httpx_mock):
    httpx_mock.add_response(
        url="https://api.example.com/data",
        json={"message": "success"},
        status_code=200,
    )

    response = httpx.get("https://api.example.com/data")
    assert response.status_code == 200
    assert response.json() == {"message": "success"}


# ---------------------------------------------------------------------------
# 2. 模擬 404 Not Found
# ---------------------------------------------------------------------------

def test_mocked_404(httpx_mock):
    httpx_mock.add_response(
        url="https://api.example.com/notfound",
        status_code=404,
        json={"error": "Not Found"},
    )

    response = httpx.get("https://api.example.com/notfound")
    assert response.status_code == 404
    assert response.json()["error"] == "Not Found"


# ---------------------------------------------------------------------------
# 3. 模擬 500 並驗證我們自己的 fetch_user_meta 會 raise
# ---------------------------------------------------------------------------

def test_fetch_user_meta_raises_on_500(httpx_mock):
    """fetch_user_meta() 內部呼叫 response.raise_for_status()。

    我們可以用 mock 強制讓 server 「壞掉」，然後檢查我們的程式有沒有正確
    把錯誤往外丟（而不是默默吞掉）。
    """
    httpx_mock.add_response(
        url="https://jsonplaceholder.typicode.com/users/99",
        status_code=500,
        json={"error": "Internal Server Error"},
    )

    with pytest.raises(httpx.HTTPStatusError):
        fetch_user_meta(user_id=99)


# ---------------------------------------------------------------------------
# 4. 模擬一個自訂 base_url，順便確認我們的函式組合 URL 正確
# ---------------------------------------------------------------------------

def test_fetch_user_meta_uses_custom_base_url(httpx_mock):
    httpx_mock.add_response(
        url="https://my-mirror.example.org/users/7",
        json={"id": 7, "name": "Erik", "email": "erik@example.org"},
        status_code=200,
    )

    user = fetch_user_meta(user_id=7, base_url="https://my-mirror.example.org")
    assert user["id"] == 7
    assert user["name"] == "Erik"


# ---------------------------------------------------------------------------
# 5. 一個 fixture 可以在 test 之間共用 mock 設定
# ---------------------------------------------------------------------------

@pytest.fixture
def mock_pubmed_eutils(httpx_mock):
    """模擬 PubMed E-utilities 回傳一筆假文獻 metadata。

    真實情境：你的研究 pipeline 會抓某個 PMID 的標題、摘要、年份。
    在 CI 上跑時不希望真的打 NCBI 的 API（rate limit）。
    """
    httpx_mock.add_response(
        url="https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?db=pubmed&id=12345",
        json={
            "result": {
                "12345": {
                    "title": "Stroop interference in healthy aging",
                    "pubdate": "2024",
                    "authors": [{"name": "Chang E"}],
                }
            }
        },
        status_code=200,
    )
    return "12345"


def test_pubmed_metadata(mock_pubmed_eutils):
    pmid = mock_pubmed_eutils
    response = httpx.get(
        f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?db=pubmed&id={pmid}"
    )
    paper = response.json()["result"][pmid]
    assert "Stroop" in paper["title"]
    assert paper["pubdate"] == "2024"
