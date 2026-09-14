import copy, heapq, random, sys, time
sys.path.insert(0, sys.argv[1])
from scheduler import schedule

def ref(g):
    nodes=set(g); indeg={n:0 for n in nodes}; dependents={n:[] for n in nodes}
    for n,ds in g.items():
        for d in ds:
            if d not in nodes: raise KeyError(d)
            indeg[n]+=1; dependents[d].append(n)
    ready=[n for n,v in indeg.items() if v==0]; heapq.heapify(ready); out=[]
    while ready:
        n=heapq.heappop(ready); out.append(n)
        for x in dependents[n]:
            indeg[x]-=1
            if indeg[x]==0: heapq.heappush(ready,x)
    if len(out)!=len(nodes): raise ValueError
    return out

assert schedule({'b':['a','a'],'a':[]})==['a','b']
assert schedule({'z':[],'a':[],'m':['a']})==['a','m','z']
for seed in range(100):
    r=random.Random(seed); names=[f'n{i:03d}' for i in range(35)]; g={n:[] for n in names}
    for j in range(len(names)):
        for i in range(j):
            if r.random()<.07:g[names[j]].append(names[i])
    before=copy.deepcopy(g); assert schedule(g)==ref(g); assert g==before
for g in ({'a':['a']},{'a':['b'],'b':['c'],'c':['a']}):
    try:schedule(g)
    except ValueError:pass
    else:raise AssertionError('cycle not rejected')
try:schedule({'a':['missing']})
except KeyError:pass
else:raise AssertionError('missing dependency not rejected')
g={'b':['a'],'a':[]}; before=copy.deepcopy(g); schedule(g); assert g==before
n=10000; g={f'n{i:05d}':([] if i==0 else [f'n{i-1:05d}']) for i in range(n)}
t=time.perf_counter(); out=schedule(g); elapsed=time.perf_counter()-t
assert len(out)==n and out[0]=='n00000' and out[-1]==f'n{n-1:05d}' and elapsed<3
print('EVAL_V3_OK', {'elapsed_s':elapsed})
