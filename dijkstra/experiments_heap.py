"""
Empirical analysis of Dijkstra with adjacency lists + min-heap (part b) on the
same (|V|, |E|) grid as experiments.py, so (a) and (b) can be compared cell by
cell. Per feasible cell we run TRIALS random graphs (same seeds as part a) and
average the comparison counts; running time is the median. Outputs go into
./results_heap:
    grid.csv                     raw averaged grid
    vs_E_fixedV.png              line charts, |V| fixed, |E| varies
    vs_V_fixedE.png              line charts, |E| fixed, x axis is |V|log2|V|
    contour_comparisons.png      filled contours, x axis is |V|log2|V|
    contour_time.png

Why |V|log2|V|: every vertex is popped from the heap about once and each pop
costs ~log|V| comparisons, so the |V| side of the cost grows like |V|log|V|
while the relaxation checks grow exactly like |E|. Putting |V|log|V| on the
x axis and |E| on the y axis makes the contours of the total close to
straight lines (fit_report prints how close).
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

from dijkstra_heap import dijkstra_heap
from graph_gen import generate_edges, to_adj_lists

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "results_heap")
TRIALS = 5
PASSES = 3  # whole-grid passes, see run_grid
V_VALUES = list(range(100, 1001, 100))
E_VALUES = list(range(5000, 100001, 5000))
COUNT_KEYS = ("heap", "relax", "stale", "total", "updates")
KEYS = COUNT_KEYS + ("time",)


def run_grid():
    """
    Timing on a busy laptop is noisy in stretches (a whole row of V values can
    come out slow), so a best-of-N inside one cell doesn't help. Instead every
    (V, E, seed) graph is timed once per pass, passes visit the graphs in a
    different shuffled order, and each graph keeps its fastest time. Counts are
    deterministic so they only come from the first pass.
    """
    shape = (len(V_VALUES), len(E_VALUES))
    tasks = [(i, j, s) for i, n in enumerate(V_VALUES) for j, m in enumerate(E_VALUES)
             if n - 1 <= m <= n * (n - 1) for s in range(TRIALS)]
    best = {t: float("inf") for t in tasks}
    counts = {}
    rng = np.random.default_rng(2001)

    for p in range(PASSES):
        for done, t in enumerate(rng.permutation(len(tasks))):
            i, j, s = tasks[t]
            adj = to_adj_lists(V_VALUES[i], generate_edges(V_VALUES[i], E_VALUES[j], seed=s))
            gc.collect()
            gc.disable()
            start = time.perf_counter()
            _, c = dijkstra_heap(adj, 0)
            elapsed = time.perf_counter() - start
            gc.enable()
            best[tasks[t]] = min(best[tasks[t]], elapsed)
            counts[tasks[t]] = c
        print(f"pass {p + 1}/{PASSES} done", flush=True)

    g = {k: np.full(shape, np.nan) for k in KEYS}
    for i in range(len(V_VALUES)):
        for j in range(len(E_VALUES)):
            cell = [(i, j, s) for s in range(TRIALS) if (i, j, s) in best]
            if not cell:
                continue
            for k in COUNT_KEYS:
                g[k][i, j] = np.mean([getattr(counts[t], k) for t in cell])
            g["time"][i, j] = float(np.median([best[t] for t in cell]))
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, "grid.csv"), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["V", "E", "heap_cmp", "relax_cmp", "stale_cmp", "total_cmp",
                    "updates_K", "seconds"])
        for i, n in enumerate(V_VALUES):
            for j, m in enumerate(E_VALUES):
                if not np.isnan(g["total"][i, j]):
                    w.writerow([n, m] + [g[k][i, j] for k in KEYS])
    return g


def load_grid():
    shape = (len(V_VALUES), len(E_VALUES))
    g = {k: np.full(shape, np.nan) for k in KEYS}
    cols = {"heap": "heap_cmp", "relax": "relax_cmp", "stale": "stale_cmp",
            "total": "total_cmp", "updates": "updates_K", "time": "seconds"}
    with open(os.path.join(OUT, "grid.csv")) as f:
        for r in csv.DictReader(f):
            i, j = V_VALUES.index(int(r["V"])), E_VALUES.index(int(r["E"]))
            for k, col in cols.items():
                g[k][i, j] = float(r[col])
    return g


FIXED_V = 500
FIXED_E = 20000


def vlogv(v):
    return v * np.log2(v)


def line_figure(xs, g_slice, xlabel, title, fname, vlogv_x=False):
    """vlogv_x: plot against |V|log2|V| (ticks show both that and |V|)."""
    pos = [vlogv(x) for x in xs] if vlogv_x else list(xs)
    labels = ([f"{vlogv(x):,.0f}\n(V={x})" for x in xs] if vlogv_x
              else [f"{x:,}" for x in xs])
    fig, axes = plt.subplots(1, 2, figsize=(14, 5.5))
    styles = [("total", "Total Comparisons", "o", "tab:blue"),
              ("heap", "Heap Comparisons (sift up/down)", "s", "tab:orange"),
              ("relax", "Relaxation Comparisons", "^", "tab:green"),
              ("stale", "Stale Check Comparisons", "D", "tab:purple")]
    for key, label, mk, col in styles:
        axes[0].plot(pos, g_slice[key], marker=mk, markersize=7, linewidth=2,
                     color=col, label=label)
    axes[0].set_ylabel("Number of Key Comparisons", fontsize=12)
    axes[0].set_title("Key Comparisons", fontsize=13, fontweight="bold")
    axes[1].plot(pos, g_slice["time"], marker="D", markersize=7, linewidth=2,
                 color="tab:red", label="Running time")
    axes[1].set_ylabel("Running time (s)", fontsize=12)
    axes[1].set_title("Running Time (median of trials)", fontsize=13, fontweight="bold")
    axes[1].set_ylim(bottom=0)
    step = 2 if vlogv_x else 1                  # skip alternate labels, avoids overlap
    for a in axes:
        a.set_xlabel(xlabel, fontsize=12)
        a.set_xticks(pos[::step])
        a.set_xticklabels(labels[::step], fontsize=8)
        a.tick_params(axis="x", rotation=0 if vlogv_x else 45)
        a.grid(True, linestyle="--", alpha=0.6)
        a.legend()
    fig.suptitle(title, fontsize=14, fontweight="bold")
    fig.tight_layout()
    fig.savefig(os.path.join(OUT, fname), dpi=130)
    plt.close(fig)


def contour_figure(g, keys, titles, fname, cbar_labels, ncols):
    nrows = -(-len(keys) // ncols)
    fig, axes = plt.subplots(nrows, ncols, figsize=(6.2 * ncols, 5.4 * nrows))
    xv = [vlogv(v) for v in V_VALUES]             # x axis is |V|log2|V| so cost is ~linear
    X, Y = np.meshgrid(xv, E_VALUES, indexing="ij")
    for ax, key, title, lab in zip(np.atleast_1d(axes).ravel(), keys, titles, cbar_labels):
        Z = np.ma.masked_invalid(g[key])
        cf = ax.contourf(X, Y, Z, levels=14, cmap="viridis")
        cl = ax.contour(X, Y, Z, levels=14, colors="white", linewidths=0.8)
        ax.clabel(cl, fmt="%.3g", fontsize=7)
        fig.colorbar(cf, ax=ax, label=lab)
        ax.plot(xv, [v * (v - 1) for v in V_VALUES], "r--", linewidth=1,
                label="|E| = |V|(|V|-1) (max)")
        ax.set_ylim(E_VALUES[0], E_VALUES[-1])
        ax.set_facecolor("lightgray")             # infeasible region
        ax.set_xlim(xv[0], xv[-1])
        ax.set_xticks(xv[1::2])
        ax.set_xticklabels([f"{x:,.0f}\n(V={v})" for x, v in
                            zip(xv[1::2], V_VALUES[1::2])], fontsize=8)
        ax.text(xv[0] + 200, E_VALUES[-1] * 0.93, "infeasible", fontsize=8)
        ax.set_xlabel("|V| log2|V|", fontsize=12)
        ax.set_ylabel("Number of Edges (|E|)", fontsize=12)
        ax.set_title(title, fontsize=13, fontweight="bold")
        ax.legend(loc="lower right", fontsize=8)
    fig.tight_layout()
    fig.savefig(os.path.join(OUT, fname), dpi=130)
    plt.close(fig)


def fit_report(g):
    """Least squares: cost ~ a*E + b*V*log2(V) + c, to check how straight the
    contours in the (V log V, E) plane can be. K is fitted separately, it
    follows V*ln(E/V), which mixes V and E and is why the heap and stale
    contours bend a little."""
    rows = [(n, m, i, j) for i, n in enumerate(V_VALUES) for j, m in enumerate(E_VALUES)
            if not np.isnan(g["total"][i, j])]
    n, m = (np.array(c, float) for c in zip(*[(r[0], r[1]) for r in rows]))
    cell = lambda k: np.array([g[k][r[2], r[3]] for r in rows])
    A = np.column_stack([m, vlogv(n), np.ones_like(n)])
    for name, key in (("total comparisons", "total"), ("heap comparisons", "heap"),
                      ("stale checks", "stale"), ("time", "time")):
        y = cell(key)
        coef, *_ = np.linalg.lstsq(A, y, rcond=None)
        r2 = 1 - ((y - A @ coef) ** 2).sum() / ((y - y.mean()) ** 2).sum()
        print(f"fit {name:<18}: {coef[0]:.4g}*E + {coef[1]:.4g}*V*log2V + {coef[2]:.4g}"
              f"   R^2 = {r2:.4f}")
    print(f"relaxation checks == |E| in every cell: {np.allclose(cell('relax'), m)}")
    y = cell("updates")
    B = np.column_stack([n * np.log(m / n), np.ones_like(n)])
    coef, *_ = np.linalg.lstsq(B, y, rcond=None)
    r2 = 1 - ((y - B @ coef) ** 2).sum() / ((y - y.mean()) ** 2).sum()
    print(f"fit K (successful relaxations): {coef[0]:.4g}*V*ln(E/V) + {coef[1]:.4g}"
          f"   R^2 = {r2:.4f}")


def main():
    # `python experiments_heap.py --replot` redraws from results_heap/grid.csv
    g = load_grid() if "--replot" in sys.argv else run_grid()
    i = V_VALUES.index(FIXED_V)
    line_figure(E_VALUES, {k: v[i, :] for k, v in g.items()},
                "Number of Edges (|E|)",
                f"Dijkstra (adjacency lists + heap), |V| = {FIXED_V}: Cost vs. |E|",
                "vs_E_fixedV.png")
    j = E_VALUES.index(FIXED_E)
    ok = [k for k, n in enumerate(V_VALUES) if n * (n - 1) >= FIXED_E]
    line_figure([V_VALUES[k] for k in ok], {k: v[ok, j] for k, v in g.items()},
                "|V| log2|V| (number of vertices times log2 of it)",
                f"Dijkstra (adjacency lists + heap), |E| = {FIXED_E}: Cost vs. |V|log|V|",
                "vs_V_fixedE.png", vlogv_x=True)
    contour_figure(g, ["heap", "relax", "stale", "total"],
                   ["Heap comparisons", "Relaxation comparisons",
                    "Stale check comparisons", "Total comparisons"],
                   "contour_comparisons.png", ["comparisons"] * 4, ncols=2)
    contour_figure(g, ["time"], ["Running time"], "contour_time.png",
                   ["seconds"], ncols=1)
    fit_report(g)


if __name__ == "__main__":
    main()
