import random, sys, time
sys.path.insert(0, sys.argv[1])
from intervals import covered_length

def brute(xs):
    points=set()
    for a,b in xs:
        if a>b: a,b=b,a
        points.update(range(a,b))
    return len(points)

cases=[
    [], [(4,1)], [(1,4),(4,8)], [(5,5)],
    [(10,-10),(-5,3)], [(1,10),(2,3),(1,10)],
    [(-7,-2),(-5,4),(4,9)],
]
for case in cases:
    assert covered_length(case)==brute(case), case
for seed in range(100):
    r=random.Random(seed)
    xs=[(r.randint(-50,50), r.randint(-50,50)) for _ in range(r.randint(0,100))]
    assert covered_length(xs)==brute(xs), seed
assert covered_length((x for x in [(5,1),(2,9),(20,22)]))==10
huge=10**2000
assert covered_length([(huge,huge+9),(huge+9,huge+20)])==20
big=[(i*3,i*3+2) for i in range(50000)]
t=time.perf_counter(); assert covered_length(big)==100000; elapsed=time.perf_counter()-t
assert elapsed<3.0, elapsed
print('EVAL_V3_OK', {'elapsed_s':elapsed})
