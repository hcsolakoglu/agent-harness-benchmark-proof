import asyncio


async def bounded_map(fn, items, limit):
    """Apply async *fn* to each item of *items* with at most *limit* calls
    in flight, returning results in input order.

    Items are pulled lazily from *items*, so at most *limit* tasks exist
    at any time regardless of iterable size. Raises ValueError if limit < 1.
    """
    if limit < 1:
        raise ValueError("limit must be at least 1")

    iterator = iter(items)
    results = []
    pending = {}
    exhausted = False

    try:
        while True:
            while len(pending) < limit and not exhausted:
                try:
                    item = next(iterator)
                except StopIteration:
                    exhausted = True
                    break
                index = len(results)
                results.append(None)
                pending[asyncio.ensure_future(fn(item))] = index

            if not pending:
                break

            done, _ = await asyncio.wait(pending, return_when=asyncio.FIRST_COMPLETED)
            for task in done:
                results[pending.pop(task)] = task.result()
    except BaseException:
        for task in pending:
            task.cancel()
        if pending:
            await asyncio.gather(*pending, return_exceptions=True)
        raise

    return results
