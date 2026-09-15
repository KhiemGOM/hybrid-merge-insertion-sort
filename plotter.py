"""
Takes in a dictionary in format {1000: 13246, 5000: 87514, ....}
whereby the keys represent the array size (for question ci) or 
threshold size (for question cii), and the values represent the 
number of corresponding key comparisons. Plots a bar graph.
"""

import matplotlib.pyplot as plt
from matplotlib.ticker import StrMethodFormatter, FormatStrFormatter

def plot_bar_graph(comparisons, x_label, y_label, save_path):
    x_ticks = [f"{k:,}" for k in comparisons.keys()]
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(x_ticks, comparisons.values())

    ax.set_title(f"Key Comparisons by {x_label}")
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)
    ax.ticklabel_format(style="plain", axis="y")
    ax.yaxis.set_major_formatter(StrMethodFormatter('{x:,.0f}'))
    plt.grid(axis="y", linestyle="--", alpha=0.7)

    fig.tight_layout()
    plt.savefig(save_path)
    plt.show()

    return fig, ax

def plot_line_graph(data, x_label, y_label, title, save_path):
    x_vals = list(data.keys())
    y_vals = list(data.values())

    fig, ax = plt.subplots(figsize=(10, 6))

    # Plotting the numerical line graph with size 5 markers
    ax.plot(x_vals, y_vals, marker='o', markersize=5, linestyle='-', color='tab:blue', label='Empirical Data')

    # Formatting the y-axis to display commas
    ax.set_xticks(x_vals)

    # Adding titles, labels, and the requested legend
    ax.set_title(title)
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)

    ax.grid(True, linestyle='--', alpha=0.7)
    ax.legend()

    plt.tight_layout()
    plt.savefig(save_path)
    plt.show()