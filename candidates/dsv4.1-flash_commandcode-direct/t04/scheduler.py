import heapq


def schedule(graph):
    dependencies = {}
    for node, deps in graph.items():
        unique = set()
        for dep in deps:
            if dep not in graph:
                raise KeyError(dep)
            unique.add(dep)
        dependencies[node] = unique

    indegree = {node: len(deps) for node, deps in dependencies.items()}
    dependents = {node: [] for node in graph}
    for node, deps in dependencies.items():
        for dep in deps:
            dependents[dep].append(node)

    ready = [node for node, degree in indegree.items() if degree == 0]
    heapq.heapify(ready)

    out = []
    while ready:
        node = heapq.heappop(ready)
        out.append(node)
        for dependent in dependents[node]:
            indegree[dependent] -= 1
            if indegree[dependent] == 0:
                heapq.heappush(ready, dependent)

    if len(out) != len(graph):
        raise ValueError("graph contains a cycle")

    return out
