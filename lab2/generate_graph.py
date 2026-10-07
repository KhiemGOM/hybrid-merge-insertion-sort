import random

def generate_random_graph(V, E, seed=41):
    rng = random.Random(seed) if seed is not None else random

    graph = [[] for _ in range(V)]
    edges_added = 0
    while edges_added < E:
        u = rng.randint(0, V - 1)
        v = rng.randint(0, V - 1)
        if u != v:
            w = rng.randint(1, 100)
            graph[u].append((v, w))
            edges_added += 1
    return graph