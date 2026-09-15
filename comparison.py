import time
import os
from hybrid_sort import hybrid_sort, merge

def original_merge_sort(arr, left=0, right=None):
    """Standard recursive Merge Sort down to base size 1."""
    if right is None:
        right = len(arr) - 1
    
    if left >= right:
        return 0

    mid = (left + right) // 2
    comparisons = 0
    comparisons += original_merge_sort(arr, left, mid)
    comparisons += original_merge_sort(arr, mid + 1, right)
    comparisons += merge(arr, left, mid, right)
    return comparisons

def run_benchmark():
    file_path = "data/data_10000000.txt"
    
    if not os.path.exists(file_path):
        print(f"File '{file_path}' not found. Please run generate_data.py first!")
        return

    print("Loading 10M dataset into memory...")
    with open(file_path, "r") as f:
        # Convert strings to integers strictly
        data = [int(line) for line in f if line.strip()]

    # Optimal S determined from Part (c)
    OPTIMAL_S = 13 

    print("\n--- Running Original Merge Sort ---")
    data_ms = data.copy() # Fresh copy so it isn't pre-sorted
    start = time.perf_counter()
    comps_ms = original_merge_sort(data_ms)
    time_ms = time.perf_counter() - start
    print(f"Original Merge Sort:")
    print(f"  - Key Comparisons: {comps_ms:,}")
    print(f"  - CPU Time:        {time_ms:.4f} seconds")

    print(f"\n--- Running Hybrid Sort (S = {OPTIMAL_S}) ---")
    data_hs = data.copy() # Fresh copy
    start = time.perf_counter()
    comps_hs = hybrid_sort(data_hs, threshold=OPTIMAL_S)
    time_hs = time.perf_counter() - start
    print(f"Hybrid Sort (S={OPTIMAL_S}):")
    print(f"  - Key Comparisons: {comps_hs:,}")
    print(f"  - CPU Time:        {time_hs:.4f} seconds")

    # Percentage calculations
    comp_diff = ((comps_hs - comps_ms) / comps_ms) * 100
    time_diff = ((time_hs - time_ms) / time_ms) * 100
    print("\n--- Summary Comparison ---")
    print(f"Comparisons Delta: {comp_diff:+.2f}%")
    print(f"CPU Time Delta:    {time_diff:+.2f}%")

if __name__ == "__main__":
    run_benchmark()