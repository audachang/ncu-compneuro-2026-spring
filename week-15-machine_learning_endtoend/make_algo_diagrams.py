"""Generate 5 algorithm intuition diagrams for Week 15 slides.

Each PNG is ~6 in wide x 2.2 in tall (matches the slot reserved below the
code block in the corresponding algorithm slide).

Output: diagrams/algo_linear.png, algo_knn.png, algo_tree.png,
        algo_ensemble.png, algo_kernel.png

Run:
    python make_algo_diagrams.py
"""
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

OUT_DIR = Path("diagrams")
OUT_DIR.mkdir(exist_ok=True)

# Match slide palette
TEAL = "#0D9B9B"
NAVY = "#14325C"
ORANGE = "#F97116"
GREEN = "#2E8B57"
RED = "#D34F4F"
AMBER = "#E8A12A"
LIGHT = "#F7F8FA"
MUTED = "#5F6B83"

FIG_SIZE = (6.0, 2.2)
DPI = 160


def _frame(ax):
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color(MUTED)
    ax.spines["bottom"].set_color(MUTED)
    ax.tick_params(colors=MUTED, labelsize=8)


# ============================================================
# 1. Linear regression — scatter + fitted line
# ============================================================
def diagram_linear():
    rng = np.random.default_rng(42)
    x = np.linspace(0, 10, 30)
    y = 1.5 * x + 2 + rng.normal(0, 1.2, x.size)

    fig, ax = plt.subplots(figsize=FIG_SIZE, dpi=DPI)
    ax.scatter(x, y, s=22, color=NAVY, alpha=0.7, label="data")

    # Fitted line
    w, b = np.polyfit(x, y, 1)
    xs = np.array([x.min(), x.max()])
    ax.plot(xs, w * xs + b, color=TEAL, linewidth=2.2,
            label=f"y = {w:.2f}·x + {b:.2f}")

    # Residual lines for a few points
    for xi, yi in zip(x[::6], y[::6]):
        yp = w * xi + b
        ax.plot([xi, xi], [yi, yp], color=AMBER, linewidth=0.8, alpha=0.6)

    ax.set_xlabel("feature x", fontsize=9, color=MUTED)
    ax.set_ylabel("target y", fontsize=9, color=MUTED)
    ax.legend(fontsize=8, frameon=False, loc="upper left")
    _frame(ax)
    ax.set_title("Fit a straight line that minimises squared residuals",
                 fontsize=10, color=NAVY, pad=4)
    plt.tight_layout()
    plt.savefig(OUT_DIR / "algo_linear.png", bbox_inches="tight")
    plt.close()


# ============================================================
# 2. k-NN — query point + 5 nearest neighbours highlighted
# ============================================================
def diagram_knn():
    rng = np.random.default_rng(7)
    n = 40
    X = rng.uniform(0, 10, (n, 2))
    # Two classes by a soft boundary
    cls = (X[:, 0] + X[:, 1] > 10).astype(int)

    query = np.array([5.5, 5.0])
    dists = np.linalg.norm(X - query, axis=1)
    k = 5
    knn_idx = np.argsort(dists)[:k]

    fig, ax = plt.subplots(figsize=FIG_SIZE, dpi=DPI)
    # Plot all points
    colours = np.where(cls == 0, TEAL, ORANGE)
    ax.scatter(X[:, 0], X[:, 1], c=colours, s=30, alpha=0.5,
               edgecolors="white", linewidths=0.5)
    # Highlight kNN
    for i in knn_idx:
        ax.plot([query[0], X[i, 0]], [query[1], X[i, 1]],
                color=MUTED, linewidth=0.8, alpha=0.7, zorder=1)
        ax.scatter(X[i, 0], X[i, 1],
                   facecolor=colours[i], edgecolor=NAVY,
                   linewidth=1.6, s=60, zorder=3)
    # Query point
    ax.scatter(*query, marker="*", s=180, color="black",
               edgecolor="white", linewidth=1.4, zorder=5)
    ax.text(query[0] + 0.2, query[1] + 0.3, "? new sample",
            fontsize=9, color="black")

    # Circle around k nearest
    max_d = dists[knn_idx].max()
    circle = plt.Circle(query, max_d, color=MUTED,
                        fill=False, linestyle="--", linewidth=1)
    ax.add_artist(circle)

    legend_h = [
        mpatches.Patch(color=TEAL, label="class A"),
        mpatches.Patch(color=ORANGE, label="class B"),
    ]
    ax.legend(handles=legend_h, fontsize=8, frameon=False, loc="upper left")
    ax.set_xlim(0, 10); ax.set_ylim(0, 10)
    ax.set_xlabel("feature 1", fontsize=9, color=MUTED)
    ax.set_ylabel("feature 2", fontsize=9, color=MUTED)
    _frame(ax)
    ax.set_title(f"Find k={k} nearest neighbours, vote by majority",
                 fontsize=10, color=NAVY, pad=4)
    plt.tight_layout()
    plt.savefig(OUT_DIR / "algo_knn.png", bbox_inches="tight")
    plt.close()


# ============================================================
# 3. Decision Tree — tree on left, axis-aligned partition on right
# ============================================================
def diagram_tree():
    fig, (axT, axP) = plt.subplots(1, 2, figsize=FIG_SIZE, dpi=DPI,
                                   gridspec_kw={"width_ratios": [1, 1]})

    # --- Tree (drawn manually) -----------------------------------------
    def node(ax, x, y, text, fill=NAVY):
        rect = mpatches.FancyBboxPatch(
            (x - 0.35, y - 0.18), 0.7, 0.36,
            boxstyle="round,pad=0.02",
            facecolor=fill, edgecolor="white", linewidth=1,
        )
        ax.add_patch(rect)
        ax.text(x, y, text, ha="center", va="center",
                color="white", fontsize=8, fontweight="bold")

    def edge(ax, x1, y1, x2, y2, label=None):
        ax.plot([x1, x2], [y1 - 0.18, y2 + 0.18],
                color=MUTED, linewidth=1)
        if label:
            ax.text((x1 + x2) / 2 + 0.05, (y1 + y2) / 2,
                    label, fontsize=7, color=MUTED)

    # Level 1
    node(axT, 0.5, 0.85, "age < 50?", fill=NAVY)
    # Level 2
    node(axT, 0.22, 0.50, "income\n< 30k?", fill=TEAL)
    node(axT, 0.78, 0.50, "edu\n> 12y?", fill=TEAL)
    edge(axT, 0.5, 0.85, 0.22, 0.50, "yes")
    edge(axT, 0.5, 0.85, 0.78, 0.50, "no")
    # Leaves
    for x, lab, c in [(0.08, "low", AMBER),
                      (0.36, "med", AMBER),
                      (0.64, "high", GREEN),
                      (0.92, "high", GREEN)]:
        rect = mpatches.FancyBboxPatch(
            (x - 0.10, 0.10), 0.20, 0.16,
            boxstyle="round,pad=0.02",
            facecolor=c, edgecolor="white", linewidth=1,
        )
        axT.add_patch(rect)
        axT.text(x, 0.18, lab, ha="center", va="center",
                 color="white", fontsize=7, fontweight="bold")
    edge(axT, 0.22, 0.50, 0.08, 0.18)
    edge(axT, 0.22, 0.50, 0.36, 0.18)
    edge(axT, 0.78, 0.50, 0.64, 0.18)
    edge(axT, 0.78, 0.50, 0.92, 0.18)

    axT.set_xlim(0, 1); axT.set_ylim(0, 1)
    axT.axis("off")
    axT.set_title("Recursive splits", fontsize=9, color=NAVY)

    # --- Partition ------------------------------------------------------
    # Show 2D feature space cut by axis-aligned rules
    axP.add_patch(mpatches.Rectangle((0, 0.5), 0.5, 0.5,
                                      color=AMBER, alpha=0.5))
    axP.add_patch(mpatches.Rectangle((0, 0), 0.5, 0.5,
                                      color=AMBER, alpha=0.85))
    axP.add_patch(mpatches.Rectangle((0.5, 0), 1.0, 0.6,
                                      color=GREEN, alpha=0.5))
    axP.add_patch(mpatches.Rectangle((0.5, 0.6), 1.0, 0.4,
                                      color=GREEN, alpha=0.85))
    # Split lines
    axP.plot([0.5, 0.5], [0, 1], color="white", linewidth=1.6)
    axP.plot([0, 0.5], [0.5, 0.5], color="white", linewidth=1.6)
    axP.plot([0.5, 1.0], [0.6, 0.6], color="white", linewidth=1.6)

    axP.set_xlim(0, 1); axP.set_ylim(0, 1)
    axP.set_xlabel("age", fontsize=9, color=MUTED)
    axP.set_ylabel("income / edu", fontsize=9, color=MUTED)
    axP.set_xticks([]); axP.set_yticks([])
    _frame(axP)
    axP.set_title("→ Axis-aligned partition of feature space",
                  fontsize=9, color=NAVY)

    plt.tight_layout()
    plt.savefig(OUT_DIR / "algo_tree.png", bbox_inches="tight")
    plt.close()


# ============================================================
# 4. Ensemble — 5 small trees + arrow + average
# ============================================================
def diagram_ensemble():
    fig, ax = plt.subplots(figsize=FIG_SIZE, dpi=DPI)

    # Draw 5 simple "trees" (just sketches)
    n_trees = 5
    tree_w = 0.10
    gap = 0.04
    total_w = n_trees * tree_w + (n_trees - 1) * gap
    start = 0.05
    rng = np.random.default_rng(2)

    def mini_tree(ax, x0, y0, w, h, seed):
        rr = np.random.default_rng(seed)
        # root
        ax.plot([x0 + w/2, x0 + w*0.25], [y0 + h, y0 + h*0.55],
                color=NAVY, linewidth=1)
        ax.plot([x0 + w/2, x0 + w*0.75], [y0 + h, y0 + h*0.55],
                color=NAVY, linewidth=1)
        # left child
        ax.plot([x0 + w*0.25, x0 + w*0.10], [y0 + h*0.55, y0 + h*0.10],
                color=NAVY, linewidth=1)
        ax.plot([x0 + w*0.25, x0 + w*0.40], [y0 + h*0.55, y0 + h*0.10],
                color=NAVY, linewidth=1)
        # right child
        ax.plot([x0 + w*0.75, x0 + w*0.60], [y0 + h*0.55, y0 + h*0.10],
                color=NAVY, linewidth=1)
        ax.plot([x0 + w*0.75, x0 + w*0.90], [y0 + h*0.55, y0 + h*0.10],
                color=NAVY, linewidth=1)
        # leaves
        for lx in [0.10, 0.40, 0.60, 0.90]:
            jitter = rr.normal(0, 0.02)
            c = ax.scatter(x0 + w*lx, y0 + h*0.10 + jitter,
                           s=40, color=TEAL, zorder=3,
                           edgecolor="white", linewidth=0.6)
        # root node circle
        ax.scatter(x0 + w/2, y0 + h, s=60, color=NAVY,
                   edgecolor="white", linewidth=0.8, zorder=3)

    for i in range(n_trees):
        x0 = start + i * (tree_w + gap)
        mini_tree(ax, x0, 0.30, tree_w, 0.55, seed=i)
        ax.text(x0 + tree_w/2, 0.20, f"tree {i+1}",
                ha="center", fontsize=7, color=MUTED)

    # Arrow → average
    arr_x0 = start + total_w + 0.02
    ax.annotate("", xy=(arr_x0 + 0.10, 0.55),
                xytext=(arr_x0, 0.55),
                arrowprops=dict(arrowstyle="->", lw=2, color=AMBER))
    ax.text(arr_x0 + 0.05, 0.65, "average\n(or vote)",
            ha="center", fontsize=8, color=AMBER, fontweight="bold")

    # Final prediction box
    final_rect = mpatches.FancyBboxPatch(
        (arr_x0 + 0.13, 0.40), 0.20, 0.30,
        boxstyle="round,pad=0.02",
        facecolor=GREEN, edgecolor="white", linewidth=1,
    )
    ax.add_patch(final_rect)
    ax.text(arr_x0 + 0.23, 0.55, "ŷ",
            ha="center", va="center", color="white",
            fontsize=14, fontweight="bold")
    ax.text(arr_x0 + 0.23, 0.32, "final\nprediction",
            ha="center", fontsize=7, color=MUTED)

    ax.set_xlim(0, 1); ax.set_ylim(0, 1)
    ax.axis("off")
    ax.set_title("Bagging: many high-variance trees → averaged → low variance",
                 fontsize=10, color=NAVY, pad=4)
    plt.tight_layout()
    plt.savefig(OUT_DIR / "algo_ensemble.png", bbox_inches="tight")
    plt.close()


# ============================================================
# 5. Kernel SVM — non-separable in 1D → separable after RBF lift
# ============================================================
def diagram_kernel():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=FIG_SIZE, dpi=DPI,
                                   gridspec_kw={"width_ratios": [1, 1.1]})

    # --- Left: 1D not linearly separable ---
    rng = np.random.default_rng(11)
    n = 20
    # Class A in the middle, class B on both sides
    a_x = rng.uniform(-1, 1, n)
    b_x = np.concatenate([rng.uniform(-3, -1.5, n // 2),
                          rng.uniform(1.5, 3, n // 2)])
    ax1.scatter(a_x, np.zeros_like(a_x), color=TEAL, s=40,
                edgecolor="white", linewidth=0.6, label="class A")
    ax1.scatter(b_x, np.zeros_like(b_x), color=ORANGE, s=40,
                edgecolor="white", linewidth=0.6, label="class B")
    ax1.axhline(0, color=MUTED, linewidth=0.6)
    ax1.set_xlim(-4, 4); ax1.set_ylim(-1, 1)
    ax1.set_yticks([])
    ax1.set_xlabel("feature x  (1-D)", fontsize=9, color=MUTED)
    ax1.legend(fontsize=7, frameon=False, loc="upper center",
               ncol=2, bbox_to_anchor=(0.5, 1.15))
    ax1.set_title("Not linearly separable in 1D",
                  fontsize=9, color=NAVY, pad=14)
    _frame(ax1)
    ax1.text(0, -0.7, "no straight line works",
             ha="center", color=RED, fontsize=8, fontweight="bold")

    # Arrow between panels
    fig.text(0.50, 0.50, "RBF\nkernel\n→", ha="center", va="center",
             fontsize=9, color=AMBER, fontweight="bold")

    # --- Right: lifted to 2D with phi(x) = (x, x^2), separable ---
    a_x2 = a_x
    a_y2 = a_x2 ** 2
    b_x2 = b_x
    b_y2 = b_x2 ** 2
    ax2.scatter(a_x2, a_y2, color=TEAL, s=40,
                edgecolor="white", linewidth=0.6)
    ax2.scatter(b_x2, b_y2, color=ORANGE, s=40,
                edgecolor="white", linewidth=0.6)
    # Separating hyperplane (horizontal line)
    ax2.axhline(1.3, color=GREEN, linewidth=2.0, linestyle="--",
                label="hyperplane")
    ax2.set_xlabel("x", fontsize=9, color=MUTED)
    ax2.set_ylabel("φ(x) = x²", fontsize=9, color=MUTED)
    ax2.legend(fontsize=7, frameon=False, loc="upper right")
    ax2.set_title("Linearly separable after lift",
                  fontsize=9, color=NAVY, pad=14)
    _frame(ax2)

    plt.tight_layout()
    plt.savefig(OUT_DIR / "algo_kernel.png", bbox_inches="tight")
    plt.close()


def main():
    diagram_linear()
    diagram_knn()
    diagram_tree()
    diagram_ensemble()
    diagram_kernel()
    print("Wrote 5 diagrams to", OUT_DIR.resolve())


if __name__ == "__main__":
    main()
