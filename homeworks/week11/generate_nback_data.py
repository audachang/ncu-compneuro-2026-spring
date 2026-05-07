"""Generate a synthetic N-back working memory dataset for the Week 11 homework.

Resembles a typical lifespan working-memory study where participants complete
1-back, 2-back, and 3-back tasks. Three condition rows per participant.

Output (writes to BOTH starter/data/ and solution/data/):
    nback_working_memory.csv

Schema
------
participant_id : str   "P001"–"P200"
age            : int   18–75
sex            : "F" / "M"
education      : int   years (9–22)
group          : "young" (18–34) / "middle" (35–54) / "older" (55–75)
condition      : "1-back" / "2-back" / "3-back"
n_trials       : int   typically 80
accuracy       : float 0–1
mean_rt_ms     : float ms (correct trials)
d_prime        : float signal-detection sensitivity
"""

from pathlib import Path

import numpy as np
import pandas as pd

OUT_NAMES = [
    Path(__file__).parent / "starter" / "data" / "nback_working_memory.csv",
    Path(__file__).parent / "solution" / "data" / "nback_working_memory.csv",
]
N_PART = 200
SEED = 11


def simulate_nback(n: int = N_PART, seed: int = SEED) -> pd.DataFrame:
    rng = np.random.default_rng(seed)

    age = rng.integers(18, 76, size=n)
    sex = rng.choice(["F", "M"], size=n, p=[0.55, 0.45])
    education = np.clip(rng.normal(15, 3, n).round().astype(int), 9, 22)

    rows = []
    # Condition-specific baselines
    cond_params = {
        "1-back": {"acc0": 0.95, "rt0": 480, "dp0": 3.2},
        "2-back": {"acc0": 0.85, "rt0": 620, "dp0": 2.4},
        "3-back": {"acc0": 0.72, "rt0": 760, "dp0": 1.6},
    }
    for i in range(n):
        a = age[i]
        edu = education[i]
        # Age-related load: every year above 25 reduces accuracy/d', slows RT
        age_load = max(a - 25, 0)
        # Education adds small reserve effect
        edu_boost = (edu - 12) * 0.01

        for cond, params in cond_params.items():
            # Higher load (3-back) → larger age effect
            load_mult = {"1-back": 0.6, "2-back": 1.0, "3-back": 1.6}[cond]

            acc = params["acc0"] - 0.0035 * age_load * load_mult + edu_boost \
                  + rng.normal(0, 0.04)
            acc = float(np.clip(acc, 0.30, 1.0))

            rt = params["rt0"] + 4.2 * age_load * load_mult \
                 + rng.normal(0, 45)
            rt = float(np.clip(rt, 250, None))

            dp = params["dp0"] - 0.012 * age_load * load_mult + edu_boost * 4 \
                 + rng.normal(0, 0.25)
            dp = float(np.clip(dp, 0, 5))

            rows.append({
                "participant_id":  f"P{i+1:03d}",
                "age":             int(a),
                "sex":             str(sex[i]),
                "education":       int(edu),
                "group":           ("young" if a < 35 else
                                    "middle" if a < 55 else "older"),
                "condition":       cond,
                "n_trials":        80,
                "accuracy":        round(acc, 3),
                "mean_rt_ms":      round(rt, 1),
                "d_prime":         round(dp, 2),
            })

    df = pd.DataFrame(rows)
    return df.sort_values(["participant_id", "condition"]).reset_index(drop=True)


if __name__ == "__main__":
    df = simulate_nback()
    for path in OUT_NAMES:
        path.parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(path, index=False)
        print(f"Wrote {len(df)} rows to {path}")

    print("\nSummary by condition × group:")
    print(df.groupby(["condition", "group"], observed=True)[
        ["accuracy", "mean_rt_ms", "d_prime"]
    ].mean().round(2))
