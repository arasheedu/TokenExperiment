#!/usr/bin/env python3
"""Visualise results.csv produced by measure_models.py.

Usage:
    pip install matplotlib
    python plot_results.py [results.csv] [--out results.png] [--share-axes-with other.csv ...]

Draws three panels per model: output tokens (mean ± sd), wall time, and the
share of runs whose generated solver produced the correct answer.
"""

from __future__ import annotations

import argparse
import csv
import statistics
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# Light-mode palette: one hue for magnitude, status colours for pass/fail.
BLUE = "#2a78d6"
GOOD = "#0ca30c"
CRITICAL = "#d03b3b"
INK = "#0b0b0b"
INK_2 = "#52514e"
GRID = "#e4e3df"
SURFACE = "#fcfcfb"


def load(path: Path) -> list[dict]:
    with path.open(newline="") as f:
        rows = list(csv.DictReader(f))
    if not rows:
        sys.exit(f"{path} is empty")
    return rows


def summarise(rows: list[dict]) -> list[dict]:
    """Aggregate per model: mean/sd output tokens, mean input, mean seconds, pass rate."""
    by_model: dict[str, list[dict]] = {}
    for r in rows:
        by_model.setdefault(r["model"], []).append(r)

    out = []
    for model, rs in sorted(by_model.items()):
        ok = [r for r in rs if r.get("output_tokens") not in ("", None)]
        toks = [int(r["output_tokens"]) for r in ok]
        ins = [int(r["input_tokens"]) for r in ok]
        secs = [float(r["wall_seconds"]) for r in ok if r.get("wall_seconds")]
        passes = sum(1 for r in rs if str(r.get("correct")).lower() == "true")
        out.append({
            "model": model,
            "n": len(rs),
            "out_mean": statistics.mean(toks) if toks else 0,
            "out_sd": statistics.stdev(toks) if len(toks) > 1 else 0,
            "in_mean": statistics.mean(ins) if ins else 0,
            "sec_mean": statistics.mean(secs) if secs else 0,
            "pass_rate": passes / len(rs) if rs else 0,
        })
    return out


def print_table(summary: list[dict]) -> None:
    print(f"{'model':40s} {'n':>2}  {'out_tokens (mean ± sd)':>22}  {'in_tokens':>9}  {'seconds':>7}  pass")
    for s in summary:
        print(f"{s['model']:40s} {s['n']:2d}  {s['out_mean']:11.0f} ± {s['out_sd']:7.0f}"
              f"  {s['in_mean']:9.0f}  {s['sec_mean']:7.1f}  {s['pass_rate']:4.0%}")


def axis_limits(*summaries: list[dict]) -> tuple[float, float, float]:
    """x-axis upper limits (tokens, seconds, pass %) covering every summary given."""
    all_rows = [s for summary in summaries for s in summary]
    tok = max((s["out_mean"] + s["out_sd"] for s in all_rows), default=1)
    sec = max((s["sec_mean"] for s in all_rows), default=1)
    return tok * 1.25, sec * 1.25, 125


def plot(summary: list[dict], out_path: Path,
         limits: tuple[float, float, float] | None = None) -> None:
    limits = limits or axis_limits(summary)
    models = [s["model"] for s in summary]
    y = list(range(len(models)))
    fig, axes = plt.subplots(
        1, 3, figsize=(15, max(3.5, 0.5 * len(models) + 1.5)),
        sharey=True, facecolor=SURFACE,
    )
    fig.suptitle("Sudoku solver generation, per Claude model",
                 color=INK, fontsize=13, x=0.01, ha="left")

    panels = [
        ("Output tokens (mean ± sd)", [s["out_mean"] for s in summary],
         [s["out_sd"] for s in summary], BLUE, "{:,.0f}"),
        ("Wall time, seconds", [s["sec_mean"] for s in summary], None, BLUE, "{:.1f}"),
        ("Correct solutions, % of runs", [100 * s["pass_rate"] for s in summary],
         None, None, "{:.0f}%"),
    ]
    for ax, xmax, (title, vals, err, color, fmt) in zip(axes, limits, panels):
        colors = color or [GOOD if v == 100 else CRITICAL for v in vals]
        ax.barh(y, vals, height=0.6, color=colors,
                xerr=err, ecolor=INK_2, capsize=3, error_kw={"lw": 1})
        for i, v in enumerate(vals):
            x = v + (err[i] if err else 0)
            ax.text(x, i, "  " + fmt.format(v), va="center", fontsize=9, color=INK_2)
        ax.set_title(title, loc="left", fontsize=10, color=INK)
        ax.set_facecolor(SURFACE)
        ax.grid(axis="x", color=GRID, lw=0.8)
        ax.set_axisbelow(True)
        for side in ("top", "right", "left"):
            ax.spines[side].set_visible(False)
        ax.spines["bottom"].set_color(GRID)
        ax.tick_params(colors=INK_2, length=0)
        ax.set_xlim(0, xmax)

    axes[0].set_yticks(y)
    axes[0].set_yticklabels(models, color=INK, fontsize=9)
    axes[0].invert_yaxis()
    fig.tight_layout(rect=(0, 0, 1, 0.95))
    fig.savefig(out_path, dpi=150, facecolor=SURFACE)
    print(f"\nchart written to {out_path}")


def main() -> None:
    ap = argparse.ArgumentParser(description="Plot token statistics from results.csv")
    ap.add_argument("csv", nargs="?", default="results.csv", help="input CSV (default results.csv)")
    ap.add_argument("--out", default="results.png", help="output image (default results.png)")
    ap.add_argument("--share-axes-with", metavar="CSV", nargs="+", default=[],
                    help="other result CSVs; x-axis limits cover them too, so charts compare directly")
    args = ap.parse_args()

    summary = summarise(load(Path(args.csv)))
    others = [summarise(load(Path(p))) for p in args.share_axes_with]
    print_table(summary)
    plot(summary, Path(args.out), axis_limits(summary, *others))


if __name__ == "__main__":
    main()
