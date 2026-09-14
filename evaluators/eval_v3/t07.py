import asyncio, sys, time
sys.path.insert(0, sys.argv[1])
from amap import bounded_map

async def main():
    active=peak=0
    async def f(x):
        nonlocal active,peak
        active+=1; peak=max(peak,active)
        try: await asyncio.sleep(.001*(7-x%7))
        finally: active-=1
        return x*3
    out=await asyncio.wait_for(bounded_map(f,(i for i in range(100)),7),2)
    assert out==[i*3 for i in range(100)] and peak==7
    for bad in (0,-1):
        try:await bounded_map(f,[1],bad)
        except ValueError:pass
        else:raise AssertionError('bad limit accepted')

    consumed=0; gate=asyncio.Event()
    def source():
        nonlocal consumed
        for i in range(100000): consumed+=1; yield i
    async def blocked(x): await gate.wait(); return x
    t=asyncio.create_task(bounded_map(blocked,source(),4)); await asyncio.sleep(.02)
    assert consumed < 1024, ('eager source consumption',consumed)
    t.cancel()
    try:await asyncio.wait_for(t,.5)
    except asyncio.CancelledError:pass

    cancelled=0
    async def boom(x):
        nonlocal cancelled
        if x==1: raise RuntimeError('boom')
        try:
            await asyncio.sleep(.05 if x==0 else 1)
            return x
        except asyncio.CancelledError:
            cancelled+=1; raise
    started=time.perf_counter()
    try:await asyncio.wait_for(bounded_map(boom,range(20),3),1)
    except RuntimeError as e: assert str(e)=='boom'
    else:raise AssertionError('mapper failure not propagated')
    mapper_failure_s=time.perf_counter()-started

    class Bad:
        def __init__(self): self.n=0
        def __iter__(self): return self
        def __next__(self):
            self.n+=1
            if self.n==3: raise LookupError('source')
            return self.n
    async def quick(x): await asyncio.sleep(.005); return x
    try:await asyncio.wait_for(bounded_map(quick,Bad(),2),1)
    except LookupError as e: assert str(e)=='source'
    else:raise AssertionError('source failure not propagated')

    return {'lazy_consumed':consumed,'mapper_failure_s':mapper_failure_s,'cancelled_children':cancelled}

metrics=asyncio.run(main())
print('EVAL_V3_OK', metrics)
