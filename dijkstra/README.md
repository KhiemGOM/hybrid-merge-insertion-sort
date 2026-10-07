# Project 2: Dijkstra's Algorithm (SC2001)

Files
- `dijkstra.py` - (a) adjacency matrix + array PQ, (b) adjacency lists + binary min-heap
- `graph_gen.py` - random connected weighted digraphs with exact |V| and |E|
- `test_correctness.py` - checks both against a `heapq` reference
- `experiments.py` - empirical study, writes CSVs and PNGs to `results/`

Run (from this folder, needs `matplotlib`):
```
python test_correctness.py
python experiments.py
```

"Key comparisons" = comparisons between distance values (PQ scans, heap sifts, relaxation tests).

## (a) Adjacency matrix + array: Theta(|V|^2)

- Extract-min scans the array: Theta(|V|), done |V| times -> Theta(|V|^2).
- Each extracted vertex scans its matrix row to find neighbours: Theta(|V|), |V| times -> Theta(|V|^2).
- Decrease-key is a single array write: O(1), at most |E| times -> O(|E|).
- Total: Theta(|V|^2 + |E|) = Theta(|V|^2), independent of |E| (|E| <= |V|^2).

## (b) Adjacency lists + min-heap: O((|V| + |E|) log |V|)

- Each vertex is inserted once and extracted once: O(|V| log |V|).
- Each edge is examined once; a successful relaxation does decrease-key (sift-up, position map kept): O(log |V|) each, so O(|E| log |V|).
- Total: O((|V| + |E|) log |V|). For a connected graph (|E| >= |V| - 1) this is O(|E| log |V|).
  - Sparse (|E| = O(|V|)): O(|V| log |V|).
  - Dense (|E| = Theta(|V|^2)): O(|V|^2 log |V|).

## Empirical results (see `results/`)

| Experiment | Observation |
|---|---|
| exp1: E = 5V, V = 100..1000 | (a) comparisons grow ~|V|^2 (5,307 -> 503,005); (b) grows ~|V| log |V| (1,243 -> 18,802). At V = 1000 (b) is ~15x faster in time. |
| exp2: E = V(V-1)/2, V = 100..700 | Both grow ~|V|^2 (b with extra log factor in the worst case). (b) does fewer comparisons, but its time crosses above (a) from V ~ 600 because of heap overhead (swaps, position map). |
| exp3: V = 500, E = 499..249,500 | (a) is flat in |E| (125,749 -> 250,000 comparisons, time ~0.022-0.034 s); (b) grows with |E| (499 -> 132,907 comparisons), and becomes slower than (a) in time at the densest setting (0.047 s vs 0.034 s). |

Note: the comparison count for (a) only counts the PQ scan and relaxation tests; the matrix row scan
(a Theta(|V|) loop per vertex, even for non-edges) is what keeps its running time at Theta(|V|^2) and is
visible in the timings. Timings are Python wall-clock averaged over 3 random graphs, so exact numbers vary by machine.

## (c) Comparison

| | (a) matrix + array | (b) lists + heap |
|---|---|---|
| Time | Theta(V^2) | O((V + E) log V) |
| Space | Theta(V^2) | Theta(V + E) |
| Depends on E? | No | Yes |

- **Sparse graphs (E << V^2 / log V)**: (b) is clearly better, near-linear vs quadratic (e.g. road networks, E = O(V)).
- **Dense graphs (E = Theta(V^2))**: (a) is better or equal: Theta(V^2) vs Theta(V^2 log V), and it has a smaller constant factor
  (no heap swaps or position bookkeeping, simpler memory access). Crossover is roughly when E log V ~ V^2, i.e. E ~ V^2 / log V.
- Memory: the matrix needs Theta(V^2) space even when the graph is sparse; adjacency lists need Theta(V + E).
- A Fibonacci heap would give O(E + V log V) and beat both in theory, but is rarely faster in practice.
