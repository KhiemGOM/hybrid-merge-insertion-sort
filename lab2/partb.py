import time
import matplotlib.pyplot as plt
from generate_graph import generate_random_graph

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
        parent = (idx - 1) // 2
        while idx > 0:
            self.comparisons += 1
            if self.heap[idx][0] < self.heap[parent][0]:
                self.heap[idx], self.heap[parent] = \
                self.heap[parent], self.heap[idx]
                idx = parent
                parent = (idx - 1) // 2
            else:
                break

    def _sift_down(self, idx):
        n = len(self.heap)

        while True:
            left = 2 * idx + 1
            right = 2 * idx + 2
            smallest = idx

            if left < n:
                self.comparisons += 1
                if self.heap[left][0] < self.heap[smallest][0]:
                    smallest = left

            if right < n:
                self.comparisons += 1
                if self.heap[right][0] < self.heap[smallest][0]:
                    smallest = right

            if smallest != idx:
                self.heap[idx], self.heap[smallest] = \
                self.heap[smallest], self.heap[idx]
                idx = smallest
            else:
                break            

def dijkstra(graph, source, num_vertices):
    distance = [float('inf')] * num_vertices
    distance[source] = 0

    relaxation_comparisons = 0
    stale_check_comparisons = 0

    min_heap = MinHeap()
    min_heap.insert((0, source))

    while len(min_heap) > 0:
        current_dist, u = min_heap.pop()  ## Heap comparisons

        stale_check_comparisons += 1  
        if current_dist > distance[u]:   ## Stale check comparisons
            continue

        for v, weight in graph[u]:
            new_dist = current_dist + weight
            relaxation_comparisons += 1
            if new_dist < distance[v]:  ## Relaxation comparisons
                distance[v] = new_dist
                min_heap.insert((new_dist, v))  ## Heap comparisons

    total_graph_comparisons = stale_check_comparisons + relaxation_comparisons
    total_comparisons = total_graph_comparisons + min_heap.comparisons

    return distance, {
        "heap_comparisons": min_heap.comparisons,
        "relaxation_comparisons": relaxation_comparisons,
        "stale_check_comparisons": stale_check_comparisons,
        "total_comparisons": total_comparisons
    }


V = 5000
e_results = {}
for E in range(10000, 500001, 20000):
    g = generate_random_graph(V, E)
    start_time = time.perf_counter()
    distnace, comparisons = dijkstra(g, 0, V)
    elapsed_time = time.perf_counter() - start_time
    comparisons["runtime"] = elapsed_time
    print(f"\nComparison count for {E} edges took {elapsed_time*1000:.2f}ms!\n=========")
    for key, value in comparisons.items():
        print(f"{key}: {value}")
    e_results[E] = comparisons

# Extract x values (number of edges/vertices) and y series
x_vals = sorted(e_results.keys())

metrics = [
    ('total_comparisons', 'Total Comparisons', '#1f77b4', 'o'),
    ('heap_comparisons', 'Heap Comparisons', '#ff7f0e', 's'),
    ('relaxation_comparisons', 'Relaxation Comparisons', '#2ca02c', '^'),
    ('stale_check_comparisons', 'Stale Check Comparisons', '#d62728', 'D')
]

plt.figure(figsize=(9, 6))

# Plot each comparison metric with line and point markers
for key, label, color, marker in metrics:
    y_vals = [e_results[x][key] for x in x_vals]
    plt.plot(x_vals, y_vals, marker=marker, linestyle='-', linewidth=2, markersize=7, label=label, color=color)

plt.title("Dijkstra's Algorithm: Key Comparisons vs. Edges Size", fontsize=14, fontweight='bold', pad=12)
plt.xlabel("Number of Edges (|E|)", fontsize=12)
plt.ylabel("Number of Key Comparisons", fontsize=12)
plt.xticks(x_vals)
plt.grid(True, linestyle='--', alpha=0.6)
plt.legend(frameon=True, fontsize=11)
plt.tight_layout()

plt.show()

############ Plotting Runtime against edges

plt.figure(figsize=(9, 6))

# Plot each comparison metric with line and point markers
y_vals = [e_results[x]["runtime"] for x in x_vals]
plt.plot(x_vals, y_vals, marker="D", linestyle='-', linewidth=2, markersize=7, label="Runtime")

plt.title("Dijkstra's Algorithm: Runtime vs. Edges Size", fontsize=14, fontweight='bold', pad=12)
plt.xlabel("Number of Edges (|E|)", fontsize=12)
plt.ylabel("Time (s)", fontsize=12)
plt.xticks(x_vals)
plt.grid(True, linestyle='--', alpha=0.6)
plt.legend(frameon=True, fontsize=11)
plt.tight_layout()

plt.show()

##########


E = 500000
v_results = {}
for V in range(1000, 50001, 2000):
    g = generate_random_graph(V, E)
    start_time = time.perf_counter()
    distnace, comparisons = dijkstra(g, 0, V)
    elapsed_time = time.perf_counter() - start_time
    comparisons["runtime"] = elapsed_time
    print(f"\nComparison count for {V} vertices took {elapsed_time*1000:.2f}ms!\n=========")
    for key, value in comparisons.items():
        print(f"{key}: {value}")
    v_results[V] = comparisons

x_vals = sorted(v_results.keys())

metrics = [
    ('total_comparisons', 'Total Comparisons', '#1f77b4', 'o'),
    ('heap_comparisons', 'Heap Comparisons', '#ff7f0e', 's'),
    ('relaxation_comparisons', 'Relaxation Comparisons', '#2ca02c', '^'),
    ('stale_check_comparisons', 'Stale Check Comparisons', '#d62728', 'D')
]

plt.figure(figsize=(9, 6))

# Plot each comparison metric with line and point markers
for key, label, color, marker in metrics:
    y_vals = [v_results[x][key] for x in x_vals]
    plt.plot(x_vals, y_vals, marker=marker, linestyle='-', linewidth=2, markersize=7, label=label, color=color)

plt.title("Dijkstra's Algorithm: Key Comparisons vs. Vertices Size", fontsize=14, fontweight='bold', pad=12)
plt.xlabel("Number of Vertices (|V|)", fontsize=12)
plt.ylabel("Number of Key Comparisons", fontsize=12)
plt.xticks(x_vals)
plt.grid(True, linestyle='--', alpha=0.6)
plt.legend(frameon=True, fontsize=11)
plt.tight_layout()

plt.show()


############ Plotting Runtime against edges

plt.figure(figsize=(9, 6))

# Plot each comparison metric with line and point markers
y_vals = [v_results[x]["runtime"] for x in x_vals]
plt.plot(x_vals, y_vals, marker="D", linestyle='-', linewidth=2, markersize=7, label="Runtime")

plt.title("Dijkstra's Algorithm: Runtime vs. Vertices Size", fontsize=14, fontweight='bold', pad=12)
plt.xlabel("Number of Vertices (|V|)", fontsize=12)
plt.ylabel("Time (s)", fontsize=12)
plt.xticks(x_vals)
plt.grid(True, linestyle='--', alpha=0.6)
plt.legend(frameon=True, fontsize=11)
plt.tight_layout()

plt.show()

##########