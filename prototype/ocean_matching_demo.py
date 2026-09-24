"""Explanatory diagram of Hi-Five's matching pipeline as designed at the
hackathon. No synthetic data, no invented metrics — this draws the flow
and the real scoring formula from src/server/neo4j_db/relationship_scoring.py
(generate_relationship_score): 0.6 * vector_similarity + 0.4 * tag_jaccard.
"""
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch

FIGURES_DIR = os.path.join(os.path.dirname(__file__), "figures")

INK = "#282215"
EDGE = "#c6b99f"
BLUE = "#3b42db"
ORANGE = "#e85b30"
RUST = "#c2491d"
PURPLE = "#6f2f96"


def box(ax, xy, w, h, text, edgecolor=INK, facecolor="#eae4d6", fontsize=9.5, weight="medium"):
    x, y = xy
    patch = FancyBboxPatch(
        (x, y), w, h,
        boxstyle="square,pad=0.02",
        linewidth=1.3,
        edgecolor=edgecolor,
        facecolor=facecolor,
        zorder=2,
    )
    ax.add_patch(patch)
    ax.text(
        x + w / 2, y + h / 2, text,
        ha="center", va="center", fontsize=fontsize, color=INK,
        weight=weight, zorder=3, linespacing=1.4,
    )
    return patch


def arrow(ax, start, end, color=INK, style="-|>", lw=1.5, connectionstyle=None):
    patch = FancyArrowPatch(
        start, end,
        arrowstyle=style, mutation_scale=14,
        color=color, linewidth=lw, zorder=2,
        connectionstyle=connectionstyle,
        shrinkA=2, shrinkB=2,
    )
    ax.add_patch(patch)


def plot_matching_flow(path):
    fig, ax = plt.subplots(figsize=(11, 7.5))
    ax.set_xlim(0, 11)
    ax.set_ylim(0, 8)
    ax.axis("off")

    ax.set_title(
        "Hi-Five matching pipeline — flow as designed at the hackathon",
        fontsize=13, weight="medium", loc="left",
    )
    ax.text(
        0, 7.55, "concept sketch — describes the intended flow, not a measured run",
        fontsize=8.5, color=RUST, style="italic",
    )

    # Stage 1: inputs
    box(ax, (0.2, 5.9), 2.6, 1.1, "OCEAN assessment\n(free-text answers)", edgecolor=BLUE)
    box(ax, (0.2, 4.4), 2.6, 1.1, "Interest tags\n(picked by user)", edgecolor=PURPLE)

    # Stage 2: embeddings
    box(
        ax, (3.4, 5.9), 2.7, 1.1,
        "Embed per trait:\nBGE-en-icl +\nRoBERTa-go-emotions",
        edgecolor=BLUE,
    )
    arrow(ax, (2.8, 6.45), (3.4, 6.45), color=BLUE)

    # tags flow straight to the score box, bypassing embedding
    arrow(
        ax, (2.8, 4.95), (3.4, 4.95), color=PURPLE,
    )
    box(ax, (3.4, 4.4), 2.7, 1.1, "Tag set\n(unchanged)", edgecolor=PURPLE)

    arrow(ax, (4.75, 5.9), (4.75, 5.5), color=BLUE)

    # Stage 3: score formula
    score_box = box(
        ax, (6.5, 4.6), 4.2, 2.4,
        "",
        edgecolor=INK, facecolor="#f4efe2",
    )
    ax.text(
        6.7, 6.65, "score = 0.6 × vector_similarity", fontsize=10, color=BLUE, weight="medium",
    )
    ax.text(
        6.94, 6.3, "+ 0.4 × tag_jaccard", fontsize=10, color=PURPLE, weight="medium",
    )
    ax.text(
        6.7, 5.85,
        "vector_similarity = mean of cosine sim.\nover the 5 OCEAN trait embeddings",
        fontsize=8.3, color=INK,
    )
    ax.text(
        6.7, 5.15,
        "tag_jaccard = |tags₁ ∩ tags₂| / |tags₁ ∪ tags₂|",
        fontsize=8.3, color=INK,
    )
    ax.text(
        6.7, 4.75,
        "real formula, src/server/neo4j_db/relationship_scoring.py",
        fontsize=7.3, color=RUST, style="italic",
    )

    arrow(ax, (6.1, 6.45), (6.5, 6.1), color=BLUE, connectionstyle="arc3,rad=-0.15")
    arrow(ax, (6.1, 4.95), (6.5, 5.4), color=PURPLE, connectionstyle="arc3,rad=0.15")

    # Stage 4: match -> chat window
    box(ax, (7.0, 3.0), 3.2, 1.0, "Top-ranked match\nsurfaced as a card", edgecolor=INK)
    arrow(ax, (8.6, 4.6), (8.6, 4.0), color=INK)

    box(ax, (7.0, 1.7), 3.2, 1.0, "Both swipe right\n→ chat opens", edgecolor=INK)
    arrow(ax, (8.6, 3.0), (8.6, 2.7), color=INK)

    # 48h timeline
    tl_y = 1.0
    tl_x0, tl_x1 = 0.4, 6.4
    ax.annotate(
        "", xy=(tl_x1, tl_y), xytext=(tl_x0, tl_y),
        arrowprops=dict(arrowstyle="-|>", color=ORANGE, linewidth=2),
    )
    ax.text(tl_x0, tl_y + 0.28, "match made\n(alias only)", fontsize=8.3, ha="left", color=INK)
    ax.text((tl_x0 + tl_x1) / 2, tl_y + 0.28, "48-hour anonymous chat window", fontsize=9, ha="center", color=ORANGE, weight="medium")
    ax.text(tl_x1, tl_y + 0.28, "window closes", fontsize=8.3, ha="right", color=INK)
    for frac in (0.0, 0.5, 1.0):
        xt = tl_x0 + frac * (tl_x1 - tl_x0)
        ax.plot([xt, xt], [tl_y - 0.08, tl_y + 0.08], color=ORANGE, linewidth=1.5)
    arrow(ax, (8.6, 1.7), (8.6, 1.15), color=INK, connectionstyle="arc3,rad=-0.25")

    # decision box, centered below the timeline
    dec_x, dec_y, dec_w, dec_h = (5.5, 0.15, 3.6, 0.85)
    box(ax, (dec_x, dec_y), dec_w, dec_h, "Both opt in to reveal\nbefore the clock runs out?", edgecolor=INK)
    arrow(ax, (dec_x + dec_w / 2, 1.0), (dec_x + dec_w / 2, dec_y + dec_h), color=INK)

    # outcome boxes, stacked below the decision with clear vertical gap
    reveal_x, out_y, out_w, out_h = (0.4, -1.15, 3.0, 0.85)
    dissolve_x = 4.2
    box(ax, (reveal_x, out_y), out_w, out_h, "Identities reveal\n→ permanent friend", edgecolor=BLUE)
    box(ax, (dissolve_x, out_y), out_w, out_h, "Match dissolves\n(stays anonymous)", edgecolor=RUST)

    arrow(
        ax, (dec_x + 0.4, dec_y), (reveal_x + out_w - 0.3, out_y + out_h),
        color=BLUE, connectionstyle="arc3,rad=0.2",
    )
    ax.text(2.9, -0.15, "yes, both", fontsize=7.8, color=BLUE, ha="center")
    arrow(
        ax, (dec_x + dec_w / 2, dec_y), (dissolve_x + out_w / 2, out_y + out_h),
        color=RUST,
    )
    ax.text(dissolve_x + out_w + 0.4, -0.15, "no / timeout", fontsize=7.8, color=RUST, ha="left")

    ax.set_ylim(-1.6, 8.0)

    fig.savefig(path, dpi=200)
    plt.close(fig)


def main():
    os.makedirs(FIGURES_DIR, exist_ok=True)
    plot_matching_flow(os.path.join(FIGURES_DIR, "matching_flow.png"))
    print(f"Wrote 1 figure to {FIGURES_DIR}")


if __name__ == "__main__":
    main()
