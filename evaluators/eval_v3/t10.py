import sys
sys.path.insert(0, sys.argv[1])
from ledger import apply_batch
class MyInt(int):pass

def expect(exc,state,ops):
    before=state.copy()
    try:apply_batch(state,ops)
    except exc:pass
    except Exception as e:raise AssertionError(('wrong exception',type(e).__name__,ops))
    else:raise AssertionError(('no exception',ops))
    assert state==before

s={'a':5}; out=apply_batch(s,[('add','a',2),('sub','a',3),('add','b',4)]); assert s=={'a':5} and out=={'a':4,'b':4} and out is not s
for amt in (0,-1,1.0,'1',None,True,MyInt(1)):
    expect(ValueError,{'a':5},[('add','a',amt)]); expect(ValueError,{'a':5},[('sub','a',amt)])
expect(KeyError,{'a':5},[('sub','x',1)])
expect(ValueError,{'a':5},[('sub','a',6)])
expect(ValueError,{'a':5},[('mul','a',1)])
for ops in ([('add','a')],[('add','a',1,2)],[None],['add']):expect(ValueError,{'a':5},ops)
s={'a':5}
def late_ops():
    yield ('add','a',5); yield ('add','b',2); yield ('sub','a',99)
expect(ValueError,s,late_ops()); assert s=={'a':5}
print('EVAL_V3_OK')
