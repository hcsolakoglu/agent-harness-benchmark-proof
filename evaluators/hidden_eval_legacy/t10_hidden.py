import sys
sys.path.insert(0,sys.argv[1]); from ledger import apply_batch
s={'a':5,'b':1}; out=apply_batch(s,[('sub','a',2),('add','b',4)]); assert out is not s and out=={'a':3,'b':5} and s=={'a':5,'b':1}
for ops in [[('sub','a',6)],[('mul','a',2)],[('add','a',-1)],[('add','x',3),('sub','x',4)]]:
 s={'a':5}; before=s.copy()
 try: apply_batch(s,ops)
 except (ValueError,KeyError): pass
 else: raise AssertionError(ops)
 assert s==before
# bool is not accepted as amount despite int subclass
try:apply_batch({'a':1},[('add','a',True)])
except ValueError:pass
else:raise AssertionError
print('HIDDEN_OK')
