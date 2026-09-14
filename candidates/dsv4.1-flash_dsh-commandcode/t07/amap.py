"""Concurrency-limited, order-preserving ``async`` mapping over any iterable.

The public entry point is :func:`bounded_map`.  It applies an async callable
to every item of an iterable while running at most ``limit`` calls at the same
time and returns the results in the same order as the input.
"""

from __future__ import annotations

import asyncio
from collections import deque
from typing import Any, AsyncIterable, Awaitable, Callable, Iterable, List, TypeVar, Union

__all__ = ["bounded_map"]

T = TypeVar("T")
R = TypeVar("R")


def _next_item_getter(
    items: Union[Iterable[T], AsyncIterable[T]], exhausted: Any
) -> Callable[[], Awaitable[Any]]:
    """Build an async callable returning the next item or ``exhausted``.

    Synchronous iterables (lists, tuples, ranges, generators, iterators, ...)
    and asynchronous iterables are both supported.  The input is consumed
    lazily, one item per call.
    """
    aiter = getattr(items, "__aiter__", None)
    if aiter is not None:
        async_iterator = aiter()

        async def next_async() -> Any:
            try:
                return await async_iterator.__anext__()
            except StopAsyncIteration:
                return exhausted

        return next_async

    iterator = iter(items)

    async def next_sync() -> Any:
        try:
            return next(iterator)
        except StopIteration:
            return exhausted

    return next_sync


async def bounded_map(
    fn: Callable[[T], Awaitable[R]],
    items: Union[Iterable[T], AsyncIterable[T]],
    limit: int,
) -> List[R]:
    """Map ``fn`` over ``items`` with at most ``limit`` calls in flight.

    Results are returned in input order, regardless of the order in which the
    individual calls finish.  ``items`` may be any synchronous iterable
    (including one-shot iterators and generators) or an asynchronous
    iterable; it is consumed lazily so that, for a huge or infinite input,
    only a bounded number of items is pulled and only a bounded number of
    tasks exists at any moment.

    Args:
        fn: An async callable applied to each item.
        items: Any iterable (sync or async) of items to process.
        limit: Maximum number of concurrent ``fn`` calls; must be >= 1.

    Returns:
        A list with ``fn(item)`` for every item, in the original order.

    Raises:
        ValueError: If ``limit`` is smaller than 1.
    """
    if limit < 1:
        raise ValueError(f"limit must be >= 1, got {limit!r}")

    exhausted: Any = object()  # per-call marker, unique even for odd inputs
    next_item = _next_item_getter(items, exhausted)
    pending: deque[asyncio.Future] = deque()
    results: List[R] = []

    try:
        # Prime the window.  At most ``limit`` calls are ever started ahead of
        # the consumer, no matter how large (or endless) the input is.
        while len(pending) < limit:
            item = await next_item()
            if item is exhausted:
                break
            pending.append(asyncio.ensure_future(fn(item)))

        # Await the oldest call first to preserve input order, then start the
        # next item as soon as a concurrency slot frees up.
        while pending:
            results.append(await pending.popleft())
            item = await next_item()
            if item is not exhausted:
                pending.append(asyncio.ensure_future(fn(item)))
    except BaseException:
        # A failing/cancelled call must not leave sibling work running.
        for task in pending:
            task.cancel()
        # Retrieve the outcome of every task so none is left dangling (this
        # also silences "exception was never retrieved" warnings).
        await asyncio.gather(*pending, return_exceptions=True)
        raise

    return results
