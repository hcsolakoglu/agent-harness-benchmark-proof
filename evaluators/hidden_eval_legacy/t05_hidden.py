import sys
sys.path.insert(0,sys.argv[1]); from retry import retry
log=[]; n=[0]
def f():
 n[0]+=1
 if n[0]<4: raise ConnectionError('x')
 return 9
assert retry(f,attempts=4,base_delay=.5,sleep=log.append)==9; assert log==[.5,1.0,2.0]
log=[]
def bad(): raise ValueError('programmer bug')
try: retry(bad,attempts=4,sleep=log.append)
except ValueError: pass
else: raise AssertionError('non-transient swallowed')
assert log==[]
log=[]
try: retry(lambda: (_ for _ in ()).throw(TimeoutError('last')),attempts=2,base_delay=1,sleep=log.append)
except TimeoutError as e: assert str(e)=='last'
else: raise AssertionError('last error swallowed')
assert log==[1]
try: retry(lambda:1,attempts=0)
except ValueError: pass
else: raise AssertionError
print('HIDDEN_OK')
