import asyncio
from amap import bounded_map
async def f(x): return x*2
assert asyncio.run(bounded_map(f,[1,2,3],2))==[2,4,6]
print('PUBLIC_OK')
