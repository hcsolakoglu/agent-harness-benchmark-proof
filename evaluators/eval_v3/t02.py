import json, sys, time
sys.path.insert(0, sys.argv[1])
from stream import JsonlStream

objs=[{'s':'😀 café 日本語','i':i,'nested':{'x':[1,2,3]}} for i in range(20)]
data=('\n'.join(json.dumps(x,ensure_ascii=False) for x in objs)+'\n').encode()
for cut in range(len(data)+1):
    s=JsonlStream(); got=s.feed(data[:cut])+s.feed(data[cut:]); assert got==objs, cut
s=JsonlStream(); got=[]
for b in data: got += s.feed(bytes([b]))
assert got==objs
s=JsonlStream(); assert s.feed(b'')==[]
assert s.feed(b' \t\r\n\n{"a":1}\r\n{"b":')==[{'a':1}]
assert s.feed('"😀"}\n'.encode())==[{'b':'😀'}]
assert s.feed(b'{"tail":')==[]

def bench(n):
    payload=json.dumps({'x':'a'*n}).encode()+b'\n'; s=JsonlStream(); got=[]
    t=time.perf_counter()
    for b in payload: got += s.feed(bytes([b]))
    elapsed=time.perf_counter()-t
    assert got==[{'x':'a'*n}]
    return elapsed
small=bench(50000); large=bench(200000)
ratio=large/max(small,1e-9)
print('EVAL_V3_OK', {'bytewise_50k_s':small,'bytewise_200k_s':large,'scaling_ratio':ratio})
