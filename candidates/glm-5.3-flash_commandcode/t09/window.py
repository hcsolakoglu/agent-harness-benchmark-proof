def longest_unique(text):
    last = {}
    left = 0
    best_start = 0
    best_len = 0
    for right, ch in enumerate(text):
        prev = last.get(ch, -1)
        if prev >= left:
            left = prev + 1
        last[ch] = right
        cur_len = right - left + 1
        if cur_len > best_len:
            best_len = cur_len
            best_start = left
    return text[best_start:best_start + best_len]
