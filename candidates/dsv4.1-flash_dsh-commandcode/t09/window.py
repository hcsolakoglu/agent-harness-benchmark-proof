"""Longest substring without repeated Unicode code points."""


def longest_unique(text):
    """Return a longest substring of ``text`` with no repeated code points.

    A "code point" is a single element of the string, so characters
    outside the Basic Multilingual Plane (e.g. emoji) each count as one
    unit, exactly like ``len``/``set`` treating the string as a sequence
    of code points.

    Ties are broken by returning the leftmost (earliest) longest
    substring.

    The implementation is a classic sliding window: ``start`` is the
    beginning of the current window, which is always duplicate-free, and
    ``last`` maps each code point to the index where it was most recently
    seen.  Extending the window to ``index`` only invalidates the window
    when the incoming code point occurs at or after ``start``; in that
    case the window can safely jump to just past that occurrence.  Each
    index is visited once and each window position moves forward
    monotonically, so the running time is O(n) and the extra space is
    O(min(n, alphabet size)).

    Args:
        text: Any indexable sequence of hashable items, normally a
            ``str``.

    Returns:
        The earliest longest duplicate-free substring of ``text``
        (``text[best_start:best_start + best_len]``).
    """
    last = {}
    start = 0
    best_start = 0
    best_len = 0

    for index, char in enumerate(text):
        previous = last.get(char, -1)
        if previous >= start:
            # ``char`` already occurs inside the window; shrink the
            # window to just past that occurrence.  Positions before
            # ``previous`` are unaffected because the suffix starting
            # there would still contain the duplicate pair.
            start = previous + 1
        last[char] = index

        length = index - start + 1
        # Strict ``>`` keeps the earliest window when lengths tie, since
        # windows are discovered in order of increasing end index.
        if length > best_len:
            best_len = length
            best_start = start

    return text[best_start:best_start + best_len]
