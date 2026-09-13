"""
Generates the random test datasets used to benchmark hybrid_sort.py.

Sizes go from 1,000 up to 10,000,000, roughly doubling/5x-ing each step so
the timing curve has enough points to actually show a trend without
generating a hundred files. Every dataset draws from the same range,
[1, 10,000,000] (x = 10,000,000), so growing the array size is the only
thing changing between runs, not the value range.
"""

import os
import random

SIZES = [
    1_000,
    5_000,
    10_000,
    50_000,
    100_000,
    500_000,
    1_000_000,
    5_000_000,
    10_000_000,
]

MAX_VALUE = 10_000_000  # x - upper bound for every generated dataset

OUTPUT_DIR = "data"


def generate_dataset(size, max_value=MAX_VALUE, seed=None):
    """Returns a list of `size` random ints in [1, max_value]."""
    rng = random.Random(seed)
    return [rng.randint(1, max_value) for _ in range(size)]


def save_dataset(data, path):
    with open(path, "w") as f:
        f.write("\n".join(map(str, data)))


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    for size in SIZES:
        # seeding with the size itself just so re-running this script
        # gives back the exact same files instead of new random ones
        data = generate_dataset(size, seed=size)
        path = os.path.join(OUTPUT_DIR, f"data_{size}.txt")
        save_dataset(data, path)
        print(f"wrote {path} ({size:,} numbers)")


if __name__ == "__main__":
    main()
