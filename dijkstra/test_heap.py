"""Tests for the heap + adjacency list Dijkstra (part b). Run from this folder:
    python -m unittest test_heap
"""
import heapq
import random
import unittest

from dijkstra_heap import INF, MinHeap, dijkstra_heap
from graph_gen import generate_edges, to_adj_lists


def reference(adj, s):
    d = [INF] * len(adj)
    d[s] = 0
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


def is_heap(items):
    return all(items[(i - 1) // 2][0] <= items[i][0] for i in range(1, len(items)))


class MinHeapBasics(unittest.TestCase):
    def test_pop_empty_raises(self):
        with self.assertRaises(IndexError):
            MinHeap().pop()

    def test_single_element(self):
        h = MinHeap()
        h.insert((5, "a"))
        self.assertEqual(len(h), 1)
        self.assertEqual(h.pop(), (5, "a"))
        self.assertEqual(len(h), 0)

    def test_pops_come_out_in_order(self):
        rng = random.Random(1)
        keys = [rng.randint(1, 1000) for _ in range(500)]
        h = MinHeap()
        for i, k in enumerate(keys):
            h.insert((k, i))
        out = [h.pop()[0] for _ in range(len(keys))]
        self.assertEqual(out, sorted(keys))

    def test_duplicate_keys_all_returned(self):
        h = MinHeap()
        for i in range(10):
            h.insert((3, i))
        self.assertEqual(sorted(h.pop()[1] for _ in range(10)), list(range(10)))

    def test_heap_property_after_every_operation(self):
        rng = random.Random(2)
        h = MinHeap()
        for step in range(300):
            if len(h) and rng.random() < 0.4:
                h.pop()
            else:
                h.insert((rng.randint(1, 50), step))
            self.assertTrue(is_heap(h.heap), f"step {step}")

    def test_len_tracks_inserts_and_pops(self):
        h = MinHeap()
        for i in range(5):
            h.insert((i, i))
        h.pop()
        self.assertEqual(len(h), 4)


class MinHeapComparisonCounts(unittest.TestCase):
    def test_first_insert_costs_nothing(self):
        h = MinHeap()
        h.insert((1, 0))
        self.assertEqual(h.comparisons, 0)

    def test_ascending_inserts_cost_one_each_after_first(self):
        h = MinHeap()
        for k in range(1, 6):
            h.insert((k, k))
        self.assertEqual(h.comparisons, 4)

    def test_pop_on_single_element_costs_nothing(self):
        h = MinHeap()
        h.insert((1, 0))
        h.pop()
        self.assertEqual(h.comparisons, 0)

    def test_small_exact_total(self):
        # inserts of 1,2,3 cost 0+1+1; popping leaves [3,2] and sifting 3 down costs 1
        h = MinHeap()
        for k in (1, 2, 3):
            h.insert((k, k))
        self.assertEqual(h.comparisons, 2)
        h.pop()
        self.assertEqual(h.comparisons, 3)

    def test_descending_inserts_climb_to_the_root(self):
        h = MinHeap()
        h.insert((8, 0))
        h.insert((4, 1))   # 1 comparison, swaps to root
        h.insert((2, 2))   # compares with root, swaps
        self.assertEqual(h.heap[0][0], 2)
        self.assertEqual(h.comparisons, 2)


class DijkstraHeapBasics(unittest.TestCase):
    def test_textbook_graph(self):
        adj = to_adj_lists(4, [(0, 1, 4), (0, 2, 1), (2, 1, 2), (1, 3, 1), (2, 3, 5)])
        dist, _ = dijkstra_heap(adj, 0)
        self.assertEqual(dist, [0, 3, 1, 4])

    def test_single_vertex(self):
        dist, c = dijkstra_heap([[]], 0)
        self.assertEqual(dist, [0])
        self.assertEqual((c.heap, c.relax, c.stale, c.updates), (0, 0, 1, 0))

    def test_unreachable_vertices_stay_infinite(self):
        dist, _ = dijkstra_heap(to_adj_lists(4, [(0, 1, 2)]), 0)
        self.assertEqual(dist, [0, 2, INF, INF])

    def test_edges_are_directed(self):
        dist, _ = dijkstra_heap(to_adj_lists(2, [(0, 1, 3)]), 1)
        self.assertEqual(dist, [INF, 0])

    def test_non_zero_source(self):
        adj = to_adj_lists(3, [(0, 1, 1), (1, 2, 1), (2, 0, 1)])
        dist, _ = dijkstra_heap(adj, 1)
        self.assertEqual(dist, [2, 0, 1])

    def test_indirect_path_beats_direct_edge(self):
        adj = to_adj_lists(3, [(0, 2, 10), (0, 1, 1), (1, 2, 1)])
        dist, _ = dijkstra_heap(adj, 0)
        self.assertEqual(dist[2], 2)

    def test_parallel_edges_use_the_cheaper_one(self):
        adj = to_adj_lists(2, [(0, 1, 9), (0, 1, 4), (0, 1, 7)])
        dist, _ = dijkstra_heap(adj, 0)
        self.assertEqual(dist, [0, 4])

    def test_ties_between_equal_paths(self):
        adj = to_adj_lists(4, [(0, 1, 1), (0, 2, 1), (1, 3, 1), (2, 3, 1)])
        dist, _ = dijkstra_heap(adj, 0)
        self.assertEqual(dist, [0, 1, 1, 2])

    def test_input_is_not_modified(self):
        adj = to_adj_lists(4, [(0, 1, 4), (0, 2, 1), (2, 1, 2), (1, 3, 1)])
        snapshot = [row[:] for row in adj]
        dijkstra_heap(adj, 0)
        self.assertEqual(adj, snapshot)


class DijkstraHeapStaleEntries(unittest.TestCase):
    # 0->1 (10) is pushed first, then 0->2->1 (2) beats it, so (10, 1) goes stale.
    EDGES = [(0, 1, 10), (0, 2, 1), (2, 1, 1), (1, 3, 1)]

    def test_stale_entry_is_skipped_not_reprocessed(self):
        adj = to_adj_lists(4, self.EDGES)
        dist, c = dijkstra_heap(adj, 0)
        self.assertEqual(dist, [0, 2, 1, 3])
        # if the stale (10, 1) were expanded again we'd see more than E checks
        self.assertEqual(c.relax, len(self.EDGES))

    def test_stale_checks_equal_pops(self):
        _, c = dijkstra_heap(to_adj_lists(4, self.EDGES), 0)
        self.assertEqual(c.updates, 4)        # 1 (10), 2, 1 (2), 3
        self.assertEqual(c.stale, 1 + c.updates)


class DijkstraHeapAgainstReference(unittest.TestCase):
    def test_random_graphs_match_heapq(self):
        rng = random.Random(7)
        for trial in range(150):
            n = rng.randint(2, 40)
            m = rng.randint(n - 1, n * (n - 1))
            adj = to_adj_lists(n, generate_edges(n, m, seed=trial))
            s = rng.randrange(n)
            got, _ = dijkstra_heap(adj, s)
            self.assertEqual(got, reference(adj, s), f"trial {trial}")

    def test_big_weights_match_heapq(self):
        adj = to_adj_lists(80, generate_edges(80, 700, max_w=10 ** 9, seed=3))
        self.assertEqual(dijkstra_heap(adj, 0)[0], reference(adj, 0))


class DijkstraHeapInvariants(unittest.TestCase):
    def test_counts_on_random_connected_graphs(self):
        for seed in range(30):
            n, m = 50, 50 + seed * 40
            adj = to_adj_lists(n, generate_edges(n, m, seed=seed))
            _, c = dijkstra_heap(adj, 0)
            self.assertEqual(c.relax, m, f"seed {seed}")
            self.assertEqual(c.stale, 1 + c.updates)
            self.assertEqual(c.total, c.heap + c.relax + c.stale)
            self.assertGreaterEqual(c.updates, n - 1)
            self.assertLessEqual(c.updates, m)
            if m >= 2 * n:
                self.assertGreater(c.heap, 0)

    def test_path_graph_never_needs_a_heap_comparison(self):
        # one entry in the heap at a time, so nothing to compare against
        path = [(i, i + 1, 1) for i in range(30)]
        dist, c = dijkstra_heap(to_adj_lists(31, path), 0)
        self.assertEqual(dist, list(range(31)))
        self.assertEqual(c.heap, 0)

    def test_more_edges_never_means_fewer_relaxation_checks(self):
        few = dijkstra_heap(to_adj_lists(40, generate_edges(40, 60, seed=1)), 0)[1]
        many = dijkstra_heap(to_adj_lists(40, generate_edges(40, 600, seed=1)), 0)[1]
        self.assertGreater(many.relax, few.relax)


if __name__ == "__main__":
    unittest.main()
