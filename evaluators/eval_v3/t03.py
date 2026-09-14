import random, sys, time, tracemalloc
sys.path.insert(0, sys.argv[1])
from cache import TTLCache

class Ref:
    def __init__(self,c,t): self.c=c; self.t=t; self.d={}; self.order=[]
    def purge(self,now):
        for k in list(self.order):
            if now-self.d[k][1]>=self.t:
                self.order.remove(k); del self.d[k]
    def put(self,k,v,now):
        if self.c<=0:return
        self.purge(now)
        if k in self.d:self.order.remove(k)
        elif len(self.d)>=self.c:
            old=self.order.pop(0); del self.d[old]
        self.d[k]=(v,now); self.order.append(k)
    def get(self,k,now,default=None):
        self.purge(now)
        if k not in self.d:return default
        v,_=self.d[k]; self.order.remove(k); self.order.append(k); return v

for seed in range(30):
    r=random.Random(seed); now=[0.0]; c=TTLCache(7,5,lambda:now[0]); ref=Ref(7,5)
    for _ in range(700):
        now[0]+=r.choice([0,.1,.5,1,3,5]); k=r.randrange(12)
        if r.random()<.55:
            v=r.randrange(1000); c.put(k,v); ref.put(k,v,now[0])
        else:
            assert c.get(k,'MISS')==ref.get(k,now[0],'MISS')

now=[0.0]; c=TTLCache(2,10,lambda:now[0]); c.put('a',1); now[0]=9; assert c.get('a')==1; now[0]=10; assert c.get('a','MISS')=='MISS'
now=[0.0]; c=TTLCache(2,10,lambda:now[0]); c.put('a',1); now[0]=9; c.put('a',2); now[0]=18; assert c.get('a')==2; now[0]=19; assert c.get('a','MISS')=='MISS'
now=[0.0]; c=TTLCache(2,5,lambda:now[0]); c.put('a',1); now[0]=1; c.put('b',2); now[0]=2; assert c.get('a')==1; c.put('c',3); assert c.get('b','MISS')=='MISS'
now=[0.0]; c=TTLCache(1,1,lambda:now[0]); c.put('a',1); now[0]=1; c.put('b',2); assert c.get('b')==2 and c.get('a','MISS')=='MISS'
for cap in (0,-2):
    z=TTLCache(cap,1,lambda:0); z.put('x',1); assert z.get('x','MISS')=='MISS'
now=[0.0]; z=TTLCache(1,0,lambda:now[0]); z.put('x',None); assert z.get('x','MISS')=='MISS'
now=[0.0]; z=TTLCache(1,10,lambda:now[0]); z.put('x',None); assert z.get('x','MISS') is None

now=[0.0]; n=5000; c=TTLCache(n,10**9,lambda:now[0])
for i in range(n): c.put(i,i)
t=time.perf_counter()
for i in range(n): assert c.get(i)==i
get_elapsed=time.perf_counter()-t

tracemalloc.start()
now=[0.0]; c2=TTLCache(8,10**9,lambda:now[0])
for i in range(8): c2.put(i,i)
for i in range(50000): c2.put(0,i)
current,peak=tracemalloc.get_traced_memory(); tracemalloc.stop()
assert c2.get(0)==49999
print('EVAL_V3_OK', {'get5000_s':get_elapsed,'hot_update_current_bytes':current,'hot_update_peak_bytes':peak})
