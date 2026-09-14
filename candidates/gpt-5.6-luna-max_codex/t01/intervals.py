def covered_length(intervals):
    """Return the size of the union of integer half-open intervals.

    Reversed intervals are treated as having their endpoints swapped.  The
    calculation works on endpoints rather than expanding the intervals, so
    its running time depends on the number of intervals, not their lengths.
    """
    normalized = []
    for a, b in intervals:
        start, end = sorted((a, b))
        if start != end:
            normalized.append((start, end))

    if not normalized:
        return 0

    normalized.sort()
    covered = 0
    current_start, current_end = normalized[0]

    for start, end in normalized[1:]:
        if start > current_end:
            covered += current_end - current_start
            current_start, current_end = start, end
        elif end > current_end:
            current_end = end

    return covered + current_end - current_start
