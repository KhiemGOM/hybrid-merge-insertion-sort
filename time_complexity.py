import matplotlib.pyplot as plt
from matplotlib.ticker import StrMethodFormatter

from hybrid_sort import hybrid_sort
from generate_data import SIZES
from plotter import plot_bar_graph

# Part ci
threshold = 42
comparisons = {}
for size in SIZES:
    file_path = f"data/data_{size}.txt"
    
    with open(file_path) as file:
        data = file.read().split("\n")

        c_count = hybrid_sort(data, threshold=threshold)
        comparisons[size] = c_count

plot_bar_graph(comparisons, x_label="Array Size")


# Part cii
thresholds = [i for i in range(1, 251, 50)]
comparisons = {}
for threshold in thresholds:
    file_path = f"data/data_50000.txt"

    with open(file_path) as file:
        data = file.read().split("\n")

        c_count = hybrid_sort(data, threshold=threshold)
        comparisons[threshold] = c_count

plot_bar_graph(comparisons=comparisons, x_label="Threshold Size")