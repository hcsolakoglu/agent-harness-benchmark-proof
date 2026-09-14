def covered_length(intervals):
    # BUG: quadratic point expansion and wrong for reversed/huge intervals
    points = set()
    for a, b in intervals:
        for x in range(a, b):
            points.add(x)
    return len(points)
