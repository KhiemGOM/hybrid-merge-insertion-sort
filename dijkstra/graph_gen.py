"""Random connected, weighted, directed graphs with exactly |V| and |E|."""

import random


def generate_edges(n, m, max_w=100, seed=None):
    """Return a set-free list of (u, v, w) with m distinct edges, no
    self-loops. A random spanning path guarantees every vertex is reachable
    from vertex 0, so n-1 <= m <= n(n-1) is required."""
    if not (n - 1 <= m <= n * (n - 1)):
        raise ValueError("need n-1 <= m <= n(n-1)")
    rng = random.Random(seed)
    order = list(range(n))
    rng.shuffle(order)
    order.remove(0)
    order.insert(0, 0)
    used = set()
    edges = []
    for a, b in zip(order, order[1:]):
        used.add((a, b))
        edges.append((a, b, rng.randint(1, max_w)))
    if m - len(edges) > 0.5 * n * (n - 1):      # dense: sample from the rest
        rest = [(u, v) for u in range(n) for v in range(n)
                if u != v and (u, v) not in used]
        for u, v in rng.sample(rest, m - len(edges)):
            edges.append((u, v, rng.randint(1, max_w)))
    else:                                        # sparse: rejection sampling
        while len(edges) < m:
            u, v = rng.randrange(n), rng.randrange(n)
            if u != v and (u, v) not in used:
                used.add((u, v))
                edges.append((u, v, rng.randint(1, max_w)))
    return edges


def to_matrix(n, edges):
    mat = [[0] * n for _ in range(n)]
    for u, v, w in edges:
        mat[u][v] = w
    return mat


def to_adj_lists(n, edges):
    adj = [[] for _ in range(n)]
    for u, v, w in edges:
        adj[u].append((v, w))
    return adj
