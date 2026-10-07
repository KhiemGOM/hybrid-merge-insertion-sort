"""
Empirical analysis of Dijkstra with adjacency matrix + array PQ on a grid in
(|V|, |E|) space. For each feasible cell (|V|-1 <= |E| <= |V|(|V|-1)) we run
TRIALS random graphs and average key comparisons (split into scan / relaxation
parts) and running time. Outputs go into ./results:
    grid.csv                    raw averaged grid
    vs_E_fixedV.png             line charts, |V| fixed, |E| varies
    vs_V_fixedE.png             line charts, |E| fixed, |V| varies
    contour_comparisons.png     filled contours over the (|V|, |E|) plane
    contour_time.png
"""
import csv
import gc
import os
import sys
import time

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from dijkstra import dijkstra_matrix_array
from graph_gen import generate_edges, to_matrix

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "results")
TRIALS = 5
PASSES = 3  # whole-grid timing passes, see run_grid
V_VALUES = list(range(100, 1001, 100))
E_VALUES = list(range(5000, 100001, 5000))
FIXED_V = 500
FIXED_E = 20000


def run_grid():
    """
    Timing on a busy machine is noisy in stretches, so a median of a few runs
    inside one cell can still come out slow (it showed up as bumps in the time
    contours). Instead every (|V|, |E|, seed) graph is timed once per pass,
    each pass visits the graphs in a different shuffled order, and every graph
    keeps its fastest time. Counts are deterministic, so they just come from
    the last pass.
    """
    shape = (len(V_VALUES), len(E_VALUES))
    tasks = [(i, j, s) for i, n in enumerate(V_VALUES) for j, m in enumerate(E_VALUES)
             if n - 1 <= m <= n * (n - 1) for s in range(TRIALS)]
    best = {t: float("inf") for t in tasks}
    counts = {}
    rng = np.random.default_rng(2001)

    for p in range(PASSES):
        for k in rng.permutation(len(tasks)):
            i, j, s = tasks[k]
            n, m = V_VALUES[i], E_VALUES[j]
            mat = to_matrix(n, generate_edges(n, m, seed=s))
            gc.collect()
            gc.disable()
            t = time.perf_counter()
            _, _, c = dijkstra_matrix_array(mat, 0)
            elapsed = time.perf_counter() - t
            gc.enable()
            best[tasks[k]] = min(best[tasks[k]], elapsed)
            counts[tasks[k]] = c
        print(f"pass {p + 1}/{PASSES} done", flush=True)

    g = {k: np.full(shape, np.nan) for k in ("scan", "relax", "total", "time")}
    for i in range(len(V_VALUES)):
        for j in range(len(E_VALUES)):
            cell = [(i, j, s) for s in range(TRIALS) if (i, j, s) in best]
            if not cell:
                continue
            g["scan"][i, j] = np.mean([counts[t].scan for t in cell])
            g["relax"][i, j] = np.mean([counts[t].relax for t in cell])
            g["total"][i, j] = g["scan"][i, j] + g["relax"][i, j]
            g["time"][i, j] = float(np.median([best[t] for t in cell]))
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, "grid.csv"), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["V", "E", "scan_cmp", "relax_cmp", "total_cmp", "seconds"])
        for i, n in enumerate(V_VALUES):
            for j, m in enumerate(E_VALUES):
                if not np.isnan(g["total"][i, j]):
                    w.writerow([n, m] + [g[k][i, j] for k in
                                         ("scan", "relax", "total", "time")])
    return g


def line_figure(xs, g_slice, xlabel, title, fname, square_x=False):
    """square_x: plot against |V|^2 (ticks labelled with |V|^2 and |V|) so that
    the quadratic dependence on |V| shows up as a straight line."""
    labels = ([f"{x * x:,}\n(V={x})" for x in xs] if square_x
              else [f"{x:,}" for x in xs])
    pos = [x * x for x in xs] if square_x else list(xs)
    fig, axes = plt.subplots(1, 2, figsize=(14, 5.5))
    ax = axes[0]
    styles = [("total", "Total Comparisons", "o", "tab:blue"),
              ("scan", "Array Scan Comparisons (extract-min)", "s", "tab:orange"),
              ("relax", "Relaxation Comparisons", "^", "tab:green")]
    for key, label, mk, col in styles:
        ax.plot(pos, g_slice[key], marker=mk, markersize=7, linewidth=2,
                color=col, label=label)
    ax.set_ylabel("Number of Key Comparisons", fontsize=12)
    ax.set_title("Key Comparisons", fontsize=13, fontweight="bold")
    ax2 = axes[1]
    ax2.plot(pos, g_slice["time"], marker="D", markersize=7, linewidth=2,
             color="tab:red", label="Running time")
    ax2.set_ylabel("Running time (s)", fontsize=12)
    ax2.set_title("Running Time (median of trials)", fontsize=13, fontweight="bold")
    ax2.set_ylim(bottom=0)
    for a in axes:
        a.set_xlabel(xlabel, fontsize=12)
        step = 2 if square_x else 1          # skip alternate labels, avoids overlap
        a.set_xticks(pos[::step])
        a.set_xticklabels(labels[::step], fontsize=8)
        a.tick_params(axis="x", rotation=45 if not square_x else 0)
        a.grid(True, linestyle="--", alpha=0.6)
        a.legend()
    fig.suptitle(title, fontsize=14, fontweight="bold")
    fig.tight_layout()
    fig.savefig(os.path.join(OUT, fname), dpi=130)
    plt.close(fig)


def contour_figure(g, keys, titles, fname, cbar_labels):
    fig, axes = plt.subplots(1, len(keys), figsize=(6.2 * len(keys), 5.5))
    V2 = [v * v for v in V_VALUES]          # x axis is |V|^2 so cost is linear
    X, Y = np.meshgrid(V2, E_VALUES, indexing="ij")
    for ax, key, title, lab in zip(np.atleast_1d(axes), keys, titles, cbar_labels):
        Z = np.ma.masked_invalid(g[key])
        cf = ax.contourf(X, Y, Z, levels=14, cmap="viridis")
        cl = ax.contour(X, Y, Z, levels=14, colors="white", linewidths=0.8)
        ax.clabel(cl, fmt="%.3g", fontsize=7)
        fig.colorbar(cf, ax=ax, label=lab)
        ax.plot(V2, [v * (v - 1) for v in V_VALUES], "r--", linewidth=1,
                label="|E| = |V|(|V|-1) (max)")
        ax.set_ylim(E_VALUES[0], E_VALUES[-1])
        ax.set_facecolor("lightgray")      # infeasible region (|E| > |V|(|V|-1))
        ax.set_xlim(V2[0], V2[-1])
        ax.set_xticks(V2[1::2])
        ax.set_xticklabels([f"{v * v:,}\n(V={v})" for v in V_VALUES[1::2]],
                           fontsize=8)
        ax.text(V2[0] + 5000, E_VALUES[-1] * 0.93, "infeasible", fontsize=8)
        ax.set_xlabel("|V|^2 (number of vertices squared)", fontsize=12)
        ax.set_ylabel("Number of Edges (|E|)", fontsize=12)
        ax.set_title(title, fontsize=13, fontweight="bold")
        ax.legend(loc="lower right", fontsize=8)
    fig.tight_layout()
    fig.savefig(os.path.join(OUT, fname), dpi=130)
    plt.close(fig)


def fit_report(g):
    """Least squares: total ~ a*V^2 + b*E + c, to check the linear structure."""
    rows = [(n, m, g["total"][i, j], g["time"][i, j])
            for i, n in enumerate(V_VALUES) for j, m in enumerate(E_VALUES)
            if not np.isnan(g["total"][i, j])]
    n, m, tot, tim = map(np.array, zip(*rows))
    A = np.column_stack([n ** 2, m, np.ones_like(n)])
    for name, y in (("comparisons", tot), ("time", tim)):
        coef, *_ = np.linalg.lstsq(A, y, rcond=None)
        r2 = 1 - ((y - A @ coef) ** 2).sum() / ((y - y.mean()) ** 2).sum()
        print(f"fit {name}: {coef[0]:.4g}*V^2 + {coef[1]:.4g}*E + {coef[2]:.4g}"
              f"   R^2 = {r2:.4f}")


def load_grid():
    shape = (len(V_VALUES), len(E_VALUES))
    g = {k: np.full(shape, np.nan) for k in ("scan", "relax", "total", "time")}
    with open(os.path.join(OUT, "grid.csv")) as f:
        for r in csv.DictReader(f):
            i, j = V_VALUES.index(int(r["V"])), E_VALUES.index(int(r["E"]))
            g["scan"][i, j] = float(r["scan_cmp"])
            g["relax"][i, j] = float(r["relax_cmp"])
            g["total"][i, j] = float(r["total_cmp"])
            g["time"][i, j] = float(r["seconds"])
    return g


def main():
    # `python experiments.py --replot` redraws from results/grid.csv without rerunning
    g = load_grid() if "--replot" in sys.argv else run_grid()
    i = V_VALUES.index(FIXED_V)
    line_figure(E_VALUES, {k: v[i, :] for k, v in g.items()},
                "Number of Edges (|E|)",
                f"Dijkstra (matrix + array), |V| = {FIXED_V}: Cost vs. |E|",
                "vs_E_fixedV.png")
    j = E_VALUES.index(FIXED_E)
    ok = [k for k, n in enumerate(V_VALUES) if n * (n - 1) >= FIXED_E]
    line_figure([V_VALUES[k] for k in ok],
                {k: v[ok, j] for k, v in g.items()},
                "|V|^2 (number of vertices squared)",
                f"Dijkstra (matrix + array), |E| = {FIXED_E}: Cost vs. |V|^2",
                "vs_V_fixedE.png", square_x=True)
    contour_figure(g, ["scan", "relax", "total"],
                   ["Array scan comparisons", "Relaxation comparisons",
                    "Total comparisons"], "contour_comparisons.png",
                   ["comparisons"] * 3)
    contour_figure(g, ["time"], ["Running time"], "contour_time.png",
                   ["seconds"])
    fit_report(g)


if __name__ == "__main__":
    main()
