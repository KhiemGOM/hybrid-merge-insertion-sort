# Project 2 (a): Dijkstra's Algorithm with Adjacency Matrix + Array (SC2001)

Files
- `dijkstra.py` - Dijkstra using an adjacency matrix and an array as the priority queue
- `graph_gen.py` - random connected weighted digraphs with exact |V| and |E|
- `test_correctness.py` - checks the result against a `heapq` reference
- `experiments.py` - empirical study, writes CSVs and PNGs to `results/`

Run (from this folder, needs `matplotlib`):
```
python test_correctness.py
python experiments.py
```

"Key comparisons" = comparisons between distance values (PQ array scan and relaxation tests).

## Theoretical complexity: Theta(|V|^2)

- Extract-min scans the array: Theta(|V|), done |V| times -> Theta(|V|^2).
- Each extracted vertex scans its matrix row to find neighbours: Theta(|V|), |V| times -> Theta(|V|^2).
- Decrease-key is a single array write: O(1), at most |E| times -> O(|E|).
- Total: Theta(|V|^2 + |E|) = Theta(|V|^2), independent of |E| (since |E| <= |V|^2).
- Space: Theta(|V|^2) for the matrix.

## Empirical results (see `results/`)

`experiments.py` runs the algorithm on a grid: |V| = 100..1000 (step 100) x |E| = 5000..100000 (step 5000),
skipping infeasible cells (|E| > |V|(|V|-1)). Each cell uses 5 random graphs (comparisons averaged, time = median).
Raw data: `results/grid.csv`. Comparisons are split into array-scan and relaxation parts.

| File | Content |
|---|---|
| `vs_E_fixedV.png` | |V| = 500, vary |E|: total / scan / relaxation comparisons and time |
| `vs_V_fixedE.png` | |E| = 20000, vary |V|: same quantities |
| `contour_comparisons.png` | Filled contours over the (|V|, |E|) plane for scan, relaxation and total comparisons |
| `contour_time.png` | Same for running time |

Findings
- Scan comparisons depend only on |V| (about |V|^2 / 2): constant in |E|, vertical contour lines.
- Relaxation comparisons depend only on |E| (about |E| / 2): constant in |V|, horizontal contour lines.
- Least-squares fit over the whole grid: comparisons = 0.5004 |V|^2 + 0.5002 |E| + 118 (R^2 = 1.0000).
- Time fit: 9.3e-8 |V|^2 + 5.9e-8 |E| (R^2 = 0.99). Both terms are present, but |V|^2 dominates for most of the grid,
  matching Theta(|V|^2 + |E|) = Theta(|V|^2).
- The matrix row scan (a Theta(|V|) loop per vertex even for non-edges) is not a key comparison, so it is not
  counted, but it is why the time still grows as |V|^2.

Timings are Python wall-clock numbers, so exact values vary by machine.
