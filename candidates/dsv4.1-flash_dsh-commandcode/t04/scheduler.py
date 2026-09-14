"""Topological scheduling with deterministic lexicographic tie-breaking."""

from heapq import heapify, heappop, heappush


def schedule(graph):
    """Return a topological order of the nodes in ``graph``.

    ``graph`` maps each node to an iterable of the nodes it depends on.  The
    result contains every node exactly once and, whenever several nodes are
    ready at the same time, the lexicographically smallest one is emitted
    first (the greedy order is the lexicographically smallest topological
    order).

    ``KeyError`` is raised if a dependency is not a key of ``graph`` and
    ``ValueError`` if the dependencies contain a cycle.  The input mapping is
    never modified.

    Runs in ``O(V + E)`` time plus ``O(V log V)`` for the ordering heap.
    """
    # Number of unsatisfied dependencies per node; every node starts at zero.
    pending = dict.fromkeys(graph, 0)
    # Reverse adjacency: node -> nodes that depend on it.
    dependents = {node: [] for node in graph}

    # Validate dependencies and build the reverse edges.  Every dependency
    # must be a key of ``graph``, otherwise the node could never be scheduled.
    for node, deps in graph.items():
        for dep in deps:
            if dep not in pending:
                raise KeyError(dep)
            pending[node] += 1
            dependents[dep].append(node)

    # All nodes without dependencies are ready; a heap yields the
    # lexicographically smallest one at each step.
    ready = [node for node, count in pending.items() if count == 0]
    heapify(ready)

    order = []
    while ready:
        node = heappop(ready)
        order.append(node)
        for dependent in dependents[node]:
            pending[dependent] -= 1
            if pending[dependent] == 0:
                heappush(ready, dependent)

    if len(order) != len(pending):
        blocked = sorted(node for node, count in pending.items() if count)
        raise ValueError(f"cyclic dependencies detected among: {blocked!r}")

    return order
