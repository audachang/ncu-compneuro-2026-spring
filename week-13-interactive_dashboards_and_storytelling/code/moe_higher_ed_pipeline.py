"""
Week 13 demo — 教育部高等教育統計 (MOE Higher Education Stats) Pipeline
========================================================================

End-to-end demo of the Week 12 pipeline applied to a Taiwan open-data
dataset:

    CSV download (教育部統計處)  →  pandas concat across years
                              →  clean / describe / analyse
                              →  Plotly interactive visualisations

Dataset size : 大專校院校別學生數，學年度 105–113 共 9 年，合併後 ~7,200 列。
Why it matters: 台灣少子化 (declining birth rate) 對高等教育的衝擊是
                公共政策與生涯規劃的熱門議題。同一支 pipeline 可以同時
                回答「總量趨勢」、「公私立差異」、「縣市分布」三個問題。

Run:   python moe_higher_ed_pipeline.py
Output: moe_higher_ed.csv  +  three Plotly figures.

Source: https://stats.moe.gov.tw  (Open Government Data, public domain)
Author: ACL@NCU — Erik Chang  (CompBigData 2026 Spring)
"""

from __future__ import annotations

from io import StringIO
from pathlib import Path

# 教育部 stats.moe.gov.tw 的 SSL 憑證觸發 OpenSSL 3.x 的
# "Missing Subject Key Identifier" 錯誤。truststore 改用作業系統
# (Windows / macOS) 的憑證儲存區驗證,必須在 import requests 之前呼叫。
import truststore
truststore.inject_into_ssl()

import pandas as pd
import plotly.express as px
import requests

# ---------------------------------------------------------------------------
# 0. Constants
# ---------------------------------------------------------------------------
MOE_URL_TEMPLATE = "https://stats.moe.gov.tw/files/detail/{year}/{year}_student.csv"
YEARS = list(range(105, 114))   # 105 → 113 學年度，共 9 年
OUT_CSV = Path(__file__).with_name("moe_higher_ed.csv")
HEADERS = {"User-Agent": "NS5116-week13-teaching-example"}


# ---------------------------------------------------------------------------
# 1. LOAD — download one CSV per year and concat
# ---------------------------------------------------------------------------
def fetch_year(year: int) -> pd.DataFrame:
    """下載單一學年度的校別學生數 CSV。

    教育部統計處的檔案使用 UTF-8 with BOM。不同年度欄位略有變動，
    所以這裡只先讀進來，schema 對齊延後到 clean() 處理。
    """
    url = MOE_URL_TEMPLATE.format(year=year)
    r = requests.get(url, timeout=30, headers=HEADERS)
    r.raise_for_status()
    df = pd.read_csv(StringIO(r.content.decode("utf-8-sig")))
    df["學年度"] = year  # 確保每筆都有學年度（早年欄位沒這欄）
    return df


def fetch_all(years: list[int] = YEARS) -> pd.DataFrame:
    parts = []
    for y in years:
        df = fetch_year(y)
        parts.append(df)
        print(f"  {y} 學年度: {df.shape}")
    return pd.concat(parts, ignore_index=True, sort=False)


# ---------------------------------------------------------------------------
# 2. CLEAN — observation-driven fixes
# ---------------------------------------------------------------------------
def clean(df: pd.DataFrame) -> pd.DataFrame:
    """整理欄位、轉型、處理缺值。

    觀察 → 動作 → 代價
    ----------------------------------------------------
    1. 縣市名稱欄位是 "30 臺北市" 這種 "代碼 + 名稱" 格式
       → 用 str.extract 拆出 city_name；代價：若格式不一致會 NaN。
    2. 「總計」是 numeric 但有些年度被讀成 object (含逗號/空白)
       → pd.to_numeric(errors="coerce")。代價：少數無法解析的列變 NaN。
    3. 「體系別」欄位 105–106 學年沒有 → 填 "未分類"。
    4. 學校代碼為 0001、0002 ...，是 string → 保留 as-is。
    """
    df = df.copy()

    # 統一縣市名稱：把 "30 臺北市" 拆成 "臺北市"
    if "縣市名稱" in df.columns:
        df["city_name"] = (df["縣市名稱"].astype(str)
                                          .str.extract(r"(?:\d+\s*)?(\S+)$")[0])
    else:
        df["city_name"] = pd.NA

    # 體系別 (一般 / 技職)
    if "體系別" in df.columns:
        df["system"] = (df["體系別"].astype(str)
                                      .str.replace(r"^\d+\s*", "", regex=True))
        df["system"] = df["system"].replace({"nan": "未分類"}).fillna("未分類")
    else:
        df["system"] = "未分類"

    # 把「總計」與「男生計/女生計」轉成 numeric
    for col in ("總計", "男生計", "女生計"):
        if col in df.columns:
            df[col] = pd.to_numeric(
                df[col].astype(str).str.replace(",", "", regex=False),
                errors="coerce",
            )

    # 105–106 學年度沒有「總計」欄,需要從各年級男/女欄位加總補上。
    # concat 之後「總計」欄存在 (107+ 有),只有 105/106 列是 NaN,
    # 所以用 row-wise fillna,只填 NaN 列,不覆寫 107+ 已公布的值。
    grade_cols = [c for c in df.columns
                  if c.endswith(("年級男生", "年級女生", "延修生男生", "延修生女生"))]
    if grade_cols:
        for c in grade_cols:
            df[c] = pd.to_numeric(
                df[c].astype(str).str.replace(",", "", regex=False),
                errors="coerce",
            )
        fallback_total = df[grade_cols].sum(axis=1, skipna=True)
        if "總計" in df.columns:
            df["總計"] = df["總計"].fillna(fallback_total)
        else:
            df["總計"] = fallback_total

    # 公立 / 私立 — 從學校名稱判斷；軍警校院需要額外 rule。
    df["sector"] = df["學校名稱"].astype(str).apply(
        lambda s: "公立" if s.startswith(("國立", "市立", "省立", "國防", "警察")) else "私立"
    )

    # 等級別清理：去掉前綴 "D " / "B " 等代碼，只留「博士/碩士/學士/...」
    if "等級別" in df.columns:
        df["degree"] = (df["等級別"].astype(str)
                                      .str.replace(r"^[A-Z]\s*", "", regex=True))

    # 日夜間別
    if "日間∕進修別" in df.columns:
        df["schedule"] = (df["日間∕進修別"].astype(str)
                                              .str.replace(r"^[A-Z]\s*", "", regex=True))

    return df


# ---------------------------------------------------------------------------
# 3. DESCRIBE
# ---------------------------------------------------------------------------
def describe(df: pd.DataFrame) -> None:
    print(f"\n  n rows         : {len(df)}")
    print(f"  學年度 range   : {df['學年度'].min()} → {df['學年度'].max()}")
    print(f"  unique schools : {df['學校名稱'].nunique()}")
    print(f"  unique cities  : {df['city_name'].nunique()}")
    print(f"  總計 (M / SD)  : {df['總計'].mean():.0f}  /  {df['總計'].std():.0f}")
    print(f"  缺值 in 總計   : {df['總計'].isna().sum()}")
    print("\n  Top 5 學校 by 平均學生數:")
    top = (df.groupby("學校名稱")["總計"].mean()
                  .sort_values(ascending=False).head())
    print(top.to_string())


# ---------------------------------------------------------------------------
# 4. ANALYSE / VISUALISE
# ---------------------------------------------------------------------------
def plot_total_over_years(df: pd.DataFrame):
    """Line chart — 每年總學生數，附少子化政策關鍵年的 annotation。"""
    agg = (df.groupby("學年度")["總計"].sum().reset_index())
    fig = px.line(
        agg, x="學年度", y="總計", markers=True,
        title="台灣大專校院總學生數 — 105–113 學年度",
        labels={"學年度": "Academic year", "總計": "Total students"},
        color_discrete_sequence=["#3b82f6"],
    )
    # Annotation: 105 學年度起，18 歲人口進入少子化骨牌效應
    fig.add_annotation(
        x=agg["學年度"].iloc[0], y=agg["總計"].iloc[0],
        text="少子化骨牌效應起點", showarrow=True, arrowhead=2,
        bgcolor="rgba(255,255,255,0.9)", bordercolor="orange",
    )
    fig.update_layout(hovermode="x unified")
    return fig


def plot_public_vs_private(df: pd.DataFrame):
    """Stacked bar — 公私立逐年比較。"""
    agg = (df.groupby(["學年度", "sector"])["總計"].sum().reset_index())
    fig = px.bar(
        agg, x="學年度", y="總計", color="sector", barmode="stack",
        title="公立 vs. 私立 大專學生數變化",
        labels={"學年度": "Academic year", "總計": "Total students", "sector": "Sector"},
        color_discrete_map={"公立": "#1d4ed8", "私立": "#f97316"},
    )
    return fig


def plot_city_distribution(df: pd.DataFrame):
    """Bar chart — 113 學年度各縣市學生數。"""
    latest = df[df["學年度"] == df["學年度"].max()]
    agg = (latest.groupby("city_name")["總計"].sum()
                  .sort_values(ascending=False)
                  .reset_index().head(15))
    fig = px.bar(
        agg, x="總計", y="city_name", orientation="h",
        color="總計", color_continuous_scale="Tealgrn",
        title=f"{df['學年度'].max()} 學年度各縣市大專學生數 (Top 15)",
        labels={"總計": "Total students", "city_name": "City"},
    )
    fig.update_layout(yaxis={"categoryorder": "total ascending"},
                      coloraxis_showscale=False)
    return fig


# ---------------------------------------------------------------------------
# 5. MAIN
# ---------------------------------------------------------------------------
def main():
    print("[1/5] Fetching MOE higher-education stats (105–113 學年度)...")
    df_raw = fetch_all()
    print(f"\n     Combined raw shape: {df_raw.shape}")

    print("\n[2/5] Describe — BEFORE clean")
    # raw 還沒清，先簡單看
    print(f"  columns: {list(df_raw.columns)[:10]}")
    print(f"  dtype of 總計: {df_raw['總計'].dtype if '總計' in df_raw.columns else 'N/A'}")

    print("\n[3/5] Cleaning...")
    df = clean(df_raw)
    print("\n     Describe — AFTER clean")
    describe(df)

    df.to_csv(OUT_CSV, index=False, encoding="utf-8-sig")
    print(f"\n[4/5] Saved CSV → {OUT_CSV}")

    print("\n[5/5] Generating Plotly figures...")
    fig1 = plot_total_over_years(df)
    fig2 = plot_public_vs_private(df)
    fig3 = plot_city_distribution(df)
    fig1.show()
    fig2.show()
    fig3.show()
    print("\nDone.")


if __name__ == "__main__":
    main()
