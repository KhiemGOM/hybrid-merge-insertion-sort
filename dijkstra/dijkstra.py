"""
Two implementations of Dijkstra's algorithm (single source shortest paths).

(a) Adjacency matrix + array as priority queue
    - extract-min is a linear scan of the array          -> O(V) each
    - decrease-key is a direct array write               -> O(1) each
    - total: O(V^2) regardless of |E|

(b) Array of adjacency lists + minimizing binary heap
    - extract-min is a heap pop                          -> O(log V) each
    - decrease-key is a sift-up (heap keeps position map)-> O(log V) each
    - total: O((V + E) log V)

Every function returns (dist, parent, comparisons) where `comparisons` is the
number of key comparisons made (distance comparisons in the priority queue
and in edge relaxation). This is the empirical measure used in experiments.
"""

INF = float("inf")


# ---------------------------------------------------------------------------
# (a) Adjacency matrix + array priority queue
# ---------------------------------------------------------------------------
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


# ---------------------------------------------------------------------------
# (b) Adjacency lists + minimizing binary heap (with decrease-key)
# ---------------------------------------------------------------------------
class MinHeap:
    """Binary min-heap of vertices keyed by dist[]; pos[] maps vertex -> index
    so decrease-key runs in O(log V)."""

    def __init__(self, dist):
        self.dist = dist
        self.heap = []
        self.pos = {}
        self.comparisons = 0

    def __len__(self):
        return len(self.heap)

    def _less(self, i, j):
        self.comparisons += 1
        return self.dist[self.heap[i]] < self.dist[self.heap[j]]

    def _swap(self, i, j):
        h = self.heap
        h[i], h[j] = h[j], h[i]
        self.pos[h[i]] = i
        self.pos[h[j]] = j

    def _sift_up(self, i):
        while i > 0:
            p = (i - 1) // 2
            if self._less(i, p):
                self._swap(i, p)
                i = p
            else:
                break

    def _sift_down(self, i):
        n = len(self.heap)
        while True:
            l, r, m = 2 * i + 1, 2 * i + 2, i
            if l < n and self._less(l, m):
                m = l
            if r < n and self._less(r, m):
                m = r
            if m == i:
                break
            self._swap(i, m)
            i = m

    def push(self, v):
        self.heap.append(v)
        self.pos[v] = len(self.heap) - 1
        self._sift_up(len(self.heap) - 1)

    def pop_min(self):
        top = self.heap[0]
        last = self.heap.pop()
        del self.pos[top]
        if self.heap:
            self.heap[0] = last
            self.pos[last] = 0
            self._sift_down(0)
        return top

    def decrease_key(self, v):
        """dist[v] was lowered by the caller; restore heap order."""
        self._sift_up(self.pos[v])


def dijkstra_list_heap(adj, source):
    """adj[u] = list of (v, weight)."""
    n = len(adj)
    dist = [INF] * n
    parent = [-1] * n
    dist[source] = 0
    heap = MinHeap(dist)
    heap.push(source)
    done = [False] * n
    comparisons = 0

    while len(heap):
        u = heap.pop_min()
        done[u] = True
        for v, w in adj[u]:
            if done[v]:
                continue
            comparisons += 1
            nd = dist[u] + w
            if nd < dist[v]:
                first_time = dist[v] == INF
                dist[v] = nd
                parent[v] = u
                if first_time:
                    heap.push(v)
                else:
                    heap.decrease_key(v)
    return dist, parent, comparisons + heap.comparisons
