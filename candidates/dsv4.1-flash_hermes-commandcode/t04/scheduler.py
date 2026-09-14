import heapq


def schedule(graph):
    """Return a topological ordering of the nodes in ``graph``.

    ``graph`` maps every node to an iterable of the nodes it depends on.  The
    ordering is built with Kahn's algorithm, and whenever several nodes are
    ready to run the lexicographically smallest one is emitted first.

    The input mapping (and the dependency iterables it contains) is never
    mutated.

    Raises:
        KeyError: if a dependency is not itself a node in ``graph``.
        ValueError: if the graph contains a cycle and no complete ordering
            exists.
    """
    # Copy the graph up front: this both guarantees the caller's structures are
    # left untouched and gives us a stable view to work from.  Missing
    # dependencies are validated before any ordering so they are reported even
    # when the graph also happens to contain a cycle.
    dependencies = {}
    for node, deps in graph.items():
        deps = list(deps)
        dependencies[node] = deps
        for dep in deps:
            if dep not in graph:
                raise KeyError(dep)

    # remaining[node] counts dependencies that have not been scheduled yet;
    # dependents[dep] lists the nodes waiting on ``dep``.
    remaining = {node: len(deps) for node, deps in dependencies.items()}
    dependents = {node: [] for node in dependencies}
    for node, deps in dependencies.items():
        for dep in deps:
            dependents[dep].append(node)

    # A min-heap always hands back the lexicographically smallest ready node.
    ready = [node for node, count in remaining.items() if count == 0]
    heapq.heapify(ready)

    order = []
    while ready:
        node = heapq.heappop(ready)
        order.append(node)
        for dependent in dependents[node]:
            remaining[dependent] -= 1
            if remaining[dependent] == 0:
                heapq.heappush(ready, dependent)

    if len(order) != len(dependencies):
        raise ValueError("graph contains a cycle")

    return order
