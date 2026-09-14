"""Bounded-concurrency asynchronous mapping helper.

Public API
----------
``bounded_map(fn, items, limit)``

Runs ``fn`` over every element of ``items`` concurrently, keeping at most
``limit`` invocations in flight at any moment, and returns a list of results
in the *same order* as the input.
"""

import asyncio
from collections import deque

__all__ = ["bounded_map"]


async def bounded_map(fn, items, limit):
    """Apply the async callable ``fn`` to each element of ``items``.

    Parameters
    ----------
    fn:
        An async callable invoked as ``await fn(item)``.
    items:
        Any (synchronous or asynchronous) iterable of inputs.  Items are
        pulled lazily, so only a bounded window is ever materialised.
    limit:
        Maximum number of ``fn`` invocations running concurrently.  Must be
        an integer ``>= 1``.

    Returns
    -------
    list
        ``[await fn(x) for x in items]`` preserving input order.

    Raises
    ------
    ValueError
        If ``limit < 1``.
    """
    if limit < 1:
        raise ValueError(f"limit must be >= 1, got {limit!r}")

    iterator = _item_iterator(items)
    semaphore = asyncio.Semaphore(limit)

    async def run(item):
        async with semaphore:
            return await fn(item)

    pending = deque()
    results = []
    try:
        # Prime the window with at most ``limit`` tasks.  Only this bounded
        # number of tasks is ever created ahead of consumption, so arbitrarily
        # large (even infinite) iterables do not spawn unbounded tasks.
        for _ in range(limit):
            item = await _next_item(iterator)
            if item is _SENTINEL:
                break
            pending.append(asyncio.ensure_future(run(item)))

        while pending:
            task = pending.popleft()
            results.append(await task)
            item = await _next_item(iterator)
            if item is _SENTINEL:
                continue
            pending.append(asyncio.ensure_future(run(item)))

        return results
    finally:
        # On failure/cancellation, make sure no orphaned tasks are left
        # running or silently dropping exceptions.
        if pending:
            for task in pending:
                task.cancel()
            await asyncio.gather(*pending, return_exceptions=True)


_SENTINEL = object()


def _item_iterator(items):
    """Return an object supporting ``await _next_item(it)``.

    Supports both synchronous iterables (list, tuple, range, set, dict,
    generators, ...) and asynchronous iterables (async generators).
    """
    if hasattr(items, "__aiter__"):
        return items.__aiter__()
    return iter(items)


async def _next_item(iterator):
    """Fetch the next item, bridging sync and async iterators."""
    if hasattr(iterator, "__anext__"):
        try:
            return await iterator.__anext__()
        except StopAsyncIteration:
            return _SENTINEL
    try:
        return next(iterator)
    except StopIteration:
        return _SENTINEL
