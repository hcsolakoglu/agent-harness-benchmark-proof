import sys,time,random,string
sys.path.insert(0,sys.argv[1]); from window import longest_unique
def valid(t,s): return s in t and len(s)==len(set(s))
def reflen(t):
 last={};start=0;best=0
 for i,c in enumerate(t):
  if c in last and last[c]>=start:start=last[c]+1
  last[c]=i;best=max(best,i-start+1)
 return best
for t in ['','abba','😀a😀bc','éabcédef','dvdf']: assert valid(t,longest_unique(t)) if t else longest_unique(t)==''; assert len(longest_unique(t))==reflen(t)
r=random.Random(0); t=''.join(r.choice(string.ascii_letters) for _ in range(300000)); st=time.perf_counter(); s=longest_unique(t); assert len(s)==reflen(t); assert time.perf_counter()-st<2
print('HIDDEN_OK')
