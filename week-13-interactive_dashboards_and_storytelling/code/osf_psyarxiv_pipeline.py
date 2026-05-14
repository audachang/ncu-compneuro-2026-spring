"""
Week 13 demo — OSF PsyArXiv Preprint Pipeline
==============================================

End-to-end demo of the Week 12 pipeline applied to a large dataset:

    API (OSF PsyArXiv)  →  JSON parse  →  pandas DataFrame
                        →  clean / describe / analyse
                        →  Plotly interactive visualisations

Dataset size : ~1,000 most-recent PsyArXiv preprints (10 pages × 100/page).
Why it matters: PsyArXiv is the de-facto preprint server for psychology and
behavioural science. Its API exposes title, abstract, tags, subjects, and
publication date — enough to ask: *what is psychology talking about right now?*

Run:  python osf_psyarxiv_pipeline.py
Output: psyarxiv_recent.csv  +  three opened Plotly figures in the browser.

Author: ACL@NCU — Erik Chang  (CompBigData 2026 Spring)
"""

from __future__ import annotations

import time
from collections import Counter
from pathlib import Path

import pandas as pd
import plotly.express as px
import requests

# ---------------------------------------------------------------------------
# 0. Constants
# ---------------------------------------------------------------------------
OSF_ENDPOINT = "https://api.osf.io/v2/preprint_providers/psyarxiv/preprints/"
N_PAGES = 10           # 10 pages × 100 per page  → ~1,000 preprints
PAGE_SIZE = 100
SLEEP = 0.3            # seconds between calls — be polite to the API
OUT_CSV = Path(__file__).with_name("psyarxiv_recent.csv")
HEADERS = {"User-Agent": "NS5116-week13-teaching-example"}


# ---------------------------------------------------------------------------
# 1. LOAD — pull paginated results from the OSF API
# ---------------------------------------------------------------------------
def fetch_psyarxiv(n_pages: int = N_PAGES) -> list[dict]:
    """抓取最近 ``n_pages * 100`` 筆 PsyArXiv preprints。

    OSF API 一次最多回傳 100 筆，所以要做 pagination。每呼叫之間
    sleep 0.3s 避免被 rate-limit。回傳的是 raw JSON 'data' list。
    """
    all_items: list[dict] = []
    for page in range(1, n_pages + 1):
        params = {
            "page": page,
            "page[size]": PAGE_SIZE,
            "sort": "-date_published",  # newest first
        }
        r = requests.get(OSF_ENDPOINT, params=params, timeout=30, headers=HEADERS)
        r.raise_for_status()
        batch = r.json().get("data", [])
        all_items.extend(batch)
        print(f"  page {page:2d}: got {len(batch)} items  (total {len(all_items)})")
        time.sleep(SLEEP)
    return all_items


# ---------------------------------------------------------------------------
# 2. PARSE — JSON → flat DataFrame
# ---------------------------------------------------------------------------
def parse_to_df(items: list[dict]) -> pd.DataFrame:
    """把 OSF 巢狀 JSON 攤平成 tidy DataFrame。

    Subjects 在 OSF 是 nested list-of-lists（subject path），我們
    只保留最深層（最具體）的那一個 label，方便後續 groupby。
    """
    records = []
    for it in items:
        a = it.get("attributes", {})
        subjects = a.get("subjects", [])
        # 取每個 chain 最後一層 (most specific label)
        leaf_subjects = [
            chain[-1].get("text")
            for chain in subjects
            if chain and chain[-1].get("text")
        ]
        records.append({
            "id": it.get("id"),
            "title": a.get("title", "").strip(),
            "description": (a.get("description") or "").strip(),
            "date_published": a.get("date_published"),
            "date_created": a.get("date_created"),
            "tags": a.get("tags", []),
            "n_tags": len(a.get("tags", [])),
            "subjects": leaf_subjects,
            "primary_subject": leaf_subjects[0] if leaf_subjects else None,
            "doi": a.get("doi"),
            "n_description_chars": len(a.get("description") or ""),
        })
    return pd.DataFrame(records)


# ---------------------------------------------------------------------------
# 3. CLEAN — observation-driven fixes
# ---------------------------------------------------------------------------
def clean(df: pd.DataFrame) -> pd.DataFrame:
    """根據 describe() 觀察到的問題逐一修補。

    觀察 → 動作 → 代價
    ----------------------------------------------------
    1. date_published 是 ISO string  →  pd.to_datetime
       代價：少數無 date 的會變 NaT，後面 plot 會自動忽略。
    2. title / description 可能有空字串 →  filter out
       代價：失去 < 1% 的列，但避免 keyword 統計被空字串污染。
    3. primary_subject 缺值 →  填 'Unspecified'
       代價：可能掩蓋編碼問題；但相較直接 dropna 更保留 n。
    """
    df = df.copy()
    df["date_published"] = pd.to_datetime(df["date_published"], errors="coerce", utc=True)
    # to_period() 會 drop timezone — 先 tz_convert(None) 避開 warning
    df["year_month"] = (df["date_published"].dt.tz_convert(None)
                          .dt.to_period("M").dt.to_timestamp())
    df["title_len"] = df["title"].str.len()
    df = df[df["title"].str.len() > 0].copy()
    df["primary_subject"] = df["primary_subject"].fillna("Unspecified")
    return df


# ---------------------------------------------------------------------------
# 4. DESCRIBE — quick health check
# ---------------------------------------------------------------------------
def describe(df: pd.DataFrame) -> None:
    """印出資料的健康檢查摘要 — Week 12 風格。"""
    print(f"\n  n rows           : {len(df)}")
    print(f"  date range       : {df['date_published'].min()}  →  {df['date_published'].max()}")
    print(f"  unique subjects  : {df['primary_subject'].nunique()}")
    print(f"  n_tags  (M / SD) : {df['n_tags'].mean():.2f}  /  {df['n_tags'].std():.2f}")
    print(f"  desc len (M / SD): {df['n_description_chars'].mean():.0f}  /  "
          f"{df['n_description_chars'].std():.0f}")
    print("\n  top 5 subjects:")
    print(df["primary_subject"].value_counts().head().to_string())


# ---------------------------------------------------------------------------
# 5. ANALYSE / VISUALISE — Plotly
# ---------------------------------------------------------------------------
def plot_subject_distribution(df: pd.DataFrame):
    """Bar chart — 哪個 psychology subfield 發文最多？"""
    counts = (df["primary_subject"]
              .value_counts()
              .head(15)
              .reset_index()
              .rename(columns={"index": "subject", "primary_subject": "subject", "count": "n"}))
    counts.columns = ["subject", "n"]
    fig = px.bar(
        counts,
        x="n", y="subject",
        orientation="h",
        color="n",
        color_continuous_scale="Blues",
        title="Top 15 PsyArXiv subjects (recent ~1000 preprints)",
        labels={"n": "Number of preprints", "subject": "Primary subject"},
    )
    fig.update_layout(yaxis={"categoryorder": "total ascending"},
                      coloraxis_showscale=False)
    return fig


def plot_monthly_volume(df: pd.DataFrame):
    """Line chart — 隨時間 preprint 數量趨勢，含 annotation。"""
    monthly = (df.dropna(subset=["year_month"])
                 .groupby("year_month").size()
                 .reset_index(name="n_preprints"))
    fig = px.line(
        monthly, x="year_month", y="n_preprints", markers=True,
        title="PsyArXiv preprints per month",
        labels={"year_month": "Month", "n_preprints": "Number of preprints"},
    )
    # 標註最高峰
    peak = monthly.loc[monthly["n_preprints"].idxmax()]
    fig.add_annotation(
        x=peak["year_month"], y=peak["n_preprints"],
        text=f"Peak: {int(peak['n_preprints'])} preprints",
        showarrow=True, arrowhead=2,
        bgcolor="rgba(255,255,255,0.8)", bordercolor="black",
    )
    fig.update_layout(hovermode="x unified")
    return fig


def plot_tag_keywords(df: pd.DataFrame):
    """Scatter / treemap — preprint title 長度 vs. tags 數量。

    Hover 顯示 title，可看出哪些是高 tag、高 title-length 的論文。
    """
    fig = px.scatter(
        df, x="n_tags", y="title_len",
        color="primary_subject",
        hover_name="title",
        hover_data={"date_published": True, "primary_subject": True},
        opacity=0.6,
        title="PsyArXiv preprints — title length vs. tag count",
        labels={"n_tags": "Number of tags", "title_len": "Title length (chars)"},
    )
    fig.update_layout(showlegend=False)  # legend 太多 subject 會擋畫面
    return fig


# ---------------------------------------------------------------------------
# 6. MAIN
# ---------------------------------------------------------------------------
def main():
    print("[1/5] Fetching from OSF PsyArXiv...")
    items = fetch_psyarxiv(N_PAGES)

    print(f"\n[2/5] Parsing {len(items)} items into DataFrame...")
    df_raw = parse_to_df(items)

    print("\n[3/5] Describe — BEFORE clean")
    describe(df_raw.assign(
        date_published=pd.to_datetime(df_raw["date_published"], errors="coerce"),
        year_month=pd.NaT,
        title_len=df_raw["title"].str.len(),
    ))

    print("\n[4/5] Cleaning...")
    df = clean(df_raw)

    print("\n     Describe — AFTER clean")
    describe(df)

    # Save CSV
    df.drop(columns=["tags", "subjects"]).to_csv(OUT_CSV, index=False)
    print(f"\n     Saved CSV → {OUT_CSV}")

    print("\n[5/5] Generating Plotly figures...")
    fig1 = plot_subject_distribution(df)
    fig2 = plot_monthly_volume(df)
    fig3 = plot_tag_keywords(df)

    # 在 script 環境用 .show()，在 Streamlit 用 st.plotly_chart(fig)
    fig1.show()
    fig2.show()
    fig3.show()
    print("\nDone.")


if __name__ == "__main__":
    main()
