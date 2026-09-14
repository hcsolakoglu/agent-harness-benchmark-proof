import random,time,sys
sys.path.insert(0,sys.argv[1]); from intervals import covered_length
def ref(xs):
 xs=sorted((min(a,b),max(a,b)) for a,b in xs if a!=b); total=0; cur=None
 for a,b in xs:
  if cur is None: cur=[a,b]
  elif a<=cur[1]: cur[1]=max(cur[1],b)
  else: total+=cur[1]-cur[0]; cur=[a,b]
 return total+(0 if cur is None else cur[1]-cur[0])
for seed in range(30):
 r=random.Random(seed); xs=[(r.randint(-10**9,10**9),r.randint(-10**9,10**9)) for _ in range(250)]; assert covered_length(xs)==ref(xs)
t=time.perf_counter(); assert covered_length([(0,10**12),(10**12-3,10**12+9)])==10**12+9; assert time.perf_counter()-t<1
print('HIDDEN_OK')
