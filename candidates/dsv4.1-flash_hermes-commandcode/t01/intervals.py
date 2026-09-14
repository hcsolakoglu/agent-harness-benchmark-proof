def covered_length(intervals):
    """Return the measure of the union of half-open integer intervals.

    Each interval is treated as the set of integers in ``[a, b)`` touch as the
    measure it contributes.  Intervals are normalized so that reversed pairs
    (``a >= b``) contribute nothing, then sorted by start and merged; the total
    is the sum of the merged segment lengths.  Runs in O(n log n) time and O(n)
    auxiliary space, so enormous and duplicated inputs are handled without
    expanding individual points.
    """
    cleaned = [(a, b) for a, b in intervals if b > a]
    if not cleaned:
        return 0

    cleaned.sort()
    total = 0
    cur_start, cur_end = cleaned[0]
    for start, end in cleaned[1:]:
        if start <= cur_end:
            if end > cur_end:
                cur_end = end
        else:
            total += cur_end - cur_start
            cur_start, cur_end = start, end
    total += cur_end - cur_start
    return total
