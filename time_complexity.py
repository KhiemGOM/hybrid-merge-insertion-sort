import matplotlib.pyplot as plt
from matplotlib.ticker import StrMethodFormatter, FormatStrFormatter
import numpy as np
import math
import time
import os

from hybrid_sort import hybrid_sort
from generate_data import SIZES
from plotter import plot_bar_graph, plot_line_graph

OUTPUT_DIR = "graphs"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Part ci
# threshold = 42
# comparisons = {}
# for size in SIZES:
#     file_path = f"data/data_{size}.txt"
    
#     with open(file_path) as file:
#         data = [int(x) for x in file.read().split("\n") if x]

#         c_count = hybrid_sort(data, threshold=threshold)
#         comparisons[size] = c_count

# x_raw = list(comparisons.keys())
# y_raw = list(comparisons.values())

# fig1, ax1 = plt.subplots(figsize=(10, 6))

# # Plot only the scatter points
# ax1.scatter(x_raw, y_raw, color='tab:blue', s=5, label='Empirical Data')

# ax1.xaxis.set_major_formatter(StrMethodFormatter('{x:,.0f}'))
# ax1.yaxis.set_major_formatter(StrMethodFormatter('{x:,.0f}'))
# ax1.set_title('Key Comparisons vs Array Size (S = 42)')
# ax1.set_xlabel('Array Size (N)')
# ax1.set_ylabel('Number of Key Comparisons')
# ax1.grid(True, linestyle='--', alpha=0.7)
# ax1.legend()

# plt.tight_layout()
# plt.savefig(f"{OUTPUT_DIR}/cia.png")
# plt.show()

# # Part ci (Evaluation)
# # We expect the hybrid algorithm's time complexity to be O(nlogn), same as merge sort despite 
# # swapping to insertion sort (which has a time complexity of O(n^2)) for subarray sizes below a 
# # threshold S, because ________. 
# # And from the tests below, we can see that the hybrid algorithm is 
# # indeed having a time complexity of O(nlogn), proven empirically.

# # 1. Calculate the constant multiplier
# growth_ratio = [count / (size * math.log2(size)) for size, count in comparisons.items()]
# grow_ratio_val = growth_ratio[-1]

# fig2, ax2 = plt.subplots(figsize=(10, 6))

# # 2. Re-plot the scatter points (zorder=3 puts dots on top of the line)
# ax2.scatter(x_raw, y_raw, color='tab:blue', s=5, label='Empirical Data', zorder=3)

# # 3. Generate smooth X values and calculate Y values for the theoretical line
# x_line = np.linspace(min(x_raw), max(x_raw), 500)
# y_line = [grow_ratio_val * x * math.log2(x) for x in x_line]

# # 4. Plot the line with the formatted equation
# equation_text = r"$y = {:.2f} \cdot n \log_2 n$".format(grow_ratio_val)
# ax2.plot(x_line, y_line, color='red', linestyle='-', linewidth=2, label=equation_text, zorder=2)

# ax2.xaxis.set_major_formatter(StrMethodFormatter('{x:,.0f}'))
# ax2.yaxis.set_major_formatter(StrMethodFormatter('{x:,.0f}'))
# ax2.set_title('Empirical Data vs Theoretical Time Complexity')
# ax2.set_xlabel('Array Size (N)')
# ax2.set_ylabel('Number of Key Comparisons')
# ax2.grid(True, linestyle='--', alpha=0.7)
# ax2.legend()

# plt.tight_layout()
# plt.savefig(f"{OUTPUT_DIR}/cib.png")
# plt.show()

# # Part cii
# thresholds = [i for i in range(1, 101, 20)]
# comparisons = {}
# for threshold in thresholds:
#     file_path = f"data/data_50000.txt"

#     with open(file_path) as file:
#         data = [int(x) for x in file.read().split("\n") if x]

#         c_count = hybrid_sort(data, threshold=threshold)
#         comparisons[threshold] = c_count

# x_vals = list(comparisons.keys())
# y_vals = list(comparisons.values())

# fig, ax = plt.subplots(figsize=(10, 6))

# # Plotting the numerical line graph with size 5 markers
# ax.plot(x_vals, y_vals, marker='o', markersize=5, linestyle='-', color='tab:blue', label='Empirical Data')

# # Formatting the y-axis to display commas
# ax.set_xticks(x_vals)
# ax.yaxis.set_major_formatter(StrMethodFormatter('{x:,.0f}'))

# # Adding titles, labels, and the requested legend
# ax.set_title('Key Comparisons by Threshold Size (S) (n = 50k)')
# ax.set_xlabel('Threshold Size (S)')
# ax.set_ylabel('Number of Key Comparisons')

# ax.grid(True, linestyle='--', alpha=0.7)
# ax.legend()

# plt.tight_layout()
# plt.savefig(f"{OUTPUT_DIR}/cii.png")
# plt.show()

# # Part cii (Evaluation)
# # We expect that swapping merge sort with insertion sort for sub-array sizes below a threshold S will increase
# # the number of key comparisons for the overall algorithm because __________. And indeed, the results shown in 
# # our experiment before confirms it. Sorting an array of size 50,000 requires the least key comparisons when 
# # using a threshold of 1, essentially relying on pure merge sort. This result is consistent for other array 
# # sizes as well.

# fig, ax = plt.subplots(figsize=(10, 6))
# thresholds = [i for i in range(1, 101, 5)]

# # Part ciii
# for size in SIZES[:-4]:
#     timing = {}
#     for threshold in thresholds:
#         file_path = f"data/data_{size}.txt"

#         with open(file_path) as file:
#             data = [int(x) for x in file.read().split("\n") if x]

#             total_time = 0
#             for i in range(10):
#                 arr = data[:]

#                 start_time = time.perf_counter()
#                 hybrid_sort(arr, threshold=threshold)
#                 elapsed_time = time.perf_counter() - start_time
#                 total_time += elapsed_time
#             timing[threshold] = (total_time / 10 / size) * 1000

#     x_vals = list(timing.keys())
#     y_vals = list(timing.values())
#     ax.plot(x_vals, y_vals, marker='o', markersize=5, linestyle='-', label=f'N = {size:,}')

# # 3. Format the entire graph OUTSIDE the loop
# ax.set_xticks(thresholds)
# ax.yaxis.set_major_formatter(FormatStrFormatter('%.4f')) # Correct formatter for decimals

# ax.set_title("Time per Element vs Threshold Size (S)")
# ax.set_xlabel("Threshold Size (S)")
# ax.set_ylabel("Time per element (milliseconds)")

# ax.grid(True, linestyle='--', alpha=0.7)
# ax.legend() # This will automatically list all the 'N = ...' labels

# plt.tight_layout()
# plt.savefig(f"{OUTPUT_DIR}/ciii_merged_performance.png")
# plt.show()


## Optimum S

thresholds = [i for i in range(6, 21)]
timing = {}
for threshold in thresholds:
    file_path = f"data/data_1000000.txt"

    with open(file_path) as file:
        data = [int(x) for x in file.read().split("\n") if x]

        total_time = 0
        for i in range(10):
            arr = data[:]

            start_time = time.perf_counter()
            hybrid_sort(arr, threshold=threshold)
            elapsed_time = time.perf_counter() - start_time
            total_time += elapsed_time
        timing[threshold] = total_time / 10

plot_line_graph(timing, x_label="Threshold Size", y_label="Average Sorting Time", title="Sorting Time vs Threshold Size (n = 1 million)", save_path=f"{OUTPUT_DIR}/Investigating.png")