import matplotlib.pyplot as plt
from matplotlib.ticker import StrMethodFormatter
import numpy as np
import math
import time
import os

from hybrid_sort import hybrid_sort
from generate_data import SIZES
from plotter import plot_bar_graph

OUTPUT_DIR = "graphs"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Part ci
threshold = 42
comparisons = {}
for size in SIZES[:-2]:
    file_path = f"data/data_{size}.txt"
    
    with open(file_path) as file:
        data = file.read().split("\n")

        c_count = hybrid_sort(data, threshold=threshold)
        comparisons[size] = c_count

fig, ax = plot_bar_graph(comparisons, x_label="Array Size", y_label="Number of Key Comparison", save_path=f"{OUTPUT_DIR}/Array_size.png")

# Part ci (Evaluation)
# We expect the hybrid algorithm's time complexity to be O(nlogn), same as merge sort despite 
# swapping to insertion sort (which has a time complexity of O(n^2)) for subarray sizes below a 
# threshold S, because ________. 
# And from the tests below, we can see that the hybrid algorithm is 
# indeed having a time complexity of O(nlogn), proven empirically.

growth_ratio = []
for size, count in comparisons.items():
    growth_ratio.append(count / (size * math.log2(size)))

grow_ratio_val = np.mean(growth_ratio)

x_vals = [f"{n:,}" for n in comparisons.keys()]
y_vals = [grow_ratio_val * x * math.log2(x) for x in comparisons.keys()]

ax.plot(x_vals, y_vals, color="red")

fig.savefig(f"{OUTPUT_DIR}/Trend.png")


# Part cii
thresholds = [i for i in range(1, 101, 20)]
comparisons = {}
for threshold in thresholds:
    file_path = f"data/data_50000.txt"

    with open(file_path) as file:
        data = file.read().split("\n")

        c_count = hybrid_sort(data, threshold=threshold)
        comparisons[threshold] = c_count

plot_bar_graph(comparisons=comparisons, x_label="Threshold Size", y_label="Number of Key Comparison", save_path=f"{OUTPUT_DIR}/Threshold_size.png")

# Part cii (Evaluation)
# We expect that swapping merge sort with insertion sort for sub-array sizes below a threshold S will increase
# the number of key comparisons for the overall algorithm because __________. And indeed, the results shown in 
# our experiment before confirms it. Sorting an array of size 50,000 requires the least key comparisons when 
# using a threshold of 1, essentially relying on pure merge sort. This result is consistent for other array 
# sizes as well.


# Part ciii
for size in SIZES[:-4]:
    thresholds = [i for i in range(1, 101, 5)]
    timing = {}
    for threshold in thresholds:
        file_path = f"data/data_{size}.txt"

        with open(file_path) as file:
            data = file.read().split("\n")

            total_time = 0
            for i in range(5):
                start_time = time.perf_counter()
                hybrid_sort(data, threshold=threshold)
                elapsed_time = time.perf_counter() - start_time
                total_time += elapsed_time
            timing[threshold] = total_time / 5 / size

    plot_bar_graph(comparisons=timing, x_label="Threshold Size", y_label="Average Time per element", save_path=f"{OUTPUT_DIR}/Performance ({size}).png")


thresholds = [i for i in range(20, 50)]
timing = {}
for threshold in thresholds:
    file_path = f"data/data_1000000.txt"

    with open(file_path) as file:
        data = file.read().split("\n")

        total_time = 0
        for i in range(10):
            start_time = time.perf_counter()
            hybrid_sort(data, threshold=threshold)
            elapsed_time = time.perf_counter() - start_time
            total_time += elapsed_time
        timing[threshold] = total_time / 10

plot_bar_graph(comparisons=timing, x_label="Threshold Size", y_label="Sorting Time", save_path=f"{OUTPUT_DIR}/Investigating.png")