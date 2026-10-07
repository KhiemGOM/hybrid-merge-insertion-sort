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

| Experiment | Observation |
|---|---|
| exp1: E = 5V, V = 100..1000 | Comparisons grow quadratically in |V| (5,307 -> 503,005); time ~0.001 s -> ~0.11 s. |
| exp2: E = V(V-1)/2, V = 100..700 | Also quadratic in |V| (7,531 -> 367,665). |
| exp3: V = 500, E = 499..249,500 | Almost flat in |E| (125,749 -> 250,000 comparisons, time ~0.023-0.033 s): cost is driven by |V|, not |E|. |

Note: the comparison count only covers the PQ scan and relaxation tests; the matrix row scan
(a Theta(|V|) loop per vertex, even for non-edges) is not counted but is reflected in the timings.
Timings are Python wall-clock averages over 3 random graphs, so exact numbers vary by machine.
