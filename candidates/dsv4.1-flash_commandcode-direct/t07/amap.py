import asyncio


async def bounded_map(fn, items, limit):
    if limit < 1:
        raise ValueError("limit must be at least 1")
    capacity = int(limit)

    if hasattr(items, "__aiter__"):
        aiterator = items.__aiter__()

        async def pull():
            try:
                return True, await aiterator.__anext__()
            except StopAsyncIteration:
                return False, None
    else:
        iterator = iter(items)

        async def pull():
            try:
                return True, next(iterator)
            except StopIteration:
                return False, None

    pending = {}
    results = {}
    submitted = 0
    exhausted = False

    async def fill():
        nonlocal submitted, exhausted
        while not exhausted and len(pending) < capacity:
            more, item = await pull()
            if not more:
                exhausted = True
                return
            task = asyncio.ensure_future(fn(item))
            pending[task] = submitted
            submitted += 1

    try:
        await fill()
        while pending:
            done, _ = await asyncio.wait(
                list(pending), return_when=asyncio.FIRST_COMPLETED
            )
            error = None
            for task in done:
                index = pending.pop(task)
                exc = task.exception()
                if exc is not None:
                    if error is None or index < error[0]:
                        error = (index, exc)
                else:
                    results[index] = task.result()
            if error is not None:
                raise error[1]
            await fill()
    finally:
        if pending:
            for task in pending:
                task.cancel()
            await asyncio.gather(*pending, return_exceptions=True)

    return [results[index] for index in range(submitted)]
