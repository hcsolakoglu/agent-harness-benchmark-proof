import asyncio
async def bounded_map(fn, items, limit):
    return [await fn(x) for x in items]
