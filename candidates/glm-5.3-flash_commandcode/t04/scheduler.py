import heapq


def schedule(graph):
    remaining = {}
    dependents = {node: [] for node in graph}
    for node, deps in graph.items():
        unique = set(deps)
        for dep in unique:
            if dep not in graph:
                raise KeyError(dep)
            dependents[dep].append(node)
        remaining[node] = unique

    ready = [node for node, deps in remaining.items() if not deps]
    heapq.heapify(ready)
    out = []
    while ready:
        node = heapq.heappop(ready)
        out.append(node)
        for dependent in dependents[node]:
            deps = remaining[dependent]
            deps.discard(node)
            if not deps:
                heapq.heappush(ready, dependent)
    if len(out) != len(graph):
        raise ValueError("cycle detected in graph")
    return out
