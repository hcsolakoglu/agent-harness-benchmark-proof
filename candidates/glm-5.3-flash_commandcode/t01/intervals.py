def covered_length(intervals):
    """Return the measure (number of integers) of the union of half-open
    intervals [a, b).

    Each (a, b) pair is normalized so that a > b denotes [b, a), and empty
    pairs (a == b) contribute nothing. Runs in O(n log n) time and O(n)
    space using exact integer arithmetic, so enormous coordinates are safe.
    """
    spans = []
    for a, b in intervals:
        if a > b:
            a, b = b, a
        if a < b:
            spans.append((a, b))
    spans.sort()

    total = 0
    merged_lo = merged_hi = None
    for lo, hi in spans:
        if merged_hi is None:
            merged_lo, merged_hi = lo, hi
        elif lo > merged_hi:
            total += merged_hi - merged_lo
            merged_lo, merged_hi = lo, hi
        elif hi > merged_hi:
            merged_hi = hi
    if merged_hi is not None:
        total += merged_hi - merged_lo
    return total
