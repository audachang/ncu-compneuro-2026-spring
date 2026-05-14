"""Generate a synthetic cognitive aging dataset for the Week 11 Streamlit demo.

Resembles a typical lifespan cognitive battery study (e.g., Cambridge Brain
Sciences online battery, Taiwan Biobank cognitive subscale). All values are
synthetic but follow plausible age-related patterns reported in the
literature (Salthouse, 2010; Hartshorne & Germine, 2015).

Output: data/cognitive_aging_taiwan.csv

Columns
-------
subject_id   : str, "S001"–"S400"
age          : int, 20–80
sex          : "F" / "M"
education    : int, years of formal education (9–22)
group        : "young" (20–39) / "middle" (40–59) / "older" (60–80)
reaction_time_ms     : float, simple RT task (lower = faster)
working_memory_span  : int, n-back / digit span score (higher = better)
processing_speed     : float, digit-symbol substitution (items / 90 s, higher = better)
moca_score           : int, Montreal Cognitive Assessment (0–30, higher = better)
stroop_interference_ms : float, incongruent − congruent RT (lower = less interference)
"""

from pathlib import Path

import numpy as np
import pandas as pd

OUT_PATH = Path(__file__).parent / "data" / "cognitive_aging_taiwan.csv"
N = 400
SEED = 42


def simulate_cognitive_aging(n: int = N, seed: int = SEED) -> pd.DataFrame:
    rng = np.random.default_rng(seed)

    # Demographics
    age = rng.integers(20, 81, size=n)
    sex = rng.choice(["F", "M"], size=n, p=[0.55, 0.45])
    education = np.clip(rng.normal(15, 3, n).round().astype(int), 9, 22)

    # Age-related slowing of RT: ~2 ms per year above 20, plus noise
    reaction_time_ms = 320 + 2.0 * (age - 20) + rng.normal(0, 35, n)

    # Working memory: peaks ~25, declines after 30
    wm_span = 7.5 - 0.04 * np.maximum(age - 25, 0) + rng.normal(0, 0.9, n)
    working_memory_span = np.clip(wm_span.round().astype(int), 2, 9)

    # Processing speed: classic linear decline
    processing_speed = 60 - 0.35 * (age - 20) + rng.normal(0, 6, n)
    processing_speed = np.clip(processing_speed, 15, None)

    # MoCA: ceiling effects at young, mild decline late life
    moca = 29.5 - 0.05 * np.maximum(age - 60, 0) + rng.normal(0, 1.2, n)
    moca_score = np.clip(moca.round().astype(int), 18, 30)

    # Stroop interference: increases with age
    stroop = 60 + 1.2 * (age - 20) + rng.normal(0, 18, n)

    # Education effect: more years → slightly better cognition (proxy for cognitive reserve)
    edu_boost = (education - 12) * 0.5
    working_memory_span = np.clip(
        (wm_span + 0.1 * (education - 12)).round().astype(int), 2, 9
    )
    moca_score = np.clip(
        (moca + 0.15 * (education - 12)).round().astype(int), 18, 30
    )

    # Group assignment
    group = pd.cut(age, bins=[19, 39, 59, 80], labels=["young", "middle", "older"])

    df = pd.DataFrame({
        "subject_id":             [f"S{i:03d}" for i in range(1, n + 1)],
        "age":                    age,
        "sex":                    sex,
        "education":              education,
        "group":                  group.astype(str),
        "reaction_time_ms":       reaction_time_ms.round(1),
        "working_memory_span":    working_memory_span,
        "processing_speed":       processing_speed.round(1),
        "moca_score":             moca_score,
        "stroop_interference_ms": stroop.round(1),
    })
    return df.sort_values("subject_id").reset_index(drop=True)


if __name__ == "__main__":
    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    df = simulate_cognitive_aging()
    df.to_csv(OUT_PATH, index=False)
    print(f"Wrote {len(df)} rows to {OUT_PATH}")
    print(df.head())
    print("\n--- Summary by group ---")
    print(df.groupby("group", observed=True)[
        ["reaction_time_ms", "working_memory_span", "moca_score"]
    ].mean().round(1))
