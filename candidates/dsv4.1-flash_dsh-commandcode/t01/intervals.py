"""Utilities for measuring sets of half-open integer intervals."""


def covered_length(intervals):
    """Return the number of integers covered by the union of half-open intervals.

    Each item of *intervals* is a pair ``(a, b)`` denoting the half-open range
    ``[a, b)``, i.e. every integer ``x`` with ``a <= x < b``.  Endpoints may be
    negative and the pair may be reversed (``a > b``), in which case the
    endpoints are normalised to ``[min(a, b), max(a, b))``.  Empty intervals
    (``a == b``) contribute nothing.  Intervals may be duplicated, nested or
    touching; touching intervals such as ``[1, 4)`` and ``[4, 6)`` form the
    contiguous range ``[1, 6)`` and are merged.

    The intervals are sorted and merged in ``O(n log n)`` time using ``O(n)``
    extra space, so endpoints of arbitrary magnitude are handled without
    enumerating the (possibly enormous) number of points they span.

    Args:
        intervals: An iterable of ``(a, b)`` endpoint pairs.

    Returns:
        The measure of the union, i.e. the count of distinct integers covered
        by at least one interval.  Integer inputs yield an ``int`` result.
    """
    ordered = sorted((a, b) if a <= b else (b, a) for a, b in intervals)

    total = 0
    current_start = None
    current_end = None
    for start, end in ordered:
        if start >= end:
            # Degenerate/empty interval contributes no integer.
            continue
        if current_start is None:
            current_start, current_end = start, end
        elif start > current_end:
            # Disjoint from the current run: close it and start a new one.
            total += current_end - current_start
            current_start, current_end = start, end
        elif end > current_end:
            # Overlapping or touching: extend the current run.
            current_end = end

    if current_start is not None:
        total += current_end - current_start
    return total
