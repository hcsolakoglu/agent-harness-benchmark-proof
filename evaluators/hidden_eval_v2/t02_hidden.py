import sys,json,random
sys.path.insert(0,sys.argv[1]); from stream import JsonlStream
objs=[{'x':'😀 café 日本語','i':i} for i in range(30)]; data=('\n'.join(json.dumps(x,ensure_ascii=False) for x in objs)+'\n').encode()
for seed in range(20):
 r=random.Random(seed); s=JsonlStream(); got=[]; i=0
 while i<len(data):
  k=r.randint(1,7); got+=s.feed(data[i:i+k]); i+=k
 assert got==objs
s=JsonlStream(); assert s.feed(b'{"x":1')==[]; assert s.feed(b'}\n\n')==[{'x':1}]
print('HIDDEN_OK')
