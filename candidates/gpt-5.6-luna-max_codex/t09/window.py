def longest_unique(text):
    """Return the earliest longest substring with unique Unicode code points."""
    last_seen = {}
    window_start = 0
    best_start = 0
    best_length = 0

    for end, code_point in enumerate(text):
        previous = last_seen.get(code_point)
        if previous is not None and previous >= window_start:
            window_start = previous + 1
        last_seen[code_point] = end

        window_length = end - window_start + 1
        if window_length > best_length:
            best_start = window_start
            best_length = window_length

    return text[best_start:best_start + best_length]
