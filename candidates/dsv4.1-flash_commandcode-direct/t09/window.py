def longest_unique(text):
    """Return the earliest longest substring with no repeated code point."""
    last = {}
    start = 0
    best_start = 0
    best_len = 0
    for i, ch in enumerate(text):
        prev = last.get(ch, -1)
        if prev >= start:
            start = prev + 1
        last[ch] = i
        length = i - start + 1
        if length > best_len:
            best_len = length
            best_start = start
    return text[best_start:best_start + best_len]
