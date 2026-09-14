import sys,asyncio
sys.path.insert(0,sys.argv[1]); from amap import bounded_map
async def main():
 active=peak=0; lock=asyncio.Lock()
 async def f(x):
  nonlocal active,peak
  async with lock: active+=1; peak=max(peak,active)
  await asyncio.sleep(.02*(5-x%5))
  async with lock: active-=1
  return x*x
 out=await bounded_map(f,list(range(12)),3); assert out==[x*x for x in range(12)]; assert peak==3
 for bad in (0,-1):
  try: await bounded_map(f,[1],bad)
  except ValueError: pass
  else: raise AssertionError
asyncio.run(main()); print('HIDDEN_OK')
