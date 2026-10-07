"""
Dijkstra's algorithm, part (b): array of adjacency lists + minimizing heap.

The heap has no decrease-key, so a successful relaxation just pushes a fresh
(dist, vertex) entry and the old one is left behind. When an old entry
comes back out, its dist is bigger than dist[v] and we skip it (stale check).

    - every successful relaxation = one push, so pushes = 1 + K
    - every pop is followed by one stale check, so stale checks = 1 + K
    - each vertex is expanded once, so relaxation checks = |E| (all reachable)
    - push / pop cost O(log heap size), heap size <= 1 + K <= 1 + |E|
    - total: O((V + E) log V)

Comparison counting follows lab2/partb.py: heap comparisons are the key
comparisons inside sift-up / sift-down, stale and relaxation checks are
counted separately, total is the sum of all three.
"""

from collections import namedtuple

INF = float("inf")
Counts = namedtuple("Counts", "heap relax stale total updates")


class MinHeap:
    def __init__(self):
        self.heap = []
        self.comparisons = 0

    def __len__(self):
        return len(self.heap)

    def insert(self, item):
        self.heap.append(item)
        self._sift_up(len(self.heap) - 1)

    def pop(self):
        if not self.heap:
            raise IndexError("Popped from empty heap")
        min_item = self.heap[0]
        last_item = self.heap.pop()
        if self.heap:
            self.heap[0] = last_item
            self._sift_down(0)
        return min_item

    def _sift_up(self, idx):
        while idx > 0:
            parent = (idx - 1) // 2
            self.comparisons += 1
            if self.heap[idx][0] < self.heap[parent][0]:
                self.heap[idx], self.heap[parent] = self.heap[parent], self.heap[idx]
                idx = parent
            else:
                break

    def _sift_down(self, idx):
        n = len(self.heap)
        while True:
            left, right = 2 * idx + 1, 2 * idx + 2
            smallest = idx
            if left < n:
                self.comparisons += 1
                if self.heap[left][0] < self.heap[smallest][0]:
                    smallest = left
            if right < n:
                self.comparisons += 1
                if self.heap[right][0] < self.heap[smallest][0]:
                    smallest = right
            if smallest == idx:
                break
            self.heap[idx], self.heap[smallest] = self.heap[smallest], self.heap[idx]
            idx = smallest


def dijkstra_heap(adj, source):
    """adj[u] is a list of (v, weight). Returns (dist, counts); dist[v] is
    INF when v is unreachable. counts.updates is K, the number of successful
    relaxations."""
    n = len(adj)
    dist = [INF] * n
    dist[source] = 0
    heap = MinHeap()
    heap.insert((0, source))
    relax = stale = updates = 0

    while len(heap) > 0:
        d, u = heap.pop()
        stale += 1
        if d > dist[u]:
            continue
        for v, w in adj[u]:
            relax += 1
            if d + w < dist[v]:
                dist[v] = d + w
                updates += 1
                heap.insert((dist[v], v))

    return dist, Counts(heap.comparisons, relax, stale,
                        heap.comparisons + relax + stale, updates)
