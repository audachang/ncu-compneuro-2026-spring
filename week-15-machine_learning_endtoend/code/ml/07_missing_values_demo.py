"""Week 15 - Missing values teaching demo.

Generates a synthetic cogneuro dataset (60 subjects x 10 columns) that
intentionally contains three contrasting missing-value patterns, so
students can immediately see when to drop rows vs. drop columns vs. impute.

Scenario:
    A lab collected behavioral scores from 60 subjects across multiple
    cognitive tasks plus two physiological measures.

    - stroop_rt, flanker_rt, nback_acc, wm_span : standard tasks, mostly complete
    - hrv_lf_hf : added a piece of equipment that only arrived halfway through
                  ~75% missing (NOT MAR - it's missing by design / batch)
    - skin_conductance : a single bad sensor day - entire column may be unusable
    - 3 subjects had an experimental abort - most rows missing for those subjects

Run:
    python 07_missing_values_demo.py            # prints summary to stdout
    python 07_missing_values_demo.py --csv      # also writes missing_demo.csv
    python 07_missing_values_demo.py --plot     # writes missing_demo.png
"""
from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import pandas as pd


# ---------------------------------------------------------------------------
# Synthetic data generator
# ---------------------------------------------------------------------------
def make_demo_dataset(n_subjects: int = 60, seed: int = 42) -> pd.DataFrame:
    """Build a 60x10 cogneuro dataset with three contrasting missingness patterns."""
    rng = np.random.default_rng(seed)

    sid = np.arange(1, n_subjects + 1)
    age = rng.integers(20, 75, size=n_subjects).astype(float)
    group = np.where(age < 45, "young", "older")

    stroop_rt = rng.normal(520, 60, n_subjects)
    flanker_rt = rng.normal(490, 55, n_subjects)
    nback_acc = np.clip(rng.normal(0.82, 0.08, n_subjects), 0, 1)
    wm_span = rng.integers(3, 8, n_subjects).astype(float)

    # HRV equipment arrived around subject 45 - ~75% missing.
    hrv_lf_hf = rng.normal(2.1, 0.6, n_subjects)
    hrv_lf_hf[sid < 45] = np.nan

    # Skin conductance sensor failed - 85% missing.
    skin_cond = rng.normal(8.0, 1.5, n_subjects)
    sc_mask = rng.random(n_subjects) < 0.85
    skin_cond[sc_mask] = np.nan

    composite_score = (
        0.4 * (1000 - stroop_rt) / 10
        + 0.3 * (1000 - flanker_rt) / 10
        + 0.2 * nback_acc * 100
        + 0.1 * wm_span * 10
        + rng.normal(0, 5, n_subjects)
    )

    df = pd.DataFrame({
        "subject_id": sid,
        "age": age,
        "group": group,
        "stroop_rt": stroop_rt,
        "flanker_rt": flanker_rt,
        "nback_acc": nback_acc,
        "wm_span": wm_span,
        "hrv_lf_hf": hrv_lf_hf,
        "skin_conductance": skin_cond,
        "composite_score": composite_score,
    })

    # 3 subjects aborted partway through - scatter missing across behavioral cols
    abort_subjects = rng.choice(sid, size=3, replace=False)
    abort_cols = ["stroop_rt", "flanker_rt", "nback_acc",
                  "wm_span", "composite_score"]
    for s in abort_subjects:
        n_drop = int(rng.integers(3, 6))
        missing_cols = rng.choice(abort_cols, size=n_drop, replace=False)
        df.loc[df["subject_id"] == s, missing_cols] = np.nan

    # ~5% scattered missing in one important behavioral column
    sporadic_idx = rng.choice(n_subjects, size=3, replace=False)
    df.loc[sporadic_idx, "stroop_rt"] = np.nan

    return df


# ---------------------------------------------------------------------------
# Missingness summary
# ---------------------------------------------------------------------------
def summarize_missing(df: pd.DataFrame) -> pd.DataFrame:
    out = pd.DataFrame({
        "n_missing": df.isna().sum(),
        "pct_missing": (df.isna().mean() * 100).round(1),
    }).sort_values("pct_missing", ascending=False)
    return out


def recommend_strategy(pct: float, n_rows_lost: int, n_total: int) -> str:
    if pct >= 60:
        return "-> DROP COLUMN  (too much missing to impute reliably)"
    if pct >= 20:
        return "-> IMPUTE       (consider domain-aware imputation)"
    if 0 < pct and n_rows_lost <= 0.05 * n_total:
        return "-> DROP ROWS    (small loss; safest)"
    if pct > 0:
        return "-> IMPUTE       (rows are too valuable to drop)"
    return "-> KEEP AS-IS"


def report(df: pd.DataFrame) -> None:
    n = len(df)
    print(f"\nDataset: {n} subjects x {df.shape[1]} columns\n")
    summary = summarize_missing(df)
    print("=" * 68)
    print(f"{'Column':<22} {'n_missing':>10} {'pct':>7}   Recommendation")
    print("-" * 68)
    for col, row in summary.iterrows():
        if row["n_missing"] == 0:
            rec = "-> KEEP AS-IS"
        else:
            n_rows_lost = int(row["n_missing"])
            rec = recommend_strategy(row["pct_missing"], n_rows_lost, n)
        print(f"{col:<22} {int(row['n_missing']):>10} {row['pct_missing']:>6.1f}%   {rec}")
    print("=" * 68)

    print("\nIf you naively dropna() across ALL columns:")
    n_after = len(df.dropna())
    verdict = "OK" if n_after >= 0.7 * n else "BAD - most data lost"
    print(f"  rows kept = {n_after}/{n}  ({n_after/n:.1%})  -> {verdict}")

    sparse_cols = summary[summary["pct_missing"] >= 60].index.tolist()
    if sparse_cols:
        print(f"\nIf you DROP the sparse columns {sparse_cols} first, then dropna():")
        n_after2 = len(df.drop(columns=sparse_cols).dropna())
        print(f"  rows kept = {n_after2}/{n}  ({n_after2/n:.1%})  "
              f"-> much better, but loses the {sparse_cols} information")

    print("\nThe RIGHT answer is usually mixed:")
    print("  - drop columns where missing >> 60%")
    print("  - impute columns where 5% < missing < 60% (use Pipeline!)")
    print("  - drop rows where only a few are affected AND data is cheap")


# ---------------------------------------------------------------------------
# Visualization
# ---------------------------------------------------------------------------
def plot_missing_matrix(df: pd.DataFrame, out: Path = Path("missing_demo.png")) -> None:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.patches import Patch

    cols = [c for c in df.columns if c != "subject_id"]
    M = df[cols].isna().to_numpy().astype(float)
    pcts = (df[cols].isna().mean() * 100).to_numpy()

    fig, (ax_top, ax) = plt.subplots(
        2, 1, figsize=(11, 8),
        gridspec_kw={"height_ratios": [1, 7], "hspace": 0.05},
        sharex=True,
    )

    # Color by missingness severity
    def color_for(p):
        if p > 60: return "#c0392b"   # red - drop column
        if p > 20: return "#e67e22"   # orange - impute
        if p > 0:  return "#2980b9"   # blue - drop rows or impute
        return "#bbbbbb"              # complete

    bar_colors = [color_for(p) for p in pcts]

    # --- Top: bar of % missing ----------------------------------------------
    ax_top.bar(range(len(cols)), pcts, color=bar_colors, edgecolor="white")
    ax_top.set_ylim(0, 105)
    ax_top.set_ylabel("% missing", fontsize=10)
    ax_top.set_yticks([0, 25, 50, 75, 100])
    ax_top.spines["top"].set_visible(False)
    ax_top.spines["right"].set_visible(False)
    for i, p in enumerate(pcts):
        ax_top.text(i, p + 3, f"{p:.0f}%", ha="center", fontsize=9,
                    color=bar_colors[i], fontweight="bold")
    ax_top.axhline(60, color="#c0392b", linestyle=":", linewidth=0.8, alpha=0.5)
    ax_top.axhline(20, color="#e67e22", linestyle=":", linewidth=0.8, alpha=0.5)
    ax_top.set_title("Missing-value matrix  (black = missing)",
                     fontsize=13, pad=10)

    # --- Bottom: matrix -----------------------------------------------------
    ax.imshow(M, aspect="auto", cmap="Greys", interpolation="nearest",
              vmin=0, vmax=1)
    ax.set_xticks(range(len(cols)))
    ax.set_xticklabels(cols, rotation=35, ha="right", fontsize=10)
    ax.set_ylabel("Subject row", fontsize=10)

    # --- Legend below the figure --------------------------------------------
    legend_elems = [
        Patch(facecolor="#c0392b", label=">60% missing  ->  drop column"),
        Patch(facecolor="#e67e22", label="20-60% missing  ->  impute"),
        Patch(facecolor="#2980b9", label="<20% missing  ->  drop rows / impute"),
        Patch(facecolor="#bbbbbb", label="complete"),
    ]
    fig.legend(handles=legend_elems, loc="lower center",
               bbox_to_anchor=(0.5, -0.02), ncol=4,
               frameon=False, fontsize=9)

    plt.savefig(out, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"\nSaved {out}")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------
def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--csv", action="store_true")
    parser.add_argument("--plot", action="store_true")
    args = parser.parse_args()

    df = make_demo_dataset()
    report(df)

    if args.csv:
        df.to_csv("missing_demo.csv", index=False)
        print("\nSaved missing_demo.csv")
    if args.plot:
        plot_missing_matrix(df)


if __name__ == "__main__":
    main()

    plt.savefig(out, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"\nSaved {out}")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------
def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--csv", action="store_true")
    parser.add_argument("--plot", action="store_true")
    args = parser.parse_args()

    df = make_demo_dataset()
    report(df)

    if args.csv:
        df.to_csv("missing_demo.csv", index=False)
        print("\nSaved missing_demo.csv")
    if args.plot:
        plot_missing_matrix(df)


if __name__ == "__main__":
    main()
