import asyncio


async def bounded_map(fn, items, limit):
    if limit < 1:
        raise ValueError("limit must be at least 1")

    iterator = iter(items)
    results = []
    pending = {}
    exhausted = False

    def schedule_next():
        nonlocal exhausted

        if exhausted:
            return False

        try:
            item = next(iterator)
        except StopIteration:
            exhausted = True
            return False

        index = len(results)
        results.append(None)
        task = asyncio.create_task(fn(item))
        pending[task] = index
        return True

    try:
        for _ in range(limit):
            if not schedule_next():
                break

        while pending:
            done, _ = await asyncio.wait(
                pending, return_when=asyncio.FIRST_COMPLETED
            )

            for task in done:
                index = pending.pop(task)
                results[index] = task.result()

            for _ in range(len(done)):
                if not schedule_next():
                    break
    except BaseException:
        tasks = tuple(pending)
        for task in tasks:
            task.cancel()
        if tasks:
            await asyncio.gather(*tasks, return_exceptions=True)
        raise

    return results
