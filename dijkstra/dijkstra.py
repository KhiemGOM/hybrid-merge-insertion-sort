"""
Dijkstra's algorithm (single source shortest paths), part (a):
adjacency matrix + array as priority queue.

    - extract-min is a linear scan of the array          -> O(V) each
    - decrease-key is a direct array write               -> O(1) each
    - total: O(V^2) regardless of |E|

Returns (dist, parent, comparisons) where `comparisons` is the number of key
comparisons made (distance comparisons in the priority queue scan and in edge
relaxation). This is the empirical measure used in the experiments.
"""

INF = float("inf")


def dijkstra_matrix_array(matrix, source):
    """matrix[u][v] = weight of edge u->v, or 0 / INF when there is no edge
    (weights are positive, so 0 is used as 'no edge' in the matrix)."""
    n = len(matrix)
    dist = [INF] * n
    parent = [-1] * n
    dist[source] = 0
    in_pq = [True] * n          # the "array" priority queue: dist[] + in_pq[]
    comparisons = 0

    for _ in range(n):
        # extract-min: linear scan over the array, Theta(V)
        u = -1
        best = INF
        for v in range(n):
            if in_pq[v]:
                comparisons += 1
                if u == -1 or dist[v] < best:
                    u, best = v, dist[v]
        if best == INF:
            break               # remaining vertices unreachable
        in_pq[u] = False

        # scan the whole matrix row, Theta(V)
        row = matrix[u]
        for v in range(n):
            w = row[v]
            if w and in_pq[v]:
                comparisons += 1
                if dist[u] + w < dist[v]:
                    dist[v] = dist[u] + w       # decrease-key, O(1)
                    parent[v] = u
    return dist, parent, comparisons
