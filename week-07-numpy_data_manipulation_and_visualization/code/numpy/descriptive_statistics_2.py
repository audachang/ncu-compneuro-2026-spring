"""Week 07 · numpy — Descriptive Statistics: Axis-wise Aggregation

Extracted from: week-07-numpy_and_data_manipulation.md
"""

import numpy as np

# Shape (3 subjects × 10 trials)
rng = np.random.default_rng(42)
data = rng.normal(400, 80, size=(3, 10))

per_subject = data.mean(axis=1)   # mean RT per subject (3 values)
per_trial   = data.mean(axis=0)   # mean RT per trial position (10 values)

print("Mean RT per subject:", per_subject.round(1))
print("Mean RT per trial  :", per_trial.round(1))
