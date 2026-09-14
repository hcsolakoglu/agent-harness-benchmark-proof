def covered_length(intervals):
    """Measure of the union of half-open integer intervals [a, b).

    Intervals may be given in any order, with endpoints reversed, negative,
    duplicated, nested, or touching. Empty intervals contribute nothing.
    """
    spans = []
    for a, b in intervals:
        if a > b:
            a, b = b, a
        if a < b:
            spans.append((a, b))
    if not spans:
        return 0

    spans.sort()
    total = 0
    cur_start, cur_end = spans[0]
    for start, end in spans[1:]:
        if start <= cur_end:
            if end > cur_end:
                cur_end = end
        else:
            total += cur_end - cur_start
            cur_start, cur_end = start, end
    total += cur_end - cur_start
    return total
