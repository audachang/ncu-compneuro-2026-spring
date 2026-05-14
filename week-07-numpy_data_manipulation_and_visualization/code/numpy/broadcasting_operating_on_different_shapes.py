"""Week 07 · numpy — Broadcasting — Operating on Different Shapes

Extracted from: week-07-numpy_and_data_manipulation.md
"""

import numpy as np

rts = np.array([[320, 415, 280],    # subject 1: 3 trials
                [390, 425, 310]])   # subject 2: 3 trials
                                    # shape: (2, 3)

baseline = np.array([350, 400, 290])  # per-trial baseline, shape: (3,)

# Broadcasting: baseline stretches to match rts rows
centered = rts - baseline
# centered[0] = [320-350, 415-400, 280-290] = [-30, 15, -10]
# centered[1] = [390-350, 425-400, 310-290] = [40, 25, 20]

print("RTs:\n", rts)
print("Baseline:", baseline)
print("Centered:\n", centered)
