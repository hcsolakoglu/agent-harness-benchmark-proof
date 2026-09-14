def longest_unique(text):
    """Return one longest substring of ``text`` with no repeated code points.

    On ties the earliest (left-most) substring is returned.

    Runs in O(n) time and space using a sliding window: ``start`` is the
    index where the current duplicate-free window begins, and ``last`` maps
    each code point to the index of its most recent occurrence.
    """
    last = {}
    start = 0
    best_start = 0
    best_len = 0
    for i, ch in enumerate(text):
        prev = last.get(ch)
        if prev is not None and prev >= start:
            start = prev + 1
        last[ch] = i
        length = i - start + 1
        if length > best_len:
            best_len = length
            best_start = start
    return text[best_start:best_start + best_len]
