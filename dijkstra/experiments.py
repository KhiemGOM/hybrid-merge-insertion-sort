"""
Empirical analysis of Dijkstra with adjacency matrix + array PQ.

Exp 1: sparse graphs, E = 5V, V varies         (E grows linearly with V)
Exp 2: dense graphs,  E = V(V-1)/2, V varies   (E grows quadratically)
Exp 3: V fixed, E varies from V-1 up to V(V-1)

For each point: average over several random graphs of key comparisons and
running time (graph conversion excluded from timing). Outputs CSVs and PNGs
into ./results.
"""
import csv
import os
import time

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from dijkstra import dijkstra_matrix_array
from graph_gen import generate_edges, to_matrix

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "results")
TRIALS = 3


def measure(n, m):
    comps = secs = 0.0
    for seed in range(TRIALS):
        mat = to_matrix(n, generate_edges(n, m, seed=seed))
        t = time.perf_counter()
        _, _, c = dijkstra_matrix_array(mat, 0)
        secs += time.perf_counter() - t
        comps += c
    return comps / TRIALS, secs / TRIALS


def run(name, points, xlabel, xfunc):
    rows = []
    for n, m in points:
        c, t = measure(n, m)
        rows.append((n, m, c, t))
        print(f"{name}: V={n:5d} E={m:7d}  comparisons={c:12.0f}  time={t:.4f}s")
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, f"{name}.csv"), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["V", "E", "comparisons", "seconds"])
        w.writerows(rows)

    xs = [xfunc(n, m) for n, m, *_ in rows]
    fig, axes = plt.subplots(1, 2, figsize=(13, 5))
    for ax, i, ylab in ((axes[0], 2, "Key comparisons"),
                        (axes[1], 3, "Running time (s)")):
        ax.plot(xs, [r[i] for r in rows], "o-", label="(a) matrix + array")
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylab)
        ax.grid(True, linestyle="--", alpha=0.6)
        ax.legend()
    fig.suptitle(name.replace("_", " "))
    fig.tight_layout()
    fig.savefig(os.path.join(OUT, f"{name}.png"), dpi=130)
    plt.close(fig)


def main():
    run("exp1_sparse_E_5V",
        [(n, 5 * n) for n in range(100, 1001, 100)], "|V| (with |E| = 5|V|)",
        lambda n, m: n)
    run("exp2_dense_E_V2",
        [(n, n * (n - 1) // 2) for n in range(100, 701, 100)],
        "|V| (with |E| = |V|(|V|-1)/2)", lambda n, m: n)
    n = 500
    es = [n - 1, 2 * n, 5 * n, 10 * n, 20 * n, 50 * n, 100 * n, 200 * n,
          n * (n - 1)]
    run("exp3_fixed_V500_vary_E", [(n, e) for e in es], "|E| (with |V| = 500)",
        lambda n, m: m)


if __name__ == "__main__":
    main()
