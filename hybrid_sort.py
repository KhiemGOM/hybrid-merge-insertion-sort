"""
Hybrid Merge Sort / Insertion Sort.

Plain merge sort keeps recursing all the way down to subarrays of size 1,
and each of those recursive calls has overhead (function calls, list
slicing, etc.) that doesn't actually help once the subarray is tiny.
Insertion sort is bad on large arrays (O(n^2)) but it's actually quick on
small ones because there's barely any data to move around. So the trick
here: once a subarray shrinks to S elements or fewer, stop recursing and
just run insertion sort on it directly.
"""

import random


def insertion_sort(arr, left, right):
    """Sorts arr[left..right] in place. Standard insertion sort."""
    for i in range(left + 1, right + 1):
        key = arr[i]
        j = i - 1
        while j >= left and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key


def merge(arr, left, mid, right):
    """Merges the two already-sorted halves arr[left..mid] and arr[mid+1..right]."""
    left_half = arr[left:mid + 1]
    right_half = arr[mid + 1:right + 1]

    i = j = 0
    k = left

    while i < len(left_half) and j < len(right_half):
        if left_half[i] <= right_half[j]:
            arr[k] = left_half[i]
            i += 1
        else:
            arr[k] = right_half[j]
            j += 1
        k += 1

    # one of the halves still has leftovers, dump them in
    while i < len(left_half):
        arr[k] = left_half[i]
        i += 1
        k += 1

    while j < len(right_half):
        arr[k] = right_half[j]
        j += 1
        k += 1


def hybrid_sort(arr, threshold=43, left=0, right=None):
    """
    Sorts arr[left..right] in place using merge sort, but falls back to
    insertion sort once a subarray's size drops to `threshold` or below.

    threshold=43 commonly cited number (somewhere in the 30-50 range
    tends to work well in practice).
    TODO: Tuning against our own timing results?
    """
    if right is None:
        right = len(arr) - 1

    if right - left + 1 <= threshold:
        insertion_sort(arr, left, right)
        return

    mid = (left + right) // 2
    hybrid_sort(arr, threshold, left, mid)
    hybrid_sort(arr, threshold, mid + 1, right)
    merge(arr, left, mid, right)


if __name__ == "__main__":
    # quick sanity check before trusting this on the real benchmark data
    sample = [random.randint(1, 100_000) for _ in range(2000)]
    result = sample[:]
    hybrid_sort(result, threshold=43)
    assert result == sorted(sample), "hybrid_sort produced a wrong result"
    print("sanity check passed on a random 2000-element array")
