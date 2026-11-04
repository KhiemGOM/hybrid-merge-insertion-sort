"""
Part (4): Unbounded knapsack, bottom-up dynamic programming.

Recurrence (part 1):
    P(0) = 0
    P(C) = max( 0, max_{i : w_i <= C} ( P(C - w_i) + p_i ) )

Bottom-up: fill P[0], P[1], ..., P[C] in increasing order of capacity,
so every P[c - w_i] needed is already computed.
Time O(n * C), space O(C).
"""


def knapsack(C, weights, profits):
    """Return (P, choice) where P[c] is the max profit for capacity c and
    choice[c] is the item type taken last to reach P[c] (-1 if none)."""
    n = len(weights)
    P = [0] * (C + 1)
    choice = [-1] * (C + 1)

    for c in range(1, C + 1):
        for i in range(n):
            if weights[i] <= c and P[c - weights[i]] + profits[i] > P[c]:
                P[c] = P[c - weights[i]] + profits[i]
                choice[c] = i

    return P, choice


def reconstruct(C, weights, choice):
    """Follow choice[] back from capacity C; returns count of each item type."""
    counts = [0] * len(weights)
    c = C
    while c > 0 and choice[c] != -1:
        i = choice[c]
        counts[i] += 1
        c -= weights[i]
    return counts


def run(label, C, weights, profits):
    P, choice = knapsack(C, weights, profits)
    counts = reconstruct(C, weights, choice)

    print(f"=== {label}: P({C}) ===")
    print(f"weights = {weights}")
    print(f"profits = {profits}")
    print()

    print("DP table (bottom-up):")
    print(f"{'C':>4} | {'P(C)':>5} | last item taken")
    print("-" * 32)
    for c in range(C + 1):
        item = "-" if choice[c] == -1 else f"{choice[c]} (w={weights[choice[c]]}, p={profits[choice[c]]})"
        print(f"{c:>4} | {P[c]:>5} | {item}")
    print()

    print(f"Maximum profit P({C}) = {P[C]}")
    print("Items packed:")
    total_w = 0
    for i, k in enumerate(counts):
        if k:
            total_w += k * weights[i]
            print(f"  {k} x item {i} (w={weights[i]}, p={profits[i]})")
    print(f"  total weight = {total_w} / {C}")
    print()
    return P[C]


if __name__ == "__main__":
    # (4a) P(16) with the weights/profits from part (2)
    run("(4a)", 16, [4, 5, 8], [7, 6, 9])

    # (4b) P(12) with the second set of weights/profits
    run("(4b)", 12, [5, 6, 7], [7, 6, 9])
