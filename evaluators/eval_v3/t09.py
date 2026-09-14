import random, string, sys, time
sys.path.insert(0, sys.argv[1])
from window import longest_unique

def ref(t):
    best=''
    for i in range(len(t)):
        seen=set()
        for j in range(i,len(t)):
            if t[j] in seen:break
            seen.add(t[j]); s=t[i:j+1]
            if len(s)>len(best):best=s
    return best
for t in ('','abba','abcabcbb','dvdf','😀a😀bc','éabcédef','abcaefghibjk','abcadbef'):
    assert longest_unique(t)==ref(t),(t,longest_unique(t),ref(t))
r=random.Random(123); alphabet='abcd😀é日'
for _ in range(1000):
    t=''.join(r.choice(alphabet) for _ in range(r.randrange(0,30))); assert longest_unique(t)==ref(t),t
big=''.join(r.choice(string.ascii_letters) for _ in range(500000)); st=time.perf_counter(); got=longest_unique(big); elapsed=time.perf_counter()-st
assert len(got)==len(set(got)) and got in big and elapsed<3
print('EVAL_V3_OK', {'elapsed_s':elapsed})
