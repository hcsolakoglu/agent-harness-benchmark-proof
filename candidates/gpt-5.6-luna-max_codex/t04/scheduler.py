import heapq


def schedule(graph):
    """Return a lexicographically minimal topological ordering of ``graph``.

    ``graph`` maps each node to the nodes that must precede it.  The input is
    only read; all bookkeeping is kept in local data structures.
    """
    nodes = set(graph)
    indegree = {node: 0 for node in nodes}
    dependents = {node: [] for node in nodes}

    for node, dependencies in graph.items():
        for dependency in dependencies:
            if dependency not in nodes:
                raise KeyError(dependency)
            indegree[node] += 1
            dependents[dependency].append(node)

    ready = [node for node, degree in indegree.items() if degree == 0]
    heapq.heapify(ready)
    ordering = []

    while ready:
        node = heapq.heappop(ready)
        ordering.append(node)

        for dependent in dependents[node]:
            indegree[dependent] -= 1
            if indegree[dependent] == 0:
                heapq.heappush(ready, dependent)

    if len(ordering) != len(nodes):
        raise ValueError("graph contains a cycle")

    return ordering
