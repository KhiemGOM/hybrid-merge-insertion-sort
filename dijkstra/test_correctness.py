"""Cross-check the implementation against a heapq-based reference Dijkstra."""
import heapq
from dijkstra import dijkstra_matrix_array, INF
from graph_gen import generate_edges, to_matrix, to_adj_lists


def reference(adj, s):
    d = [INF] * len(adj); d[s] = 0
    pq = [(0, s)]
    while pq:
        du, u = heapq.heappop(pq)
        if du > d[u]:
            continue
        for v, w in adj[u]:
            if du + w < d[v]:
                d[v] = du + w
                heapq.heappush(pq, (d[v], v))
    return d


def main():
    cases = 0
    for n in (2, 3, 5, 10, 30, 60):
        for m in sorted({n - 1, 2 * n, n * n // 2, n * (n - 1)}):
            if not n - 1 <= m <= n * (n - 1):
                continue
            for seed in range(5):
                e = generate_edges(n, m, seed=seed)
                assert len(e) == m and len({(u, v) for u, v, _ in e}) == m
                adj = to_adj_lists(n, e)
                ref = reference(adj, 0)
                assert dijkstra_matrix_array(to_matrix(n, e), 0)[0] == ref
                cases += 1
    print(f"All {cases} cases passed.")


if __name__ == "__main__":
    main()
